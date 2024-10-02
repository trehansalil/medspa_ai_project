from dataclasses import dataclass

from pymongo import MongoClient
from pymongo.synchronous.database import Database
from pymongo.collection import Collection
from medspa_ai.constants import *
import os

@dataclass(frozen=True)
class DataIngestionConfig:
    client: MongoClient
    db: Database
    coll_input_diagnosis: Collection
    g_sheets_url: str
    input_diagnosis_sheet_id: str
    input_diagnosis_qt_category: str
    input_diagnosis_qt_sub_category: str
    input_diagnosis_relevant_columns: int
    input_diagnosis_column1: str
    input_diagnosis_column2: str    
    input_diagnosis_column3: str    
    input_diagnosis_column4: str    
    input_diagnosis_column5: str    
    input_diagnosis_column6: str  
    input_diagnosis_column7: str                    

