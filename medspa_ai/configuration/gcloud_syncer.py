from datetime import datetime
import hashlib
from typing import Dict
from bson import ObjectId
from tqdm import tqdm 
import pandas as pd
from medspa_ai.entity.config_entity import DataIngestionConfig
from medspa_ai.configuration.base_syncer import BaseGSheetSync

class GSheetSync(BaseGSheetSync):
    """
    A class to synchronize data from Google Sheets to a database, wrangle the data, and add metadata.
    """
    
    def __init__(self, ingestion_config: DataIngestionConfig):
        """
        Initializes the GSheetSync object with configuration for data ingestion.
        
        Parameters:
        ingestion_config (DataIngestionConfig): Configuration object containing Google Sheets ID, URL, and relevant columns.
        """
        # Initialize the base class with Google Sheets ID and URL
        super().__init__(ingestion_config.input_diagnosis_sheet_id, ingestion_config.g_sheets_url)
        
        # Store the ingestion config for further use
        self.ingestion_config = ingestion_config

    def read_to_wrangle_data(self):
        """
        Reads data from Google Sheets, selects relevant columns, performs basic cleaning, 
        and renames columns for further processing.
        """
        # Step 1: Reading the entire data from the specified Google Sheets
        self.df = self.read_data_from_sheet()

        # Step 2: Slice the dataframe to keep only relevant columns based on configuration
        self.df = self.df.iloc[:, :self.ingestion_config.input_diagnosis_relevant_columns]
        
        # Step 3: Remove rows where all values are NaN (completely empty rows)
        self.df.dropna(how="all", inplace=True)

        # Step 4: Fill missing 'QT_Category' values using forward fill method
        self.df[self.ingestion_config.input_diagnosis_qt_category].ffill(inplace=True)

        # Step 5: Rename columns to their intended names for downstream usage
        self.df.rename(
            columns={
                self.ingestion_config.input_diagnosis_qt_category: self.ingestion_config.input_diagnosis_column1,
                self.ingestion_config.input_diagnosis_qt_sub_category: self.ingestion_config.input_diagnosis_column2
            }, 
            inplace=True
        )

        # Step 6: Clean column names by stripping any leading/trailing spaces
        self.df.columns = [col.strip() for col in self.df.columns]

    def create_features(self):
        """
        Creates additional features from the wrangled data and re-arranges the columns for further use.
        """
        # Step 1: Perform data wrangling and cleaning
        self.read_to_wrangle_data()

        # Step 2: Create a new feature (column) by transforming values from the existing column
        # It lowercases and joins words with an underscore.
        self.df[self.ingestion_config.input_diagnosis_column3] = \
            self.df[self.ingestion_config.input_diagnosis_column1].apply(lambda x: "_".join(x.lower().split()))

        # Step 3: Re-arrange the columns in the dataframe as per the requirement
        cols = [
            self.ingestion_config.input_diagnosis_column1, self.ingestion_config.input_diagnosis_column2, 
            self.ingestion_config.input_diagnosis_column3, self.ingestion_config.input_diagnosis_column4,
            self.ingestion_config.input_diagnosis_column5, self.ingestion_config.input_diagnosis_column6,
            self.ingestion_config.input_diagnosis_column7
        ]
        self.df = self.df[cols]

    @staticmethod
    def row_to_json(row):
        """
        Converts a single row (Pandas Series) into a JSON-compatible dictionary.
        
        Parameters:
        row (pd.Series): A row of data to be converted to a JSON object.

        Returns:
        dict: JSON-compatible dictionary with keys as column names and values as row values.
        """
        json_data = {}
        keys = row.index.tolist()
        values = row.values.tolist()

        # Iterate over the row values and map keys to values
        for i in range(len(values)):
            current_value = values[i]
            # Check if there are non-null values after the current column
            has_non_null_after = any(pd.notna(v) for v in values[i+1:])

            # If current value is NaN and there are non-null values later, replace it with an empty string
            if pd.isna(current_value) and has_non_null_after:
                json_data[keys[i]] = ''
            elif pd.notna(current_value):
                json_data[keys[i]] = current_value

        return json_data  

    @staticmethod
    def generate_objectid_from_dict(data_dict: Dict) -> ObjectId:
        # Step 1: Convert dictionary to a sorted string to ensure consistent order
        dict_str = str(sorted(data_dict.items()))
        
        # Step 2: Hash the string representation of the dictionary using SHA-1 (or any hash function)
        hash_obj = hashlib.sha1(dict_str.encode('utf-8')).digest()
        
        # Step 3: Take the first 12 bytes of the hash to create a MongoDB ObjectId
        object_id_bytes = hash_obj[:12]
        
        # Step 4: Convert bytes to ObjectId
        object_id = ObjectId(object_id_bytes)
        
        return object_id      

    def sync_input_diagnosis_coll_from_gsheet(self):
        """
        Synchronizes the wrangled data from Google Sheets to the input diagnosis collection in the database.
        """
        # Step 1: Read and wrangle the data from Google Sheets
        self.read_to_wrangle_data()

        # Step 2: Create additional features from the wrangled data
        self.create_features()

        # Step 3: Generate current timestamp and a unique ObjectId for metadata
        current_time = datetime.now()
        uuid = ObjectId()

        # Metadata template to be added to each record
        metadata = {
            "category_description": "",
            "category_status": 1,
            "parent_category": "",
            "created_at": current_time,
            "updated_at": current_time,
            "created_by": "1",  # Placeholder values for user tracking
            "updated_by": "1",  # Placeholder values for user tracking
            "_is_deleted": 1,  # Mark the record as active (not deleted)
        }

        # Step 4: Iterate over each row, convert it to JSON format, and insert into the database
        for _, row in tqdm(self.df.iterrows(), desc="Inserting records to the database"):
            record = self.row_to_json(row)  # Convert the row to JSON
            record['_id'] = self.generate_objectid_from_dict(record)
            record.update(metadata)  # Add metadata to the record
            self.ingestion_config.coll_input_diagnosis.update_one(
                filter = {"_id": record['_id']},
                update = {"$set": record}, 
                upsert = True
            )  # Insert the record into the collection
