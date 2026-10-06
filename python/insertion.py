import asyncio

import httpx
import polars as pl


async def buscar_pokemon(client, id, sem):
    async with sem:
        url = f"https://pokeapi.co/api/v2/pokemon/{id}"
        return await client.get(url)


async def conexao():
    sem = asyncio.Semaphore(20)
    async with httpx.AsyncClient() as client:
        tarefas = [buscar_pokemon(client, id + 1, sem) for id in range(1025)]

        response = await asyncio.gather(*tarefas)
    return response


def pythonizando_dados(response):
    registros = []
    for r in response:
        if isinstance(r, httpx.Response) and r.status_code == 200:
            dados = r.json()
            registros.append(dados)

    return registros


def filtro2(dados_sujos):
    df = pl.DataFrame(dados_sujos)

    df = df.with_columns(
        types=pl.col("types").map_elements(
            lambda x: ",".join([t["type"]["name"] for t in x])
        )
    )

    df = df.select("id", "name", "types", "weight", "height")
    return df


def processo_completo():
    print("iniciando extração de dados...")
    dados_brutos = asyncio.run(conexao())
    print("limpando dados...")
    dados_sujos = pythonizando_dados(dados_brutos)
    print("convertendo em dataframe...")
    df = filtro2(dados_sujos)
            
    return df


if __name__ == "__main__":
    df = processo_completo()

    print(df)
