from funcoes import *
from insertion import *
from functools import partial
from prefect import task, flow


# opcoes={
# 	"Pesquisar Pokemons":partial(processamento.processo_completo)
# }

# menu.exibir(opcoes)

@flow
def ETL():
	conn = processo_conexao()
	df = processo_completo()
	df.to_sql("Raw_Pokemons", con=conn, schema="public", if_exists='replace', index=False)
	print("Processo Terminado")

if __name__ == "__main__":
	ETL()