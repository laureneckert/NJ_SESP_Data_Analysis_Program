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

    def print_basic_hurricane_info(self):
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
    
    def calculate_average_peak_outages(self):
        total_peak_outages = 0
        valid_storm_count = 0  # Counter for storm systems after the threshold date
        threshold_date = pd.to_datetime("2014-11-01 04:00:00")  # Define the threshold date

        if not self.storm_systems:
            print("No storm systems available.")
            self.customers_affected_sum = 0
            return

        print(f"Calculating peak outages for storm systems after {threshold_date}...")
        for storm_system in self.storm_systems:
            # Only process storm systems that start after the threshold date
            if pd.to_datetime(storm_system.start_date) > threshold_date:
                storm_outages = storm_system.calculate_peak_outages(self.eaglei_events)
                print(f"Total peak outages for {storm_system.storm_name} (after threshold): {storm_outages}")
                total_peak_outages += storm_outages
                valid_storm_count += 1  # Only increment for valid storm systems

        # Prevent division by zero if no valid storm systems were found
        if valid_storm_count > 0:
            self.customers_affected_sum = total_peak_outages / valid_storm_count
            print(f"Average Peak Outages (after threshold): {self.customers_affected_sum}")
        else:
            self.customers_affected_sum = 0
            print("No storm systems found after the threshold date. Average Peak Outages set to 0.")

    def calculate_regression_coefficients(self):
        # Preparing data for Frequency Coefficient
        year_frequency = {}
        intensities = []  # Directly store intensities of each storm
        years = []  # Store years of each storm for intensity calculation

        for storm in self.storm_systems:
            year = storm.start_date.year
            years.append(year)  # Append year for every storm
            intensities.append(storm.intensity)  # Directly append storm intensity
            year_frequency[year] = year_frequency.get(year, 0) + 1

        frequencies = list(year_frequency.values())
        unique_years = list(year_frequency.keys())  # Unique years for frequency calculation

        # Linear Regression for Frequency
        if unique_years:
            slope_freq, intercept, r_value, p_value, std_err = stats.linregress(unique_years, frequencies)
            frequency_coefficient = slope_freq + 1

            # Plotting Frequency
            plt.figure(figsize=(10, 5))
            plt.scatter(unique_years, frequencies, color='blue')
            plt.plot(unique_years, intercept + slope_freq * np.array(unique_years), 'r')
            plt.title('Storm Frequency Over Time')
            plt.xlabel('Year')
            plt.ylabel('Frequency')
            plt.grid(True)
            #plt.show()
        else:
            print("No data available for frequency analysis.")
            frequency_coefficient = None

        # Linear Regression for Intensity
        if years:
            slope_intensity, intercept, r_value, p_value, std_err = stats.linregress(years, intensities)
            intensity_coefficient = slope_intensity + 1

            # Plotting Intensity
            plt.figure(figsize=(10, 5))
            plt.scatter(years, intensities, color='green')
            plt.plot(years, intercept + slope_intensity * np.array(years), 'r')
            plt.title('Storm Intensity Over Time')
            plt.xlabel('Year')
            plt.ylabel('Intensity')
            plt.grid(True)
            #plt.show()
        else:
            print("No data available for intensity analysis.")
            intensity_coefficient = None
        self.frequency_coefficient, self.intensity_coefficient = frequency_coefficient, intensity_coefficient
        return frequency_coefficient, intensity_coefficient
        
    """
    def analyze_hurricane_data(self): #needs to be refactored for all natural hazards
        hazard_prefix = "HRCN"
        print(f"Hello! Starting analysis of hurricane data with prefix: {hazard_prefix}")
        # Debug print to check NRI_data_fields contents
        print(f"NRI_data_fields available: {hasattr(self, 'NRI_data_fields') and bool(self.NRI_data_fields)}")
        if hasattr(self, 'NRI_data_fields'):
            print(f"Sample NRI_data_fields content: {next(iter(self.NRI_data_fields.items()), ('No Data', 'N/A'))}")
        try:
            total_property_damage = self.calculate_property_damage(hazard_prefix)
            annualized_frequency = self.calculate_probability(hazard_prefix)
        except Exception as e:
            print(f"Error during hurricane data analysis: {e}")
            total_property_damage = 0
            annualized_frequency = 0

        print(f"Total Property Damage for Hurricanes: {total_property_damage}")
        print(f"Annualized Frequency (Probability) of Hurricanes: {annualized_frequency}")
    """
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

        self.average_duration_above_baseline = average_duration #attribute in natural hazards
        self.total_time_duration_customer_affected = total_duration #attribute in hazards
        self.avg_time_duration_customer_affected = average_duration #attribute in hazards

        print(f"\nAverage Eagle I Outage Duration Above Baseline for Hurricanes (after threshold date): {average_duration} hours")
        return average_duration

