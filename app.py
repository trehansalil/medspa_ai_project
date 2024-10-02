from medspa_ai.configuration import *
from datetime import datetime
from bson import ObjectId
import pandas as pd
import json

from medspa_ai.configuration.gcloud_syncer import GSheetSync





sheet_puller = GSheetSync()

sheet_puller.sync_input_diagnosis_coll_from_gsheet()