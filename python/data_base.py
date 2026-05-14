from sqlalchemy import *
from pathlib import Path
import os
from dotenv import load_dotenv
from prefect import task, flow

load_dotenv(dotenv_path='../.env')

@task
def get_db_url():
	credentials = {
		"user": os.getenv("DB_USER"),
		"pass": os.getenv("DB_PASS"),
		"bank": os.getenv("DB_NAME"),
		"host": os.getenv("DB_HOST"),
		"port": os.getenv("DB_PORT")
	}
	url = f"postgresql://{credentials['user']}:{credentials['pass']}@{credentials['host']}:{credentials['port']}/{credentials['bank']}"
	return url

    
@task
def create_db_engine(url):
	print(url)
	engine = create_engine(url)
	return engine

@task
def get_metadata(engine):
	metadata = MetaData(); metadata.reflect(bind=engine)
	return metadata

@flow(log_prints=True)
def processo_conexao():
	url = get_db_url()
	engine = create_db_engine(url)
	return engine