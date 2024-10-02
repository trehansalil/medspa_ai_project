from medspa_ai.constants import *


import numpy as np
import pandas as pd
import os
import random
import time

import re
import string

from tqdm import tqdm

from pymongo import MongoClient
from pymongo.synchronous.database import Database
from pymongo.collection import Collection


import warnings
warnings.simplefilter('ignore')

client: MongoClient = MongoClient(mongo_db_uri)
db: Database = client[mongo_db_name]

coll_input_diagnosis: Collection = db[mongo_db_coll_input_diagnosis]
