#NJSESP Project
#Lauren Eckert
#Version 2

import os
import utilities as uti
from abc import ABC, abstractmethod

class DataSource(ABC):
    def __init__(self):
        # Basic constructor for the data source
        pass
    
    @staticmethod
    def load_or_create(pickle_path, file_path, data_class, force_recreate=False):
        print(f"load_or_create called with pickle_path: {pickle_path}, file_path: {file_path}, force_recreate: {force_recreate}")

        if os.path.exists(pickle_path) and not force_recreate:
            print(f"Pickle file found at {pickle_path}. Loading data from pickle.")
            return uti.load_pickle(pickle_path)
        else:
            if force_recreate:
                print("Force recreate flag is set. Ignoring existing pickle and recreating data.")
            else:
                print(f"No pickle file found at {pickle_path}. Extracting data from source.")
            
            # Call the class method for data extraction
            data = data_class.extract_data(file_path)
            uti.save_to_pickle(data, pickle_path)
            return data
        
    @staticmethod
    @abstractmethod
    def extract_data():
        """
        Extract data from the specified source.

        Parameters:
        source_path (str): The path to the data source, which could be a file path or a directory path.

        This is an abstract method and must be implemented by all subclasses.
        """
        pass

    @staticmethod
    @abstractmethod
    def print_samples(data_source, sample_size=5):
        """
        Print samples of data from a data source.

        This is an abstract method and must be implemented by all subclasses.

        Parameters:
        data_source (list): A list of data source objects.
        sample_size (int): The number of samples to print.
        """
        pass