from medspa_ai.utils.common import read_yaml
from medspa_ai.entity.config_entity import (DataIngestionConfig)
from medspa_ai.configuration import *

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        # self.params = read_yaml(params_filepath)

        # create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        # create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            client=client,
            db=db,
            coll_input_diagnosis=coll_input_diagnosis,
            g_sheets_url=g_sheets_url,
            input_diagnosis_sheet_id=config.input_diagnosis_sheet_id,
            input_diagnosis_qt_category=config.input_diagnosis_qt_category,
            input_diagnosis_qt_sub_category=config.input_diagnosis_qt_sub_category,
            input_diagnosis_relevant_columns=int(config.input_diagnosis_relevant_columns),
            input_diagnosis_column1=config.input_diagnosis_column1,
            input_diagnosis_column2=config.input_diagnosis_column2,
            input_diagnosis_column3=config.input_diagnosis_column3,  
            input_diagnosis_column4=config.input_diagnosis_column4,  
            input_diagnosis_column5=config.input_diagnosis_column5,  
            input_diagnosis_column6=config.input_diagnosis_column6,  
            input_diagnosis_column7=config.input_diagnosis_column7,            
            
        )

        return data_ingestion_config



