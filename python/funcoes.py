
import os
import httpx
import asyncio
import pandas as pd
import time
from sqlalchemy import *
from pathlib import Path
from dotenv import load_dotenv

class menu:
	@staticmethod

	def exibir(opcoes):

		# Definição de tipo Lista ou Dicionário
		lista = list(opcoes.keys()) if isinstance(opcoes, dict) else opcoes

		# Mostrando as opções e tratamento de erros
		print()
		for i, item in enumerate(lista, 1):
			print(f"[{i}] - {item}")


		while True:
			try:
				numero = int(input("Escolha: ")) -1
				if  0 <= numero < len(lista):
					selecionado = lista[numero]
					break
				print("Digite um número válido!")
			except ValueError:
				print("Digite um número!")
				print()

		# Tratando do resultado final

		valor = opcoes[selecionado] if isinstance(opcoes, dict) else selecionado

		if isinstance(valor, (list, tuple, dict)):
			menu.espaçar()
			return menu.exibir(valor)

		elif callable(valor):
			menu.espaçar()
			return valor()

		else:
			menu.espaçar()
			print()
			return valor

	def espaçar():
		print("\n" + ">=<"*20)
	

class processamento():
	@staticmethod

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

	@staticmethod

	async def buscar_pokemon(client, id, sem):
		async with sem:
			url = f"https://pokeapi.co/api/v2/pokemon/{id}"
			return await client.get(url)

	@staticmethod
	async def conexao():
		sem = asyncio.Semaphore(50)
		async with httpx.AsyncClient() as client:
			tarefas = [processamento.buscar_pokemon(client, id + 1, sem) for id in range(1025)]

			respostas = await asyncio.gather(*tarefas)

			registros = []
			for response in respostas:
				if isinstance(response, httpx.Response) and response.status_code == 200:
					dados = response.json()
					dados_limpos = {
						"id":dados["id"],
						"name":dados["name"],
						"types": ",".join([t["type"]["name"] for t in dados["types"]]),
						"weight":dados["weight"],
						"hight":dados["height"]
					}
					registros.append(dados_limpos)

			df = pd.DataFrame(registros)

			return df

	@staticmethod
	def processo_completo():
		
		df = asyncio.run(processamento.conexao())
		menu.espaçar()
		print()
		print(df)
		conn = conexao_db.passar_conn()
		df.to_sql("Pokemons", con=conn["engine"], if_exists='replace', index=False)

class conexao_db():
	@staticmethod

	def passar_conn():
		credenciais = conexao_db.pegar_dotenv()
		url = f"postgresql://{credenciais["usuario"]}:{credenciais["senha"]}@{credenciais["host"]}:{credenciais["port"]}/{credenciais["banco"]}"
		engine = create_engine(url)
		
		metadata = MetaData(); metadata.reflect(bind=engine)
		conn = {"engine":engine, "metadata":metadata}
		
		return conn

	def pegar_dotenv():
		
		load_dotenv(dotenv_path='../.env')

		credenciais = {
			"usuario": os.getenv("DB_USER"),
			"senha": os.getenv("DB_PASS"),
			"banco": os.getenv("DB_NAME"),
			"host": os.getenv("DB_HOST"),
			"port": os.getenv("DB_PORT")
		}

		for key, value in credenciais.items():
			print(key, value)
		return credenciais