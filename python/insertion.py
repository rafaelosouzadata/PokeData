import os
import httpx
import asyncio
import pandas as pd
from sqlalchemy import *
from pathlib import Path
from data_base import *
from funcoes import *
from prefect import task, flow

@task
def montar_lista(pergunta="Escolha um número de 1 a 1025: ", ):
	lista = []

	while True:
		try:
			dado = int(input(pergunta))

			if not dado:
				break
			elif 0 < dado <= 1025:
				lista.append(dado)

			else:
				print("Use valid numbers!")
		except:
			print("Use a number!")
	return lista

async def buscar_pokemon(client, id, sem):
	async with sem:
		url = f"https://pokeapi.co/api/v2/pokemon/{id}"
		return await client.get(url)

@task
async def conexao():
	sem = asyncio.Semaphore(20)
	async with httpx.AsyncClient() as client:
		tarefas = [buscar_pokemon(client, id + 1, sem) for id in range(1025)]

		response = await asyncio.gather(*tarefas)
	return response

@task
def pythonizando_dados(response):
	registros = []
	for r in response:
		if isinstance(r, httpx.Response) and r.status_code == 200:
				dados = r.json()
				registros.append(dados)

	return registros

@task
def filtro(dados_sujos):
	registros = []
	for dados in dados_sujos:
			dados_limpos = {
				"id":dados["id"],
				"name":dados["name"],
				"types": ",".join([t["type"]["name"] for t in dados["types"]]),
				"weight":dados["weight"],
				"hight":dados["height"]
			}
			registros.append(dados_limpos)

	df = pd.DataFrame(registros)

@task
def filtro2(dados_sujos):
	df = pd.DataFrame(dados_sujos)

	df['types'] = df['types'].apply(lambda x: ",".join([t["type"]["name"] for t in x]))

	df = df[["id", "name", "types", "weight", "height"]]

	return df

@flow(log_prints=True, name="Processo Completo")
def processo_completo():
	
	dados_brutos = asyncio.run(conexao())
	dados_sujos = pythonizando_dados(dados_brutos)
	df = filtro2(dados_sujos)

	menu.espaçar()
	print()
	print(df)
	return df
