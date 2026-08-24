from functools import partial
from prefect import task, flow
from prefect_shell import ShellOperation

from funcoes import *
from insertion import *
import data_base as mod_db


# opcoes={
# 	"Pesquisar Pokemons":partial(processamento.processo_completo)
# }

# menu.exibir(opcoes)
@task
def dbt_run():
	with ShellOperation(
		commands=[
			"cd ..",
		   	"docker compose run dbt run"]
	) as cleaning:
		process = cleaning.trigger()
		process.wait_for_completion()

		resultado = process.fetch_result()
		print(resultado)

@flow
def ETL():
	conn = processo_conexao()
	df = processo_completo()
	mod_db.save_to_db(conn, df)
	dbt_run()

if __name__ == "__main__":
	ETL()