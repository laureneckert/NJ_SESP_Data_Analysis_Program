#NJSESP Project
#Lauren Eckert
#Version 2

from abc import ABC, abstractmethod
from hazard import Hazard
import utilities as uti
import os

class NaturalHazard(Hazard):
    def __init__(self, type_of_hazard):
        super().__init__(type_of_hazard)

        # Attributes specific to natural hazards
        self.NRI_data_fields = {}
        self.noaa_events = []
        self.noaa_event_count = 0
        self.unique_noaa_regions = set()
        self.unique_noaa_event_types = set()

        self.total_outages_sum = 0
        self.outage_total_by_county = {}
        
        self.eaglei_events = []
        self.unique_eaglei_regions = set()
        self.total_duration_eaglei = 0
        self.outage_duration_by_county = {}

    def calculate_statistics(self, noaa_to_eaglei_mapping):
        # Placeholder for method that calculates statistics based on NOAA and EagleI data
        pass

    def calculate_total_eaglei_outage_duration(self, outage_sum):
        # Placeholder for method that calculates total EagleI outage duration
        pass

    def calculate_scores(self):
        # Override the method from the parent class
        pass

    def print_basic_info(self):
        # Override the abstract method from the parent class
        print(f"Natural Hazard: {self.type_of_hazard}")
        print(f"Start Date: {self.start_date}, End Date: {self.end_date}")
        # Add more details as required


    @staticmethod
    @abstractmethod
    def create_default_instances():
        """
        Creates new hazard instances with default values.
        This method should be implemented in each subclass.
        """
        pass

    @staticmethod
    def load_or_create(pickle_path, subclass, force_recreate=False):
        if os.path.exists(pickle_path) and not force_recreate:
            print(f"Loading {pickle_path} from pickle.")
            return uti.load_pickle(pickle_path)
        else:
            if force_recreate:
                print(f"Force recreate flag is set. Creating new {subclass.__name__} instances.")
            else:
                print(f"No pickle file found at {pickle_path}. Creating new {subclass.__name__} instances.")

            data = subclass.create_default_instances()
            uti.save_to_pickle(data, pickle_path)
            return data[0]