import configparser
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config_path = os.path.join(os.getcwd(), "config_file.config")

config_parser = configparser.ConfigParser()
config_parser.read(config_path)

# Fetch the value of mongo_db_uri from .env
mongo_db_uri = os.getenv('MONGO_DB_URI')
# mongo_db_uri = config_parser.get('mongo_config', 'mongo_db_uri')
mongo_db_name = config_parser.get('mongo_config', 'mongo_db_name')
mongo_db_coll_input_diagnosis = config_parser.get('mongo_config', 'mongo_db_coll_input_diagnosis')


# All file inputs
g_sheets_url = config_parser.get('input_files', 'g_sheets_url')

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")