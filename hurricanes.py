#NJSESP Project
#Lauren Eckert
#Version 2

#Hurricane class
from natural_hazard import NaturalHazard
import utilities as uti
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

class Hurricane(NaturalHazard):
    def __init__(self, type_of_hazard='hurricanes'):
        super().__init__(type_of_hazard)
        self.storm_systems = []  # List to store individual StormSystem objects

    def add_storm_system(self, storm_system):
        self.storm_systems.append(storm_system)

    def print_basic_info(self):
        print(f"Hurricane Hazard Summary:")
        print(f"Type of Hazard: {self.type_of_hazard}")
        print(f"Total Property Damage: {self.total_property_damage}")
        print(f"Total Outages Sum: {self.total_outages_sum}")
        print(f"Risk Score: {self.risk_score}")
        print(f"No. of Associated Storm Systems: {len(self.storm_systems)}")

        # Print sample storm systems
        sample_size = min(5, len(self.storm_systems))  # Adjust sample size as needed
        print(f"\nSample Storm Systems:")
        for i in range(sample_size):
            storm = self.storm_systems[i]
            storm.print_basic_info()  # Call the storm_system's method

    @staticmethod
    def create_default_instances():
        # Create a default instance of Hurricane with default values
        default_hurricane = Hurricane()

        # Initialize inherited attributes from NaturalHazard
        default_hurricane.NRI_data_fields = {}  # Default NRI data fields values
        default_hurricane.noaa_events = []  # Default list of NOAA events
        default_hurricane.noaa_event_count = 0  # Default NOAA event count
        default_hurricane.unique_noaa_regions = set()  # Default set of unique NOAA regions
        default_hurricane.unique_noaa_event_types = set()  # Default set of unique NOAA event types
        default_hurricane.total_outages_sum = 0  # Default total outages sum
        default_hurricane.outage_total_by_county = {}  # Default outage total by county
        default_hurricane.eaglei_events = []  # Default list of Eagle I events
        default_hurricane.unique_eaglei_regions = set()  # Default set of unique Eagle I regions
        default_hurricane.total_duration_eaglei = 0  # Default total duration of Eagle I outages
        default_hurricane.outage_duration_by_county = {}  # Default outage duration by county

        # Initialize inherited attributes from Hazard
        default_hurricane.total_property_damage = 0.0  # Default total property damage
        default_hurricane.property_damage_by_county = {}  # Default property damage by county
        default_hurricane.total_property_damage_annualized = 0.0  # Default annualized property damage
        default_hurricane.percent_customers_affected = 0.0  # Default percent customers affected
        default_hurricane.customers_affected_sum = 0  # Default sum of customers affected
        default_hurricane.total_time_duration_customer_affected = 0.0  # Default total time duration of customers affected
        default_hurricane.time_duration_customer_affected_annualized = 0.0  # Default annualized time duration of customers affected
        default_hurricane.historical_frequency = 0.0  # Default historical frequency
        default_hurricane.future_impact_coefficient = 0.0  # Default future impact coefficient
        default_hurricane.frequency_coefficient = 0.0  # Default frequency coefficient
        default_hurricane.impact_coefficient = 0.0  # Default impact coefficient
        default_hurricane.risk_score = 0.0  # Default risk score

        # Add other default values as required

        return default_hurricane
    
    def calculate_average_peak_outages(self):
        total_peak_outages = 0
        if not self.storm_systems:
            print("No storm systems available.")
            self.customers_affected_sum = 0
            return

        print(f"Calculating peak outages for {len(self.storm_systems)} storm systems...")
        for storm_system in self.storm_systems:
            storm_outages = storm_system.calculate_peak_outages(self.eaglei_events)
            print(f"Total peak outages for {storm_system.storm_name}: {storm_outages}")
            total_peak_outages += storm_outages

        self.customers_affected_sum = total_peak_outages / len(self.storm_systems)
        print(f"Average Peak Outages: {self.customers_affected_sum}")

    def calculate_regression_coefficients(self):
        # Preparing data for Frequency Coefficient
        year_frequency = {}
        year_intensity_sum = {}
        year_intensity_count = {}

        for storm in self.storm_systems:
            year = storm.start_date.year
            year_frequency[year] = year_frequency.get(year, 0) + 1
            year_intensity_sum[year] = year_intensity_sum.get(year, 0) + storm.intensity
            year_intensity_count[year] = year_intensity_count.get(year, 0) + 1

        years = [] #fix logic for averaging intensity by year, its not necessary to average by year just plot the intensities and then get the line from that
        frequencies = []
        average_intensities = []

        for year in year_frequency:
            years.append(year)
            frequencies.append(year_frequency[year])

            if year_intensity_count[year] > 0:
                average_intensity = year_intensity_sum[year] / year_intensity_count[year]
                average_intensities.append(average_intensity)
            else:
                # Handle years with no storm systems
                print(f"No storm systems recorded for the year {year}")
                average_intensities.append(0)  # Or choose to handle this differently

        # Linear Regression for Frequency
        if years:
            slope_freq, intercept, r_value, p_value, std_err = stats.linregress(years, frequencies)
            self.frequency_coefficient = slope_freq + 1

            # Plotting Frequency
            plt.figure(figsize=(10, 5))
            plt.scatter(years, frequencies, color='blue')
            plt.plot(years, intercept + slope_freq * np.array(years), 'r')
            plt.title('Storm Frequency Over Time')
            plt.xlabel('Year')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.show()
        else:
            print("No data available for frequency analysis.")

        # Linear Regression for Average Intensity
        if years:
            slope_intensity, intercept, r_value, p_value, std_err = stats.linregress(years, average_intensities)
            self.intensity_coefficient = slope_intensity + 1

            # Plotting Intensity
            plt.figure(figsize=(10, 5))
            plt.scatter(years, average_intensities, color='green')
            plt.plot(years, intercept + slope_intensity * np.array(years), 'r')
            plt.title('Average Storm Intensity Over Time')
            plt.xlabel('Year')
            plt.ylabel('Average Intensity')
            plt.grid(True)
            plt.show()
        else:
            print("No data available for intensity analysis.")

        return self.frequency_coefficient, self.intensity_coefficient
    
    def analyze_hurricane_data(self): #needs to be refactored for all natural hazards
        hazard_prefix = "HRCN"
        total_property_damage = self.calculate_property_damage(hazard_prefix)
        annualized_frequency = self.calculate_probability(hazard_prefix)

        print(f"Total Property Damage for Hurricanes: {total_property_damage}")
        print(f"Annualized Frequency (Probability) of Hurricanes: {annualized_frequency}")

    def calculate_statistics(self, noaa_to_eaglei_mapping):
        # Specific implementation for hurricanes
        # Implement hurricane-specific behavior here
        pass

    def calculate_scores(self):
        # Specific implementation for hurricanes
        # Implement hurricane-specific behavior here
        pass

    def calculate_risk(self):
        # Specific implementation for hurricanes
        # Implement hurricane-specific risk calculation here
        pass

    def print_basic_info(self):
        # Specific implementation for hurricanes
        print(f"Hurricane Hazard Summary:")
        print(f"Type of Hazard: {self.type_of_hazard}")
        # Include more specific details as needed

    def link_processed_noaa_events_to_storm_systems(self):
        """
        Links processed NOAA event windows to the relevant storm systems in the hurricane.
        Uses the processed_noaa_windows class attribute directly.
        """
        print("Linking processed NOAA event windows to storm systems.")
        for storm_system in self.storm_systems:

            storm_system_noaa_event_windows = [
                window for window in self.processed_noaa_windows
                if not (pd.to_datetime(window[1]) <= storm_system.start_date or 
                        pd.to_datetime(window[0]) >= storm_system.end_date)
            ]
            storm_system.processed_noaa_event_windows = storm_system_noaa_event_windows
            print(f"Linked {len(storm_system_noaa_event_windows)} windows to storm system {storm_system.storm_name}.")

    def link_and_print_summary(self):
        print("Linking processed NOAA event windows to storm systems.")
        self.link_processed_noaa_events_to_storm_systems()
        
        print("Printing summary for each linked storm system.")
        for storm_system in self.storm_systems:
            storm_system.print_linked_noaa_event_summary()

    def identify_unlinked_noaa_windows(self, return_unlinked=True):
        """
        Identifies any NOAA event windows that were not linked to any storm system.
        """
        linked_windows = set()
        for storm_system in self.storm_systems:
            for window in storm_system.processed_noaa_event_windows:
                # Ensure window has at least three elements before accessing the third
                if len(window) >= 3:
                    linked_windows.add((window[0], window[1], tuple(window[2])))
                else:
                    # Handle the case where window does not have a third element
                    linked_windows.add((window[0], window[1]))

        all_windows = set()
        for window in self.processed_noaa_windows:
            # Similar check as above
            if len(window) >= 3:
                all_windows.add((window[0], window[1], tuple(window[2])))
            else:
                all_windows.add((window[0], window[1]))

        unlinked_windows = all_windows - linked_windows

        if unlinked_windows:
            print("Unlinked NOAA Event Windows:")
            for window in sorted(list(unlinked_windows)):
                print(f"Window: {window[0]} to {window[1]}", end="")
                if len(window) > 2:
                    print(f", Source Files: {window[2]}")
                else:
                    print()  # Newline for windows without a third element
        else:
            print("All NOAA event windows are linked to storm systems.")

        if return_unlinked:
            return list(unlinked_windows)

    def find_storm_system_by_name_and_occurrence(self, storm_name, occurrence=1):
        """
        Finds a storm system by its name and occurrence.

        Parameters:
        storm_name (str): The name of the storm.
        occurrence (int): The occurrence of the storm (default is 1).

        Returns:
        StormSystem or None: The found StormSystem object or None if not found.
        """
        for system in self.storm_systems:
            if system.storm_name == storm_name and system.occurrence == occurrence:
                return system
        return None
    
    def link_unlinked_noaa_windows(self):
        """
        Links unlinked NOAA event windows to storm systems based on filenames.
        """
        unlinked_windows = self.identify_unlinked_noaa_windows(return_unlinked=True)  # Adjust the method to return unlinked windows
        for start_time, end_time, filenames in unlinked_windows:
            for filename in filenames:
                # Strip off the known constant part of the filename
                core_filename = filename.replace('_storm_data_search_results.csv', '')
                # Split by underscores
                parts = core_filename.split('_')
                # If the last part is a digit, it's an occurrence, else default to 1
                if parts[-1].isdigit():
                    occurrence = int(parts[-1])
                    storm_name = '_'.join(parts[:-1])  # Join all but the last part for the name
                else:
                    occurrence = 1
                    storm_name = core_filename  # The core filename is the storm name

                storm_system = self.find_storm_system_by_name_and_occurrence(storm_name, occurrence)
                if storm_system:
                    storm_system.processed_noaa_event_windows.append((start_time, end_time, {filename}))
                    print(f"Linked window from {start_time} to {end_time}, from file {filename}, to storm system {storm_name} (Occurrence: {occurrence}).")
                else:
                    print(f"No matching storm system found for {storm_name} (Occurrence: {occurrence}) from file {filename}.")

    def calculate_average_eaglei_outage_duration(self):
        print("Starting calculation of average Eagle I outage duration above baseline for Hurricanes.")
        threshold_date = pd.to_datetime("2014-11-01 04:00:00")
        total_duration = 0.0  # Initialize as float
        count = 0

        for storm_system in self.storm_systems:
            print(f"\nProcessing Storm System: {storm_system.storm_name}, Start Date: {storm_system.start_date}")
            if storm_system.start_date > threshold_date:
                print(f"Storm system {storm_system.storm_name} is after the threshold date {threshold_date} and will be included.")
                # Directly use the duration as it's already a float
                duration_hours = storm_system.outages_above_baseline_duration
                print(f"Including duration: {duration_hours} hours for {storm_system.storm_name}")
                total_duration += duration_hours
                count += 1
                for window in storm_system.outages_above_baseline_timestamps:
                    print(f"Included window timestamps: Start: {window[0]}, End: {window[1]}")
            else:
                print(f"Storm system {storm_system.storm_name} is before the threshold date {threshold_date} and will not be included.")

        if count > 0:
            average_duration = total_duration / count
            print(f"\nCalculated average duration: {average_duration} hours over {count} storm systems.")
        else:
            average_duration = 0.0
            print("\nNo storm systems with calculated durations found after the threshold date. Setting average duration to 0.")

        self.average_duration_above_baseline = average_duration
        print(f"\nAverage Eagle I Outage Duration Above Baseline for Hurricanes (after threshold date): {average_duration} hours")
        return average_duration

