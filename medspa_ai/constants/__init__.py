# Requires the PyMongo package.
# https://api.mongodb.com/python/current
import configparser
import os

config_path = os.path.join(os.getcwd(), "config_file.config")

config_parser = configparser.ConfigParser()
config_parser.read(config_path)

mongo_db_uri = config_parser.get('mongo_config', 'mongo_db_uri')
mongo_db_name = config_parser.get('mongo_config', 'mongo_db_name')
mongo_db_coll_input_diagnosis = config_parser.get('mongo_config', 'mongo_db_coll_input_diagnosis')


# All file inputs
g_sheets_url = config_parser.get('input_files', 'g_sheets_url')