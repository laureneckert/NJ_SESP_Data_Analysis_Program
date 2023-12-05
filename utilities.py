#Lauren Eckert
#NJSESP Project for Junior Clinic
#utilities.py

#Libraries
from datetime import datetime
import pickle
import sys
import contextlib

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

def load_pickle(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)
    
@contextlib.contextmanager
def redirect_stdout_to_file(file_path):
    """
    Context manager for redirecting stdout to a file.

    Parameters:
    file_path (str): Path to the file where stdout will be written.
    """
    original_stdout = sys.stdout  # Save the original stdout
    with open(file_path, 'w') as file:
        sys.stdout = file  # Redirect stdout to the file
        yield
        sys.stdout = original_stdout  # Reset stdout back to original
