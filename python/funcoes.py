from data_base import *
from sqlalchemy import *


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
                numero = int(input("Escolha: ")) - 1
                if 0 <= numero < len(lista):
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
        print("\n" + ">=<" * 20)banco
