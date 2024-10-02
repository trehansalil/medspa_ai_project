import os
import inspect
from medspa_ai.logger import logging
from medspa_ai.entity.config_entity import DataIngestionConfig
from medspa_ai.configuration.gcloud_syncer import GSheetSync


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.gsheet_sync = GSheetSync(self.data_ingestion_config)
        
    def get_data_from_cloud(self) -> None:
        current_function_name = inspect.stack()[0][3]
        try:
            logging.info(f"Entered the {current_function_name} method of {self.__class__.__name__} class")
            # os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)
            # dataset_url = self.data_ingestion_config.source_url
            # unzip_dir = self.data_ingestion_config.unzip_dir
            # os.makedirs(self.data_ingestion_config.root_dir, exist_ok=True)
            logging.info(f"Ingesting data from google sheets into to mongo db's collection: {self.data_ingestion_config.coll_input_diagnosis.name}")

            self.gsheet_sync.sync_input_diagnosis_coll_from_gsheet()

            logging.info(f"Ingested data from google sheets into to mongo db's collection: {self.data_ingestion_config.coll_input_diagnosis.name}")            
            


            logging.info(f"Exited the {current_function_name} method of {self.__class__.__name__} class")
        except Exception as e:
            raise e

    def initiate_data_ingestion(self):
        current_function_name = inspect.stack()[0][3]
        logging.info(f"Entered the {current_function_name} method of {self.__class__.__name__} class")
        
        try:
            self.get_data_from_cloud()
            logging.info(f"Fetched the data from Gsheet using {current_function_name} method of {self.__class__.__name__} class")           

        except Exception as e:
            raise e   