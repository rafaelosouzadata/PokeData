from funcoes import *
from insertion import *
from functools import partial
from prefect import task, flow


# opcoes={
# 	"Pesquisar Pokemons":partial(processamento.processo_completo)
# }

# menu.exibir(opcoes)

if __name__ == "__main__":
	processo_completo()