
import os
import requests
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

	def lista_automatica(batchsize=100):
		lista = []
		id = 0

		while id < 50:
			id += 1
			lista.append(id)
			if len(lista) == batchsize:
				yield lista
				lista = []
		if lista:
			yield lista


	def pedido(lista):
		registros = []
		for id in lista:
			url = f"https://pokeapi.co/api/v2/pokemon/{id}"
			response = requests.get(url)
			dados = response.json()

			dados_limpos = {
				"id": dados["id"],
				"nome": dados["name"],
				"tipo": dados["types"],
				"peso": dados["weight"],
				"altura": dados["height"]
			}

			registros.append(dados_limpos)
		return registros

	def pandificacao(registros):
		df = pd.DataFrame(registros)
		df = df.explode("tipo",ignore_index=True)
		df["tipo"] = df["tipo"].apply(lambda x: x["type"]["name"])
		return df

	def processo_completo():
		lista_batchs = []
		for dados in processamento.lista_automatica():
			registros = processamento.pedido(dados)
			batch = processamento.pandificacao(registros)
			lista_batchs.append(batch)
			time.sleep(0.5)

		df = pd.DataFrame()
		for batch in lista_batchs:
			df = pd.concat([df,batch], ignore_index=True)

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