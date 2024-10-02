from datetime import datetime
import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import shutil
from bson import ObjectId
from tqdm import tqdm 

import pandas as pd
from medspa_ai.configuration.base_syncer import BaseGSheetSync, ingestion_config


class GSheetSync(BaseGSheetSync):
    """
    A class to synchronize data from Google Sheets to a database.
    """
    def __init__(self):
        """
        Initializes the GSheetSync object with the input diagnosis sheet ID.
        """
        super().__init__(ingestion_config.input_diagnosis_sheet_id)

    def read_to_wrangle_data(self):
        """
        Reads data from Google Sheets, slices relevant content, and performs initial data cleaning.
        """
        # Reading data from Google Sheets
        self.df = self.read_data_from_sheet()

        # Slicing the relevant content only
        self.df = self.df.iloc[:, :ingestion_config.input_diagnosis_relevant_columns]
        self.df.dropna(how="all", inplace=True)

        # Fill empty 'QT_Category' cells forward
        self.df[ingestion_config.input_diagnosis_qt_category].ffill(inplace=True)

        # Rename columns as per requirements
        self.df.rename(
            columns={
                ingestion_config.input_diagnosis_qt_category: ingestion_config.input_diagnosis_replace1, 
                ingestion_config.input_diagnosis_qt_sub_category: ingestion_config.input_diagnosis_replace2
                }, inplace=True
            )

        # Cleaning up of columns eliminates edge cases
        self.df.columns = [i.strip() for i in self.df.columns]

    def create_features(self):
        """
        Wrangles the data and creates new features.
        """
        # Wrangling the data
        self.read_to_wrangle_data()

        # Create a new column by applying a transformation to an existing column
        self.df[ingestion_config.input_diagnosis_column3] = \
            self.df[ingestion_config.input_diagnosis_replace1].apply(lambda x: "_".join(x.lower().split()))

    @staticmethod
    def row_to_json(row):
        """
        Converts a pandas Series (row) to a JSON-compatible dictionary.
        """
        json_data = {}
        keys = row.index.tolist()
        values = row.values.tolist()

        # Iterate through values in the row
        for i in range(len(values)):
            current_value = values[i]
            has_non_null_after = any(pd.notna(v) for v in values[i+1:])

            if pd.isna(current_value) and has_non_null_after:
                json_data[keys[i]] = ''
            elif pd.notna(current_value):
                json_data[keys[i]] = current_value

        return json_data    

    def sync_input_diagnosis_coll_from_gsheet(self):
        """
        Synchronizes data from Google Sheets to the input diagnosis collection.
        """
        self.read_to_wrangle_data()

        self.create_features()

        current_time = datetime.now()

        uuid = ObjectId()

        metadata = {
            "category_id": uuid, 
            "category_description": "",
            "category_status": 1,
            "parent_category": "",
            "created_at": current_time,
            "updated_at": current_time,
            "created_by": "1",
            "updated_by": "1",
            "_is_deleted": 1,
        }        

        # Convert raw_df rows to JSON and insert into the database
        for i, row in tqdm(self.df.iterrows()):
            json_data = self.row_to_json(row)
            record = metadata.copy()  # Create a copy of metadata to avoid modifying the original
            record.update(json_data)
            ingestion_config.coll_input_diagnosis.insert_one(record)