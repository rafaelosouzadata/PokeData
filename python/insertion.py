import asyncio
from dataclasses import dataclass, field

import httpx
import polars as pl


@dataclass
class ApiInfo:
    which_api: str
    pokemon_qty: int = 1025
    url: str = field(init=False)
    df: pl.DataFrame = field(init=False)

    def __post_init__(self):
        match self.which_api:
            case "specie":
                self.url = "https://pokeapi.co/api/v2/pokemon-species/"
            case "pokemon":
                self.url = "https://pokeapi.co/api/v2/pokemon/"


async def buscar_pokemon(client, url, sem):
    async with sem:
        return await client.get(url)


async def conexao(api: ApiInfo):
    sem = asyncio.Semaphore(20)
    async with httpx.AsyncClient() as client:
        tarefas = []
        for id in range(api.pokemon_qty):
            tarefas.append(buscar_pokemon(client, f"{api.url}{id + 1}", sem))

        response = await asyncio.gather(*tarefas)
    return response


def pythonizando_dados(response):
    registros = []
    for r in response:
        if isinstance(r, httpx.Response) and r.status_code == 200:
            dados = r.json()
            registros.append(dados)

    return registros


def filter_pokemons(dados_sujos):
    df = pl.DataFrame(dados_sujos)

    df = df.with_columns(
        types=pl.col("types").map_elements(
            lambda x: ",".join([t["type"]["name"] for t in x])
        )
    )

    df = df.select("id", "name", "types", "weight", "height")
    return df


def filter_species(dados_sujos):
    df = pl.DataFrame(dados_sujos)

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
    print(f"== Processo de {api.which_api} ==")

    print("iniciando extração de dados...")
    dados_brutos = asyncio.run(conexao(api))

    print("limpando dados...")
    dados_sujos = pythonizando_dados(dados_brutos)

    print("convertendo em dataframe...")
    match api.which_api:
        case "pokemon":
            df = filter_pokemons(dados_sujos)
        case "specie":
            df = filter_species(dados_sujos)

    return df


def processo_completo(n: int = 1025):
    api_specie = ApiInfo("specie", n)
    api_pokemon = ApiInfo("pokemon", n)

    api_pokemon.df = extraction_orquestration(api_pokemon)
    api_specie.df = extraction_orquestration(api_specie)

    return [api_pokemon, api_specie]


if __name__ == "__main__":
    dados = processo_completo(10)

    print(dados)
