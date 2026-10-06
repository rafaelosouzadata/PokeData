import subprocess

import data_base as mod_db
import funcoes as mod_func
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
    conn = mod_func.processo_conexao()
    print("iniciando conexão com API...")
    df = mod_ins.processo_completo()
    print("salvando no banco de dados...")
    mod_db.save_to_db(conn, df)
    print("rodando dbt")
    dbt_run()


if __name__ == "__main__":
    try:
        ETL()
    except Exception as e:
        print(e)