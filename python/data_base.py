from sqlalchemy import *
# from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

def get_db_url():
	credentials = {
		"user": os.getenv("DB_USER"),
		"pass": os.getenv("DB_PASS"),
		"bank": os.getenv("DB_NAME"),
		"host": os.getenv("DB_HOST"),
		"port": os.getenv("DB_PORT")
	}
	url = f"postgresql://{credentials["user"]}:{credentials["pass"]}@{credentials["host"]}:{credentials["port"]}/{credentials["bank"]}"
	return url

def create_db_engine():
	url = get_db_url()
	engine = create_engine(url)
	return engine

def get_metadata(engine):
	metadata = MetaData(); metadata.reflect(bind=engine)
	return metadata