import subprocess
from pathlib import Path

import data_base as mod_db
import insertion as mod_ins


def cli_execution(command: list):
    resultado = subprocess.run(
        command,
        # cwd="..",
        text=True,
        capture_output=True,
    )

    print(resultado.stdout)

    if resultado.returncode != 0:
        print("Erro na execução:", resultado.stderr)


def dbt_run():
    dbt_packages = Path(".") / "dbt" / "dbt_packages"

    if not dbt_packages.exists():
        dbt_deps_command = ["docker", "compose", "run", "--rm", "dbt", "deps"]
        cli_execution(dbt_deps_command)

    dbt_run_command = ["docker", "compose", "run", "--rm", "dbt", "build"]
    cli_execution(dbt_run_command)


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
