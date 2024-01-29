#NJSESP Project
#Lauren Eckert
#Version 2

from abc import ABC, abstractmethod
from hazard import Hazard
import utilities as uti
import os
import EagleIEvent
import NOAAEvent
import FEMA_NRI_data

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
            loaded_data = uti.load_pickle(pickle_path)
            # Return the first item if loaded_data is a list, otherwise return the loaded_data itself
            return loaded_data[0] if isinstance(loaded_data, list) else loaded_data
        else:
            if force_recreate:
                print(f"Force recreate flag is set. Creating new {subclass.__name__} instances.")
            else:
                print(f"No pickle file found at {pickle_path}. Creating new {subclass.__name__} instances.")

            data = subclass.create_default_instances()
            uti.save_to_pickle(data, pickle_path)
            return data[0] if isinstance(data, list) else data

    def print_data_source_samples(self, sample_size=5):
            """
            Prints samples from each data source associated with the hazard.

            Parameters:
            sample_size (int): The number of samples to print from each data source.
            """
            print(f"\n{self.type_of_hazard.upper()} Hazard Data Samples:")

            # Print NOAA Event Samples
            print("\nNOAA Event Samples:")
            for i, event in enumerate(self.noaa_events[:sample_size]):
                print(f"Sample {i+1}: {event}")

            # Print Eagle I Event Samples
            print("\nEagle I Event Samples:")
            for i, event in enumerate(self.eaglei_events[:sample_size]):
                print(f"Sample {i+1}: {event}")

            # Print FEMA NRI Data Samples
            print("\nFEMA NRI Data Samples:")
            for i, (key, value) in enumerate(self.NRI_data_fields.items()):
                if i >= sample_size:
                    break
                print(f"Sample {i+1}: {key} - {value}")

            print("\nEnd of Data Samples")

    def calculate_percent_customers_affected(self):
        # Define the total number of customers in the state
        total_customers_in_state = 4030000 #according to utilities websites

        if total_customers_in_state > 0:
            self.percent_customers_affected = (self.customers_affected_sum / total_customers_in_state) * 100
        else:
            self.percent_customers_affected = 0.0

    def calculate_property_damage(self, hazard_prefix):
        """
        Calculates the total property damage for the hazard.

        Parameters:
        hazard_prefix (str): The prefix used for the specific natural hazard in FEMA data.

        Returns:
        float: The total property damage for the hazard.
        """
        exposure_attribute = f"{hazard_prefix}_EXPT"
        loss_ratio_attribute = f"{hazard_prefix}_HLRR"
        property_damage = 0.0

        for key, value in self.NRI_data_fields.items():
            if key.startswith(exposure_attribute) and key.replace(exposure_attribute, loss_ratio_attribute) in self.NRI_data_fields:
                exposure = value
                loss_ratio = self.NRI_data_fields[key.replace(exposure_attribute, loss_ratio_attribute)]
                property_damage += exposure * loss_ratio

        return property_damage

    def calculate_probability(self, hazard_prefix):
        """
        Calculates the annualized frequency (probability) of the hazard.

        Parameters:
        hazard_prefix (str): The prefix used for the specific natural hazard in FEMA data.

        Returns:
        float: The annualized frequency of the hazard.
        """
        frequency_attribute = f"{hazard_prefix}_AFREQ"
        total_frequency = 0.0
        count = 0

        for key, value in self.NRI_data_fields.items():
            if key.startswith(frequency_attribute):
                total_frequency += value
                count += 1

        return total_frequency / count if count > 0 else 0.0
