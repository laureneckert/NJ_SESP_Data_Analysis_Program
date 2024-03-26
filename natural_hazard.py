#NJSESP Project
#Lauren Eckert
#Version 2

from abc import ABC, abstractmethod
from hazard import Hazard
import utilities as uti
import os
import pandas as pd

class NaturalHazard(Hazard):
    def __init__(self, type_of_hazard):
        super().__init__(type_of_hazard)

        # Attributes specific to natural hazards
        self.NRI_data_fields = {}
        self.noaa_events = []
        self.noaa_event_count = 0
        self.processed_noaa_windows = [] #store processed event windows
        self.threat_incident_count = 0 
        self.unique_noaa_regions = set()
        self.unique_noaa_event_types = set()

        self.total_outages_sum = 0
        self.outage_total_by_county = {}
        
        self.eaglei_events = []
        self.unique_eaglei_regions = set()
        
        self.average_duration_above_baseline = 0.0 #average per threat incident
        #self.outage_duration_by_county = {} #to delete?
        self.timestamps_above_baseline = []

    def calculate_statistics(self, noaa_to_eaglei_mapping):
        # Placeholder for method that calculates statistics based on NOAA and EagleI data
        # Default implementation for natural hazards
        # Implement generic behavior here
        pass

    def calculate_scores(self):
        # Override the method from the parent class
        # Default implementation for natural hazards
        # Implement generic behavior here
        pass

    def calculate_risk(self):
        # Default implementation for natural hazards
        # Implement generic behavior here
        pass

    def print_basic_info(self):
        # Default implementation for natural hazards
        # Implement generic behavior here
        print(f"Natural Hazard: {self.type_of_hazard}")

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

    def get_event_times(self, event): #for NOAA events, should probably go in that class

        """
        Adjusts the event times, taking into account peculiarities such as missing end times.
        """
        start_time = uti.parse_date_time(event.begin_date, str(event.begin_time).zfill(4))
        if event.end_date and event.end_time:
            end_time = uti.parse_date_time(event.end_date, str(event.end_time).zfill(4))
        else:
            end_time = start_time + pd.Timedelta(hours=1)  # Adjust according to your logic

        # Ensure end_time is not before start_time
        if end_time <= start_time:
            end_time = start_time + pd.Timedelta(hours=1)

        print(f"Event: {event.event_id}, Start: {start_time}, End: {end_time}, Type: {event.event_type}")
        return start_time, end_time

    def process_noaa_events(self):
        print("Sorting NOAA events by start date.")
        self.noaa_events.sort(key=lambda event: event.begin_date)

        merged_windows = []
        print("Processing NOAA events for overlapping and extending end times.")
        for event in self.noaa_events:
            start_time, end_time = self.get_event_times(event)  # Use the new method here
 
            # Check if this event logically should be merged with the last window
            if merged_windows:
                last_window_start_year = merged_windows[-1][0].year
                current_event_year = start_time.year
                # Ensure events are from the same year and check temporal proximity
                if last_window_start_year == current_event_year and start_time <= merged_windows[-1][1] + pd.Timedelta(hours=1):
                    merged_windows[-1][1] = max(merged_windows[-1][1], end_time)
                    merged_windows[-1][2].add(event.filename)
                    print(f"Merged with window from {merged_windows[-1][0]} to {merged_windows[-1][1]}, from files: {merged_windows[-1][2]}")
                else:
                    merged_windows.append([start_time, end_time, {event.filename}])
                    print(f"Created new window from {start_time} to {end_time}, from file {event.filename}")
            else:
                merged_windows.append([start_time, end_time, {event.filename}])
                print(f"Created new window from {start_time} to {end_time}, from file {event.filename}")

        self.processed_noaa_windows = [(window[0], window[1], window[2]) for window in merged_windows]
        self.threat_incident_count = len(merged_windows)
        print(f"Finished processing. Total threat incidents: {self.threat_incident_count}.")

    def print_noaa_window_summary(self):
        """
        Prints a summary of processed NOAA event windows, including the filenames.
        """
        print(f"{self.type_of_hazard} has {self.threat_incident_count} threat incidents.")
        for start, end, filenames in self.processed_noaa_windows:
            filenames_str = ', '.join(filenames)  # Convert the set of filenames to a string
            print(f"Window: {start} to {end}, Source Files: {filenames_str}")

    def calculate_duration_above_baseline_for_windows(self, event_windows, ewma_data, seasonal_baseline):
        if not event_windows:
            print("No event windows provided for analysis.")
            return pd.Timedelta(0), []

        if ewma_data.empty or seasonal_baseline.empty:
            print("EWMA data or seasonal baseline is empty.")
            return pd.Timedelta(0), []

        total_duration_above = pd.Timedelta(0)
        timestamps_above = []
        ewma_start, ewma_end = ewma_data.index[0], ewma_data.index[-1]

        print("Processing event windows to calculate total time above baseline.")

        for window in event_windows:
            start, end = pd.to_datetime(window[0]), pd.to_datetime(window[1])
            
            # Check if window is within EWMA data range
            if start > ewma_end or end < ewma_start:
                print(f"Skipping window from {start} to {end} as it is outside the EWMA data range.")
                continue

            # Adjust window to overlap with EWMA data timeframe
            window_start = max(start, ewma_start)
            window_end = min(end, ewma_end)

            window_ewma = ewma_data[window_start:window_end]
            window_baseline = seasonal_baseline[window_start:window_end]
            window_above_baseline = window_ewma > window_baseline

            # Add check for empty window_above_baseline
            if window_above_baseline.empty:
                print("No data points above baseline in this window.")
                continue

            # Now properly handle NaN values resulting from the shift operation
            rising_points = window_above_baseline[(window_above_baseline & (~window_above_baseline.shift(1).fillna(False)))].index
            falling_points = window_above_baseline[(~window_above_baseline & (window_above_baseline.shift(1).fillna(False)))].index

            if window_above_baseline.iloc[0]:
                rising_points = [window_start] + list(rising_points)
            if window_above_baseline.iloc[-1]:
                falling_points = list(falling_points) + [window_end]

            for rise, fall in zip(rising_points, falling_points):
                duration = fall - rise
                total_duration_above += duration
                timestamps_above.append((rise, fall))
                print(f"Window from {rise} to {fall} is above baseline, contributing {duration} to the total.")
        
        # Convert total_duration_above from Timedelta to float (hours)
        total_duration_hours = total_duration_above.total_seconds() / 3600

        print(f"Total duration above baseline: {total_duration_above}")
        return total_duration_hours, timestamps_above


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
    
    def calculate_average_eaglei_outage_duration(self):
        #placeholder for the implementation of the general case
        #hurricanes has its own implementation
        pass
