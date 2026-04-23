from funcoes import *
from functools import partial

opcoes={
	"Pesquisar Pokemons":partial(processamento.processo_completo)
}

menu.exibir(opcoes)