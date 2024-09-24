from medspa_ai.constants import *
from pymongo import MongoClient

client = MongoClient(mongo_db_uri)
db = client[mongo_db_name]

coll_input_diagnosis = db[mongo_db_coll_input_diagnosis]