# Lauren Eckert
# NJSESP Project for Junior Clinic

# Driver class

import pandas as pd
import os
import pickle
from datetime import datetime

from hurricanes import Hurricane 
from NOAAEvent import NOAAEvent
import driverFunctions as df
from driverFunctions import noaa_to_eaglei_mapping


# File paths
hurricanes_excel_file_path = r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\excelInfo\hurricanes.xlsx"
pickle_directory = r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles"

# Ensure the pickle directory exists
if not os.path.exists(pickle_directory):
    os.makedirs(pickle_directory)

# Load or create hurricane objects
hurricane_pickle_path = os.path.join(pickle_directory, 'hurricane_objects.pkl')
if not os.path.exists(hurricane_pickle_path):
    hurricanes = df.create_hurricanes_from_excel(hurricanes_excel_file_path)
    with open(hurricane_pickle_path, 'wb') as f:
        pickle.dump(hurricanes, f)
    print("Hurricane objects have been saved to a pickle file.")
else:
    with open(hurricane_pickle_path, 'rb') as f:
        hurricanes = pickle.load(f)
    print("Hurricane objects have been loaded from the pickle file.")

# Process NOAA events
noaa_files_directory = r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\excelInfo\storm info"
noaa_pickle_path = os.path.join(pickle_directory, 'all_noaa_events.pkl')

if not os.path.exists(noaa_pickle_path):
    all_noaa_events = {}
    for filename in os.listdir(noaa_files_directory):
        if filename.endswith("_storm_data_search_results.csv"):
            print(f"Processing file: {filename}")
            noaa_file_path = os.path.join(noaa_files_directory, filename)
            parts = filename.replace("_storm_data_search_results.csv", "").split('_')
            storm_name = parts[0]
            storm_occurrence = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
            hurricane = df.find_hurricane_by_name_and_occurrence(hurricanes, storm_name, storm_occurrence)
            if hurricane:
                df.add_noaa_events_for_hurricane(noaa_file_path, hurricane)
                all_noaa_events[(hurricane.storm_name, hurricane.occurrence)] = hurricane.noaa_events
    with open(noaa_pickle_path, 'wb') as f:
        pickle.dump(all_noaa_events, f)
    print("All NOAA events have been saved to a pickle file.")
else:
    with open(noaa_pickle_path, 'rb') as f:
        all_noaa_events = pickle.load(f)
    for hurricane in hurricanes:
        key = (hurricane.storm_name, hurricane.occurrence)
        if key in all_noaa_events:
            hurricane.noaa_events = all_noaa_events[key]
    print("All NOAA events have been loaded from the pickle file.")

# Add Eagle I events
eagle_i_directory = r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\excelInfo\eaglei_outages"
eagle_i_pickle_path = os.path.join(pickle_directory, 'eagle_i_events.pkl')

if not os.path.exists(eagle_i_pickle_path):
    eagle_i_events = df.extract_eagle_i_events(eagle_i_directory)
    with open(eagle_i_pickle_path, 'wb') as f:
        pickle.dump(eagle_i_events, f)
    print("Eagle I events have been saved to a pickle file.")
else:
    with open(eagle_i_pickle_path, 'rb') as f:
        eagle_i_events = pickle.load(f)
    print("Eagle I events have been loaded from the pickle file.")

# Call the function with your data
df.print_data_samples(hurricanes, eagle_i_events)

# Call the link_eaglei_to_noaa function with the region mapping
df.link_eaglei_to_noaa(hurricanes, eagle_i_events, noaa_to_eaglei_mapping)

# Path to the hurricane objects pickle file
hurricane_pickle_path = r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\hurricane_objects.pkl"

# Open the file in write-binary mode and overwrite with updated hurricane objects
with open(hurricane_pickle_path, 'wb') as f:
    pickle.dump(hurricanes, f)

print("Updated hurricane objects have been saved back to the pickle file.")
