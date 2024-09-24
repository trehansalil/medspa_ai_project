from medspa_ai.configuration import *
from datetime import datetime
from bson import ObjectId

category = "Skin Type"
current_time = datetime.now()
uuid = ObjectId()

coll_input_diagnosis.insert_one(
    {
        "category_id": uuid, 
        "category_name": category, 
        "category_slug":  "_".join(category.lower().split()), 
        "category_description": "",
        "category_Status": 1,
        "parent_category": "",
        "created_at": current_time,
        "updated_at": current_time,
        "created_by": "1",
        "updated_by": "1",
        "_is_deleted": 1,
        "sub_category_name": "Oil",
        "L1": "Oily"
    }
)