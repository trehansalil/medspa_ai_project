import pandas as pd
import json

# sheet link
file_link = "https://docs.google.com/spreadsheets/d/1iAXQKhULnSwcWosUTARVahFZrHxmj1wBLZMoPSdKkxY/export?format=csv&gid=1402403750"

df = pd.read_csv(file_link)

# Selecting relevant columns
raw_df = df.iloc[:, :6]
raw_df.dropna(how="all", inplace=True)

# Fill empty 'QT_Category' cells forward
raw_df["QT_Category"].ffill(inplace=True)

# Rename columns as per reqd
raw_df.rename(columns={'QT_Category': 'category_name', 'QT_Sub Category': 'sub_category_name'}, inplace=True)

# Function to convert a row to JSON format
def row_to_json(row):
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

# Convert raw_df rows to JSON
json_list = [row_to_json(row) for i, row in raw_df.iterrows()]

# Output JSON data
for row in json_list:
    print(json.dumps(row, indent=4))
