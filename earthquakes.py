#NJSESP Project
#Lauren Eckert
#Version 2

#Earthquakes class
from natural_hazard import NaturalHazard
from FEMA_NRI_data import FEMA_NRI_data
from USGSEvent import USGSEvent
import utilities as uti
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

class Earthquakes(NaturalHazard):
    def __init__(self, type_of_hazard='earthquakes'):
        super().__init__(type_of_hazard)

    def calculate_average_eaglei_outage_duration(self, ewma_data, seasonal_baseline, USGSEvents):
        print(f"Starting calculation of average Eagle I outage duration above baseline for {self.type_of_hazard}.")
        threshold_date = pd.to_datetime("2014-11-01 04:00:00")  # Placeholder date; adjust as needed
        
        usgs_windows = []  # Initialize the list to store the windows
        for event in USGSEvents:
            if hasattr(event, 'usgs_window'):
                print(f"Adding {event.usgs_window} to list of windows to evaluate.")
                usgs_windows.append(event.usgs_window)
        
        # Filter windows that are after the threshold date
        relevant_windows = [(window[0], window[1]) for window in usgs_windows if window[0] > threshold_date]
        print(f"Filtered {len(relevant_windows)} out of {len(usgs_windows)} USGS Earthquake windows after threshold date for processing.")

        # Calculate duration above baseline for all relevant windows in one go
        if relevant_windows:
            total_duration, all_timestamps_above = self.calculate_duration_above_baseline_for_windows(
                relevant_windows, ewma_data, seasonal_baseline)
            count = len(relevant_windows)  # Number of windows considered
            average_duration = total_duration / count if count else 0.0
        else:
            total_duration, all_timestamps_above = 0.0, []
            average_duration = 0.0
            print("\nNo relevant USGS Earthquake windows found after the threshold date. Setting average duration to 0.")

        # Assign calculated values to the instance attributes
        self.outages_above_baseline_timestamps = all_timestamps_above  # Timestamps for periods above baseline
        
        self.average_duration_above_baseline = average_duration  # Attribute for average duration
        self.total_time_duration_customer_affected = total_duration  # Total duration across all events
        self.avg_time_duration_customer_affected = average_duration  # Average duration per event

        print(f"\nAverage Eagle I Outage Duration Above Baseline for {self.type_of_hazard} (after threshold date): {average_duration} hours")
        return average_duration
