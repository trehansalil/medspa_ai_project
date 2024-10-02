# Importing necessary modules and classes
from abc import abstractmethod

# Importing pandas for data manipulation
import pandas as pd


"""
BaseGSheetSync Class:
This is an abstract base class for Google Sheets synchronization.
It provides a basic structure for reading data from a Google Sheet.
"""

class BaseGSheetSync:
    """
    Parameters:
    sheet_id (str): The ID of the Google Sheet to be synced.
    """

    def __init__(self, sheet_id, gsheet_url):
        """
        Initializes the BaseGSheetSync object with the given sheet_id and gsheet_url.
        """
        self.sheet_id = sheet_id
        self.gsheet_url = gsheet_url

    @abstractmethod
    def read_data_from_sheet(self) -> pd.DataFrame:
        """
        Abstract method to read data from the Google Sheet.
        This method is to be implemented by the child classes.

        Returns:
        pd.DataFrame: The data read from the Google Sheet.
        """
        # Generate the link to the Google Sheet in CSV format
        sheet_link = f"{self.gsheet_url}/export?format=csv&gid={self.sheet_id}"

        # Read the data from the sheet using the generated link
        df = pd.read_csv(sheet_link)

        # Return the read data
        return df