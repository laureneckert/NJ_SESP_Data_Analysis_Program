#Lauren Eckert
#NJSESP Project for Junior Clinic
#utilities.py

#Libraries
from datetime import datetime
import pickle

#imports from other package files
from hurricanes import Hurricane 
from NOAAEvent import NOAAEvent
from EagleIEvent import EagleIEvent

def parse_date_time(date_str, time_str):
    # Combine date and time into a single datetime object
    datetime_str = f"{date_str} {time_str}"
    return datetime.strptime(datetime_str, '%m/%d/%Y %H%M')

def save_to_pickle(obj, file_path):
    """
    Saves a given Python object to a pickle file.

    Parameters:
    obj (object): The Python object to be saved.
    file_path (str): The path where the pickle file will be saved.
    """
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)
        print(f"Object successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving object to pickle: {e}")