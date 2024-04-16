#NJSESP Project
#Lauren Eckert
#Version 2

# utilities.py

# Libraries
from datetime import datetime
import pandas as pd
import pickle
import sys
import contextlib
import njsesp_config

def parse_date_time(date_str, time_str):
    """
    Combine date and time strings into a single datetime object.

    Parameters:
    date_str (str): The date string in 'mm/dd/yyyy' format.
    time_str (str): The time string in 'HHMM' format.

    Returns:
    datetime: The combined datetime object.
    """
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
    """
    Loads and returns data from a pickle file.

    Parameters:
    file_path (str): The path of the pickle file to be loaded.

    Returns:
    object: The Python object loaded from the pickle file.
    """
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return None

@contextlib.contextmanager
def redirect_stdout_to_file(file_path):
    """
    Context manager for redirecting stdout to a file.

    Parameters:
    file_path (str): Path to the file where stdout will be written.

    Usage:
    with redirect_stdout_to_file(file path):
        print("This will go to the file.")
    """
    original_stdout = sys.stdout  # Save the original stdout
    with open(file_path, 'w') as file:
        sys.stdout = file  # Redirect stdout to the file
        yield
        sys.stdout = original_stdout  # Reset stdout back to original

def save_natural_hazards_to_pickles(hazards):
    for hazard in hazards:
        try:
            pickle_path = njsesp_config.get_pickle_path(hazard.type_of_hazard)
            if pickle_path:
                save_to_pickle(hazard, pickle_path)
                print(f"Saved {hazard.type_of_hazard} data to {pickle_path}")
            else:
                print(f"No pickle path found for {hazard.type_of_hazard}")
        except Exception as e:
            print(f"Error saving {hazard.type_of_hazard}: {e}")

def timedelta_to_hours(td):
    """Converts a Timedelta to hours as a float."""
    return td.total_seconds() / 3600.0

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0