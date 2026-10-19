"""Extraction pipeline for PokeAPI data.

Fetches Pokémon and Pokémon-species records concurrently from PokeAPI
(https://pokeapi.co) using ``httpx`` and ``asyncio``, and converts them into
cleaned ``polars`` DataFrames.

Typical usage:
    >>> data = insertion_pipeline(10)  # doctest: +SKIP
    >>> data[0].df.columns  # doctest: +SKIP
    ['id', 'name', 'types', 'weight', 'height']
"""

import asyncio
from dataclasses import dataclass, field

import httpx
import polars as pl


@dataclass
class ApiInfo:
    """Configuration and result holder for one PokeAPI endpoint.

    The endpoint URL is derived from ``which_api`` in ``__post_init__``.
    The ``df`` attribute is not set on creation; it is filled in later by the
    extraction step.

    Attributes:
        which_api: Endpoint to query. Supported values are ``"specie"``
            (pokemon-species) and ``"pokemon"``.
        pokemon_qty: Number of records to fetch, as sequential ids starting at
            1. Defaults to 1025.
        url: Base URL of the endpoint, ending with a slash. Derived from
            ``which_api``; not an init argument.
        df: DataFrame with the cleaned records. Not an init argument; set by
            the pipeline after extraction.
    """

    which_api: str
    pokemon_qty: int = 1025
    url: str = field(init=False)
    df: pl.DataFrame = field(init=False)

    def __post_init__(self):
        """Set ``url`` according to ``which_api``.

        Note:
            If ``which_api`` is not ``"specie"`` or ``"pokemon"``, ``url`` is
            left unset and accessing it raises ``AttributeError``.
        """
        match self.which_api:
            case "specie":
                self.url = "https://pokeapi.co/api/v2/pokemon-species/"
            case "pokemon":
                self.url = "https://pokeapi.co/api/v2/pokemon/"


async def search_process(client, url, sem):
    """Perform a GET request while respecting a concurrency limit.

    Args:
        client (httpx.AsyncClient): Client used to send the request.
        url (str): Full URL to request.
        sem (asyncio.Semaphore): Semaphore that caps how many requests run at
            the same time.

    Returns:
        httpx.Response: The response, whatever its status code.
    """
    async with sem:
        return await client.get(url)


async def connect_api(api: ApiInfo):
    """Fetch every record of an endpoint concurrently.

    Requests ids ``1`` through ``api.pokemon_qty`` with at most 20 requests in
    flight at once.

    Args:
        api: Endpoint configuration. ``api.url`` and ``api.pokemon_qty`` are
            used.

    Returns:
        list[httpx.Response]: One response per requested id, in id order.
        Responses with non-200 status codes are included; filtering is left to
        the caller.

    Raises:
        httpx.HTTPError: If any request fails at the transport level
            (timeout, connection error, etc.). The remaining requests are not
            cancelled automatically.
    """
    sem = asyncio.Semaphore(20)
    async with httpx.AsyncClient() as client:
        tarefas = []
        for id in range(api.pokemon_qty):
            tarefas.append(search_process(client, f"{api.url}{id + 1}", sem))

        response = await asyncio.gather(*tarefas)
    return response


def api_to_dict(response):
    """Extract the JSON payload from successful responses.

    Args:
        response (list[httpx.Response]): Responses returned by
            ``connect_api``. Items that are not ``httpx.Response`` instances
            are ignored.

    Returns:
        list[dict]: Decoded JSON bodies of the responses with status code 200.
        Any other response is silently discarded, so the result may be shorter
        than the input.
    """
    registers = []
    for r in response:
        if isinstance(r, httpx.Response) and r.status_code == 200:
            data = r.json()
            registers.append(data)

    return registers


def filter_pokemons(dirty_data):
    """Build the Pokémon DataFrame from raw API records.

    The ``types`` field, originally a list of nested structs, is flattened into
    a comma-separated string of type names (e.g. ``"grass,poison"``).

    Args:
        dirty_data (list[dict]): Raw records from the ``pokemon`` endpoint.

    Returns:
        pl.DataFrame: DataFrame with the columns ``id``, ``name``, ``types``,
        ``weight`` and ``height``.
    """
    df = pl.DataFrame(dirty_data)

    df = df.with_columns(
        types=pl.col("types").map_elements(
            lambda x: ",".join([t["type"]["name"] for t in x])
        )
    )

    df = df.select("id", "name", "types", "weight", "height")
    return df


def filter_species(dirty_data):
    """Build the species DataFrame from raw API records.

    The ``generation`` field, originally a struct, is reduced to its ``name``
    (e.g. ``"generation-i"``).

    Args:
        dirty_data (list[dict]): Raw records from the ``pokemon-species``
            endpoint.

    Returns:
        pl.DataFrame: DataFrame with the columns ``id``, ``name``, ``order``,
        ``gender_rate``, ``capture_rate``, ``is_baby``, ``is_legendary``,
        ``is_mythical`` and ``generation``.
    """
    df = pl.DataFrame(dirty_data)

    df = df.with_columns(generation=pl.col("generation").struct.field("name"))
    df = df.select(
        "id",
        "name",
        "order",
        "gender_rate",
        "capture_rate",
        "is_baby",
        "is_legendary",
        "is_mythical",
        "generation",
    )
    return df


def extraction_orquestration(api: ApiInfo):
    """Run the full extraction for one endpoint.

    Steps: fetch all records, keep the successful ones, and convert them into
    a cleaned DataFrame. Progress is printed to stdout.

    Args:
        api: Endpoint configuration. ``api.which_api`` selects the cleaning
            function (``"pokemon"`` or ``"specie"``).

    Returns:
        pl.DataFrame: The cleaned DataFrame for the endpoint.

    Raises:
        UnboundLocalError: If ``api.which_api`` is neither ``"pokemon"`` nor
            ``"specie"`` (``df`` is never assigned).
        httpx.HTTPError: If a request fails at the transport level.
    """
    print(f"== Processo de {api.which_api} ==")

    print("iniciando extração de dados...")
    raw_data = asyncio.run(connect_api(api))

    print("limpando dados...")
    dirty_data = api_to_dict(raw_data)

    print("convertendo em dataframe...")
    match api.which_api:
        case "pokemon":
            df = filter_pokemons(dirty_data)
        case "specie":
            df = filter_species(dirty_data)

    return df


def insertion_pipeline(n: int = 1025):
    """Extract Pokémon and species data for the first ``n`` ids.

    Any exception raised during extraction is caught and printed, not
    re-raised. In that case the returned ``ApiInfo`` objects may have no
    ``df`` attribute set.

    Args:
        n: Number of records to fetch from each endpoint. Defaults to 1025.

    Returns:
        list[ApiInfo]: Two items, in order: the ``"pokemon"`` ``ApiInfo`` and
        the ``"specie"`` ``ApiInfo``, each with its ``df`` populated on
        success.
    """
    api_specie = ApiInfo("specie", n)
    api_pokemon = ApiInfo("pokemon", n)

    try:
        api_pokemon.df = extraction_orquestration(api_pokemon)
        api_specie.df = extraction_orquestration(api_specie)
    except Exception as e:
        print(f"Erro: {e}")

    return [api_pokemon, api_specie]


if __name__ == "__main__":
    data = insertion_pipeline(10)

    print(data)