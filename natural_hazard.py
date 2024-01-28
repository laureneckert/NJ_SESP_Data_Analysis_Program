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

    @abstractmethod
    def print_basic_info(self):
        pass

    def add_noaa_event(self, noaa_event):
        """
        Adds a NOAA event to the noaa_events list.

        Parameters:
        noaa_event: The NOAAEvent object to be added.
        """
        self.noaa_events.append(noaa_event)
    
    def add_eaglei_event(self, eaglei_event):
        """
        Adds an Eagle I event to the eaglei_events list.

        Parameters:
        eaglei_event: The EagleIEvent object to be added.
        """
        self.eaglei_events.append(eaglei_event)

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