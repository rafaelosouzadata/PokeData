"""Entry point of the PokeData pipeline.

Runs the whole flow in order: extract data from PokeAPI, load it into
PostgreSQL as raw tables, then transform it with dbt (executed through
Docker Compose).
"""

import subprocess
from pathlib import Path

import data_base as mod_db
import insertion as mod_ins


def cli_execution(command: list[str]):
    """Run a command-line program and print its output.

    The standard output is printed after the command finishes. If the exit
    code is not zero, the standard error is printed as well.

    Args:
        command: Program and arguments, as a list of strings (for example
            ``["docker", "compose", "run", "--rm", "dbt", "build"]``).

    Returns:
        None

    Note:
        A failing command does not raise an exception or stop the caller; the
        error is only printed. The exit code is not returned.
    """
    result = subprocess.run(
        command,
        # cwd="..",
        text=True,
        capture_output=True,
    )

    print(result.stdout)

    if result.returncode != 0:
        print("Erro na execução:", result.stderr)


def dbt_run():
    """Run the dbt project through Docker Compose.

    Installs the dbt packages (``dbt deps``) only when the ``dbt/dbt_packages``
    directory does not exist yet, then runs ``dbt build``, which executes
    models, tests, seeds and snapshots.

    Returns:
        None

    Note:
        The ``dbt/dbt_packages`` path is relative to the current working
        directory, so the function must be run from the project root. If
        ``dbt deps`` fails, ``dbt build`` still runs.
    """
    dbt_packages = Path(__file__).parent / "dbt" / "dbt_packages"

    if not dbt_packages.exists():
        dbt_deps_command = ["docker", "compose", "run", "--rm", "dbt", "deps"]
        cli_execution(dbt_deps_command)

    dbt_run_command = ["docker", "compose", "run", "--rm", "dbt", "build"]
    cli_execution(dbt_run_command)


def ETL():
    """Run the full pipeline: extract, load and transform.

    Steps:
        1. Create the database engine.
        2. Extract Pokémon and species data from PokeAPI.
        3. Save each resulting DataFrame into its raw table.
        4. Run dbt to build the transformed models.

    Returns:
        None

    Note:
        Failures in the extraction and loading steps are caught and printed
        inside those functions, so dbt may still run even when no new data was
        saved.
    """
    print("conectando ao banco de dados...")
    conn = mod_db.db_connect()

    print("iniciando conexão com API...")
    dados = mod_ins.insertion_pipeline()

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