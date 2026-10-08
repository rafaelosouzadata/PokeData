import os

import polars as pl
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def get_db_url():
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
    print(url)
    engine = sa.create_engine(url)
    return engine


def get_metadata(engine):
    metadata = sa.MetaData()
    metadata.reflect(bind=engine)
    return metadata


def save_to_db(conn, df):
    try:
        if type(df) == pl.DataFrame:
            df = df.to_pandas()

        df.to_sql(
            "raw_pokemons", con=conn, schema="public", if_exists="replace", index=False
        )
    except Exception as e:
        print(e)


def processo_conexao():
    url = get_db_url()
    engine = create_db_engine(url)
    return engine

if __name__ == "__main__":

    print(get_db_url())