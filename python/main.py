import subprocess

import data_base as mod_db
import insertion as mod_ins


def dbt_run():
    resultado = subprocess.run(
        ["docker", "compose", "run", "dbt", "run"],
        # cwd="..",
        text=True,
        capture_output=True,
    )

    print(resultado.stdout)

    if resultado.returncode != 0:
        print("Erro na execução:", resultado.stderr)


def ETL():
    print("conectando ao banco de dados...")
    conn = mod_db.processo_conexao()

    print("iniciando conexão com API...")
    dados = mod_ins.processo_completo()

    for dado in dados:
        print(f"salvando no banco de dados: {dado.which_api}")
        mod_db.save_to_db(conn, dado)

    print("rodando dbt")
    dbt_run()


if __name__ == "__main__":
    try:
        ETL()
    except Exception as e:
        print(e)
