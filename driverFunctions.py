#Lauren Eckert
#NJSESP Project for Junior Clinic
#Functions for Driver

#libraries
import pandas as pd
import os
from datetime import datetime
import pickle

#imports from other package files
from hurricanes import Hurricane 
from NOAAEvent import NOAAEvent


def link_eaglei_to_noaa(hurricanes, eagle_i_events, region_mapping):
    for hurricane in hurricanes:
        print(f"Processing Hurricane: {hurricane.storm_name}, Year: {hurricane.year}, Occurrence: {hurricane.occurrence}")
        for noaa_event in hurricane.noaa_events:
            # Convert NOAA event region to Eagle I event region
            noaa_region = region_mapping.get(noaa_event.cz_name_str, None)
            if noaa_region:
                for eagle_i_event in eagle_i_events:
                    # Check if the region and time frame match
                    if eagle_i_event['county'] == noaa_region:
                        # Pad begin and end times with zeros to ensure correct format
                        begin_time_padded = f"{noaa_event.begin_time:04d}"
                        end_time_padded = f"{noaa_event.end_time:04d}"

                        noaa_event_start_time = datetime.strptime(f"{noaa_event.begin_date} {begin_time_padded}", '%m/%d/%Y %H%M')
                        noaa_event_end_time = datetime.strptime(f"{noaa_event.end_date} {end_time_padded}", '%m/%d/%Y %H%M')

                        # Convert run_start_time to datetime if it's a string, otherwise use it directly
                        if isinstance(eagle_i_event['run_start_time'], str):
                            eagle_i_event_time = datetime.strptime(eagle_i_event['run_start_time'], '%Y-%m-%d %H:%M:%S')
                        else:
                            eagle_i_event_time = eagle_i_event['run_start_time']

                        # Check if Eagle I event time falls within the NOAA event time frame
                        if noaa_event_start_time <= eagle_i_event_time <= noaa_event_end_time:
                            hurricane.add_eaglei_event(eagle_i_event)
                            print(f"Added Eagle I event from {eagle_i_event['county']} on {eagle_i_event['run_start_time']} to Hurricane {hurricane.storm_name}")
            #else:
                #print(f"No matching region found for NOAA Event ID: {noaa_event.event_id} in Hurricane {hurricane.storm_name}")

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

# Example usage
# save_to_pickle(hurricanes, 'path_to_your_pickle_file.pkl')
