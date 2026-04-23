
import requests
import pandas as pd

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
		print(df)


	def processo_completo():
		lista = processamento.montar_lista()
		registros = processamento.pedido(lista)
		menu.espaçar()
		print()
		processamento.pandificacao(registros)
