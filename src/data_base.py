"""Database helpers for the PokeData pipeline.

Reads PostgreSQL credentials from environment variables (optionally loaded
from a ``.env`` file), creates a SQLAlchemy engine, and saves the DataFrames
produced by the extraction step into raw tables.

Environment variables:
    DB_USER: Database user.
    DB_PASS: Database password.
    DB_NAME: Database name.
    DB_HOST: Database host.
    DB_PORT: Database port.
"""

import os

import polars as pl
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def get_db_url():
    """Build the PostgreSQL connection URL from environment variables.

    Reads ``DB_USER``, ``DB_PASS``, ``DB_HOST``, ``DB_PORT`` and ``DB_NAME``.

    Returns:
        str: URL in the form
        ``postgresql://user:pass@host:port/dbname``. The password is included
        in plain text, so the value should never be printed or logged.

    Note:
        Missing variables are not detected: ``os.getenv`` returns ``None``,
        which ends up in the URL as the string ``"None"``. The password is
        also not URL-escaped, so special characters such as ``@`` or ``/``
        will produce an invalid URL.
    """
    credentials = {
        "user": os.getenv("DB_USER"),
        "pass": os.getenv("DB_PASS"),
        "bank": os.getenv("DB_NAME"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }
    url = f"postgresql://{credentials['user']}:{credentials['pass']}@{credentials['host']}:{credentials['port']}/{credentials['bank']}"
    return url


def create_db_engine(url):
    """Create a SQLAlchemy engine for the given URL.

    Args:
        url (str): Database connection URL, as returned by ``get_db_url``.

    Returns:
        sqlalchemy.engine.Engine: Engine bound to the database. No connection
        is opened until the engine is first used.
    """
    engine = sa.create_engine(url)
    return engine


def get_metadata(engine):
    """Reflect the existing database schema.

    Args:
        engine (sqlalchemy.engine.Engine): Engine used to inspect the database.

    Returns:
        sqlalchemy.MetaData: Metadata populated with every table found in the
        default schema. This opens a connection and queries the database.
    """
    metadata = sa.MetaData()
    metadata.reflect(bind=engine)
    return metadata


def save_to_db(conn, data):
    """Save the DataFrame of an ``ApiInfo`` object into a raw table.

    The target table is chosen from ``data.which_api``: ``"pokemon"`` goes to
    ``public.raw_pokemons`` and ``"specie"`` goes to ``public.raw_species``.
    The DataFrame is converted to pandas and written with ``DataFrame.to_sql``.
    If the table already exists, it is **replaced**.

    Args:
        conn (sqlalchemy.engine.Engine | sqlalchemy.engine.Connection):
            Engine or connection used to write the data.
        data (ApiInfo): Object holding ``which_api`` and the ``df`` DataFrame
            produced by the extraction step.

    Returns:
        None

    Note:
        All exceptions are caught and printed, not re-raised, so a failed save
        does not stop the caller. This includes the cases where ``data.which_api``
        is invalid or ``data.df`` is not a ``polars.DataFrame``.
    """
    try:
        match data.which_api:
            case "pokemon":
                table = "raw_pokemons"
            case "specie":
                table = "raw_species"

        if type(data.df) == pl.DataFrame:
            df = data.df.to_pandas()

        df.to_sql(table, con=conn, schema="public", if_exists="replace", index=False)
    except Exception as e:
        print(f"Erro no salvamento: {e}")


def db_connect():
    """Create an engine from the environment configuration.

    Shortcut that chains ``get_db_url`` and ``create_db_engine``.

    Returns:
        sqlalchemy.engine.Engine: Engine connected to the configured
        PostgreSQL database.
    """
    url = get_db_url()
    engine = create_db_engine(url)
    return engine


# if __name__ == "__main__":