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
        self.total_duration_eaglei = 0
        self.outage_duration_by_county = {}
        
        self.average_duration_above_baseline = 0.0 #average per threat incident
        #self.outage_duration_by_county = {} #to delete?
        self.timestamps_above_baseline = []

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
        # Print the specified information about the natural hazard
        print(f"Natural Hazard: {self.type_of_hazard}")
        print(f"Percent Customers Affected: {self.percent_customers_affected}%")
        print(f"Total Property Damage: ${self.total_property_damage:,.2f}")
        print(f"Average Time Duration Customers Affected: {self.avg_time_duration_customer_affected} hours")
        print(f"Historical Frequency: {self.historical_frequency}")
        print(f"Future Impact Coefficient: {self.future_impact_coefficient}")

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

    @classmethod
    def create_default_instances(cls):
        """
        Creates a default instance of a subclass of NaturalHazard with initialized attributes.
        The subclass type is dynamically determined based on which subclass calls this method.
        """
        instance = cls()  # Dynamically create an instance of the subclass

        # Initialize attributes inherited from Hazard
        instance.total_property_damage = 0.0
        instance.property_damage_by_county = {}  # Default mapping of county to damage amount
        instance.percent_customers_affected = 0.0
        instance.customers_affected_sum = 0  # Default sum of customers affected
        instance.total_time_duration_customer_affected = 0.0  # Total time duration of customer impact
        instance.avg_time_duration_customer_affected = 0.0  # Average time duration per threat incident
        instance.historical_frequency = 0.0
        instance.future_impact_coefficient = 0.0
        instance.frequency_coefficient = 0.0
        instance.intensity_coefficient = 0.0
        instance.risk_score = 0.0  # Default risk score calculation

        # Attributes specific to NaturalHazard
        instance.NRI_data_fields = {}  # Default NRI data fields
        instance.noaa_events = []  # List of associated NOAA events
        instance.noaa_event_count = 0  # Count of NOAA events
        instance.processed_noaa_windows = []  # List of processed NOAA event windows
        instance.threat_incident_count = 0  # Count of threat incidents
        instance.unique_noaa_regions = set()  # Set of unique NOAA regions
        instance.unique_noaa_event_types = set()  # Set of unique NOAA event types

        instance.total_outages_sum = 0  # Sum of total outages
        instance.outage_total_by_county = {}  # Mapping of county to total outages
        instance.eaglei_events = []  # List of associated Eagle I events
        instance.unique_eaglei_regions = set()  # Set of unique Eagle I regions
        instance.total_duration_eaglei = 0  # Total duration of Eagle I outages
        instance.outage_duration_by_county = {}  # Mapping of county to outage durations
        
        instance.average_duration_above_baseline = 0.0  # Average duration above baseline
        instance.timestamps_above_baseline = []  # List of timestamps above baseline for analysis

        return instance

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
        Prints samples from each data source associated with the hazard, taking into account the new nested dictionary structure.

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

        # Print FEMA NRI Data Samples, adjusted for new structure
        print("\nFEMA NRI Data Samples:")
        for hazard_prefix, counties_data in self.NRI_data_fields.items():
            print(f"\nData for Hazard Prefix: {hazard_prefix}")
            counties_sampled = 0
            for county, data in counties_data.items():
                if counties_sampled >= sample_size:
                    break
                print(f"Sample for {county}:")
                for data_key, data_value in data.items():
                    print(f"  {data_key}: {data_value}")
                counties_sampled += 1
                if counties_sampled < sample_size:
                    print("---")  # Separator if more samples follow

            if len(counties_data) > sample_size:
                print(f"... and data for more counties not shown.")
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
        """
        Calculates the total duration where event data is above the seasonal baseline.

        Parameters:
        - event_windows: List of event window tuples (start, end) for processing.
        - ewma_data: DataFrame containing Exponentially Weighted Moving Average data.
        - seasonal_baseline: DataFrame containing seasonal baseline data.

        Returns:
        - total_duration_hours: The total duration above baseline in hours.
        - timestamps_above: List of tuples with start and end timestamps above baseline.
        """

        # Return 0 duration and an empty list if there are no event windows or data is missing.
        if not event_windows:
            print("No event windows provided for analysis.")
            return 0, []

        if ewma_data.empty or seasonal_baseline.empty:
            print("EWMA data or seasonal baseline is empty.")
            return 0, []

        # Initialize total duration as a Timedelta object and a list for timestamps.
        total_duration_above = pd.Timedelta(0)
        timestamps_above = []
        # Determine the start and end of the EWMA data for comparison.
        ewma_start, ewma_end = ewma_data.index[0], ewma_data.index[-1]

        print("Processing event windows to calculate total time above baseline.")

        for window in event_windows:
            # Convert event window start and end times to datetime objects.
            start, end = pd.to_datetime(window[0]), pd.to_datetime(window[1])

            # Skip windows outside the EWMA data range.
            if start > ewma_end or end < ewma_start:
                print(f"Skipping window from {start} to {end} as it is outside the EWMA data range.")
                continue

            # Adjust window to overlap with EWMA data timeframe.
            window_start = max(start, ewma_start)
            window_end = min(end, ewma_end)

            # Extract EWMA and baseline data for the current window.
            window_ewma = ewma_data[window_start:window_end]
            window_baseline = seasonal_baseline[window_start:window_end]
            # Determine which data points are above the baseline.
            window_above_baseline = window_ewma > window_baseline

            # Continue if no data points are above the baseline.
            if window_above_baseline.empty:
                print("No data points above baseline in this window.")
                continue

            # Identify rising and falling edges of the above-baseline condition.
            rising_points = window_above_baseline[(window_above_baseline & (~window_above_baseline.shift(1).fillna(False)))].index
            falling_points = window_above_baseline[(~window_above_baseline & (window_above_baseline.shift(1).fillna(False)))].index

            # Adjust the first and last points if they are above the baseline.
            if window_above_baseline.iloc[0]:
                rising_points = [window_start] + list(rising_points)
            if window_above_baseline.iloc[-1]:
                falling_points = list(falling_points) + [window_end]

            # Calculate duration for each above-baseline period and accumulate.
            for rise, fall in zip(rising_points, falling_points):
                duration = fall - rise
                total_duration_above += duration
                timestamps_above.append((rise, fall))
                print(f"Window from {rise} to {fall} is above baseline, contributing {duration} to the total.")

        # Convert total_duration_above from Timedelta to float (hours) for easier handling.
        total_duration_hours = total_duration_above.total_seconds() / 3600

        print(f"Total duration above baseline: {total_duration_hours} hours")
        return total_duration_hours, timestamps_above

    def calculate_percent_customers_affected(self):
        # Define the total number of customers in the state
        total_customers_in_state = 4170000 #from task 1

        if total_customers_in_state > 0:
            self.percent_customers_affected = (self.customers_affected_sum / total_customers_in_state) * 100
        else:
            self.percent_customers_affected = 0.0

    def calculate_property_damage(self, hazard_prefix):
        """
        Calculates the total property damage for the hazard, specifically for buildings, 
        by aggregating data across all counties and multiplying the building exposure 
        by the building loss ratio for each county.

        Parameters:
        hazard_prefix (str): The prefix used for the specific natural hazard in FEMA data.

        Returns:
        float: The total property damage for buildings for the hazard statewide.
        """
        property_damage = 0.0

        print(f"\nCalculating property damage for buildings for hazard prefix: {hazard_prefix}...")

        if hazard_prefix not in self.NRI_data_fields:
            print(f"No data available for the hazard prefix: {hazard_prefix}")
            return property_damage

        for county, data in self.NRI_data_fields[hazard_prefix].items():
            # Use the specific attributes for buildings: EXPB for exposure and HLRB for loss ratio
            building_exposure = data.get("EXPB", 0.0)
            building_loss_ratio = data.get("HLRB", 0.0)

            # Calculate property damage for buildings in the current county
            county_property_damage = building_exposure * building_loss_ratio
            property_damage += county_property_damage

            print(f"County: {county}, Building Exposure: {building_exposure}, Building Loss Ratio: {building_loss_ratio}, Incremental Damage: {county_property_damage}")

        self.total_property_damage = property_damage
        print(f"Total property damage for buildings calculated for {hazard_prefix}: {property_damage}")
        return property_damage


    def calculate_probability(self, hazard_prefix):
        """
        Calculates the annualized frequency (probability) of the hazard by averaging
        the annualized frequency of each county. Includes print statements to show calculation progress.

        Parameters:
        hazard_prefix (str): The prefix used for the specific natural hazard in FEMA data.

        Returns:
        float: The average annualized frequency of the hazard across all counties.
        """
        total_frequency = 0.0
        count = 0

        if hazard_prefix not in self.NRI_data_fields:
            print(f"No data available for the hazard prefix: {hazard_prefix}")
            return 0.0

        print(f"Starting frequency calculation for hazard prefix: {hazard_prefix}")
        for county, data in self.NRI_data_fields[hazard_prefix].items():
            if "AFREQ" in data:
                frequency = data["AFREQ"]
                total_frequency += frequency
                count += 1
                print(f"County: {county}, Frequency: {frequency}")

        average_frequency = total_frequency / count if count > 0 else 0.0
        self.historical_frequency=average_frequency
        print(f"Calculated average frequency for {hazard_prefix}: {average_frequency} (based on {count} counties)")
        return average_frequency

    def calculate_average_eaglei_outage_duration(self):
        #placeholder for the implementation of the general case
        #hurricanes has its own implementation
        pass

    def print_nri_data_structure(self):
        print("Inspecting NRI_data_fields structure...")

        if hasattr(self, 'NRI_data_fields') and isinstance(self.NRI_data_fields, dict):
            print("NRI_data_fields is a dictionary.")
            print(f"Top-level keys in NRI_data_fields: {list(self.NRI_data_fields.keys())}")

            for hazard_prefix, data in self.NRI_data_fields.items():
                if isinstance(data, dict):
                    print(f"Structure for hazard prefix '{hazard_prefix}':")
                    print(f"Keys: {list(data.keys())}")
                    first_county_data = next(iter(data.values()), None)
                    if isinstance(first_county_data, dict):
                        print(f"Sample data for the first county under '{hazard_prefix}':")
                        for key, value in first_county_data.items():
                            print(f"{key}: {value}")
                else:
                    print(f"The data for hazard prefix '{hazard_prefix}' is not a dictionary. Actual type: {type(data)}")
                break  # Remove this if you want to print all hazard prefixes
        else:
            print("NRI_data_fields does not exist or is not a dictionary.")

    def calculate_future_impact_coefficient(self):
        """
        Calculates the future impact coefficient by multiplying the frequency coefficient
        by the intensity coefficient. The result is assigned to the future_impact_coefficient attribute.
        Detailed print statements are included to show the calculation progress.
        """
        print("Starting calculation of the Future Impact Coefficient...")
        print(f"Frequency Coefficient: {self.frequency_coefficient}")
        print(f"Intensity Coefficient: {self.intensity_coefficient}")

        # Calculate future impact coefficient
        self.future_impact_coefficient = self.frequency_coefficient * self.intensity_coefficient
        
        print(f"Future Impact Coefficient (Frequency Coefficient * Intensity Coefficient): {self.future_impact_coefficient}")
        
        return self.future_impact_coefficient