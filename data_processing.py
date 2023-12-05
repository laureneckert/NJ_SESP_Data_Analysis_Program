#Lauren Eckert
#NJSESP Project for Junior Clinic
#data_processing.py

#List of functions:
    # create_hurricanes_from_excel(file_path)
    # add_noaa_events_for_hurricane(file_path, hurricane)
    # extract_eagle_i_events(eagle_i_directory)
    # print_data_samples(hurricanes, eagle_i_events, sample_size=5)
    # link_eaglei_to_noaa(hurricanes, eagle_i_events, region_mapping)

#Libraries
import pandas as pd
import os
from datetime import datetime
import pickle

#imports from other package files
from hurricanes import Hurricane 
from NOAAEvent import NOAAEvent
import utilities as uti
from config import config

#Create hurricane objects & add data
def create_hurricanes_from_excel(file_path):
    # Read the Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []  # Return an empty list if there's an error


    # List to hold created Hurricane objects
    hurricane_list = []

    # Iterate over each row in the DataFrame and create Hurricane objects
    for index, row in df.iterrows():
        # Check if the 'End Date' is missing (it will appear as NaT in pandas)
        if pd.isnull(row['End Date']):
            end_date = row['Start Date']  # Set 'End Date' to 'Start Date' if it's missing
        else:
            end_date = row['End Date']

        # Create a Hurricane object
        hurricane = Hurricane(
            year=row['Year'],
            start_date=row['Start Date'],
            end_date=end_date,
            storm_name=row['Storm Name'],
            storm_type=row['Storm Type'],
            comment=row['Comment'],
            occurrence=row['Occurrence']
        )
        hurricane_list.append(hurricane)

    return hurricane_list

#reads excel files for storm data, creates NOAA events, and then adds them to a hurricane
def add_noaa_events_for_hurricane(file_path, hurricane):
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully read NOAA file: {file_path}")
    except Exception as e:
        print(f"Error reading NOAA file {file_path}: {e}")
        return  # Exit the function if there's an error
    
    filename = os.path.basename(file_path)  # Extract filename from the file path

    for index, row in df.iterrows():
        noaa_event = NOAAEvent(
            event_id=row.get('EVENT_ID', None),
            cz_name_str=row.get('CZ_NAME_STR', None),
            begin_location=row.get('BEGIN_LOCATION', None),
            begin_date=row.get('BEGIN_DATE', None),  
            begin_time=row.get('BEGIN_TIME', None),
            event_type=row.get('EVENT_TYPE', None),
            magnitude=row.get('MAGNITUDE', None),
            tor_f_scale=row.get('TOR_F_SCALE', None),
            deaths_direct=row.get('DEATHS_DIRECT', None),
            injuries_direct=row.get('INJURIES_DIRECT', None),
            damage_property_num=row.get('DAMAGE_PROPERTY_NUM', None),  
            damage_crops_num=row.get('DAMAGE_CROPS_NUM', None),
            state_abbr=row.get('STATE_ABBR', None),
            cz_timezone=row.get('CZ_TIMEZONE', None),
            magnitude_type=row.get('MAGNITUDE_TYPE', None),
            episode_id=row.get('EPISODE_ID', None),
            cz_type=row.get('CZ_TYPE', None),
            cz_fips=row.get('CZ_FIPS', None),
            wfo=row.get('WFO', None),
            injuries_indirect=row.get('INJURIES_INDIRECT', None),
            deaths_indirect=row.get('DEATHS_INDIRECT', None),
            source=row.get('SOURCE', None),
            flood_cause=row.get('FLOOD_CAUSE', None),
            tor_length=row.get('TOR_LENGTH', None),
            tor_width=row.get('TOR_WIDTH', None),
            begin_range=row.get('BEGIN_RANGE', None),
            begin_azimuth=row.get('BEGIN_AZIMUTH', None),
            end_range=row.get('END_RANGE', None),
            end_azimuth=row.get('END_AZIMUTH', None),
            end_location=row.get('END_LOCATION', None),
            end_date=row.get('END_DATE', None),
            end_time=row.get('END_TIME', None),
            begin_lat=row.get('BEGIN_LAT', None),
            begin_lon=row.get('BEGIN_LON', None),
            end_lat=row.get('END_LAT', None),
            end_lon=row.get('END_LON', None),
            event_narrative=row.get('EVENT_NARRATIVE', ""),
            episode_narrative=row.get('EPISODE_NARRATIVE', ""),
            absolute_rownumber=row.get('ABSOLUTE_ROWNUMBER', None),
            filename=filename,
            line_number=index + 1  # assuming the CSV has headers
        )
        hurricane.add_noaa_event(noaa_event)
    print(f"Completed adding NOAA events to hurricane {hurricane.storm_name}")

def process_noaa_events(hurricane_list, noaa_directory):
    all_noaa_events = {}

    for filename in os.listdir(noaa_directory):
        if filename.endswith("_storm_data_search_results.csv"):
            print(f"Processing file: {filename}")
            noaa_file_path = os.path.join(noaa_directory, filename)
            
            # Extract storm name and occurrence from filename
            parts = filename.replace("_storm_data_search_results.csv", "").split('_')
            storm_name = parts[0]
            storm_occurrence = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
            
            # Find the corresponding hurricane
            hurricane = next((h for h in hurricane_list if h.storm_name == storm_name and h.occurrence == storm_occurrence), None)
            
            if hurricane:
                add_noaa_events_for_hurricane(noaa_file_path, hurricane)
                all_noaa_events[(hurricane.storm_name, hurricane.occurrence)] = hurricane.noaa_events
    
    return all_noaa_events

def extract_eagle_i_events(eagle_i_directory):
    # Initialize a list to store events outside of the for loop
    events = []

    print(f"Starting to extract Eagle I events from directory: {eagle_i_directory}")
    for year in range(2014, 2023):
        file_path = os.path.join(eagle_i_directory, f"New Jersey {year}.xlsx")
        print(f"Looking for file: {file_path}")
        
        if os.path.exists(file_path):
            print(f"Processing file: {file_path}")
            df = pd.read_excel(file_path)

            # Log the number of rows found
            print(f"Found {len(df)} rows in {file_path}")

            # Iterate through the DataFrame and create a dictionary for each row
            for index, row in df.iterrows():
                event = {
                    'fips_code': row['fips_code'],
                    'county': row['county'],
                    'state': row['state'],
                    'sum': row['sum'],
                    'run_start_time': row['run_start_time']
                }
                events.append(event)
            print(f"Added {len(df)} events from {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    print(f"Extraction complete. {len(events)} total events extracted.")
    return events

def print_data_samples(hurricanes, eagle_i_events, sample_size=5):
    print("Sample Hurricane Data:")
    for hurricane in hurricanes[:sample_size]:
        print(f"Hurricane Name: {hurricane.storm_name}, Year: {hurricane.year}, Occurrence: {hurricane.occurrence}")

    print("\nSample NOAA Event Data:")
    for hurricane in hurricanes[:sample_size]:
        for noaa_event in hurricane.noaa_events[:sample_size]:
            print(f"NOAA Event ID: {noaa_event.event_id}, CZ Name: {noaa_event.cz_name_str}, Begin Date: {noaa_event.begin_date}, Begin Time: {noaa_event.begin_time}")

    print("\nSample Eagle I Event Data:")
    for eaglei_event in eagle_i_events[:sample_size]:
        # Accessing dictionary values using keys
        print(f"Eagle I Event County: {eaglei_event['county']}, Start Time: {eaglei_event['run_start_time']}")

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

def load_or_create_hurricanes(hurricanes_excel_file_path, pickle_directory):
    hurricane_pickle_path = os.path.join(pickle_directory, 'hurricane_objects.pkl')
    if not os.path.exists(hurricane_pickle_path):
        hurricanes = create_hurricanes_from_excel(hurricanes_excel_file_path)
        uti.save_to_pickle(hurricanes, hurricane_pickle_path)
        print("Hurricane objects have been saved to a pickle file.")
    else:
        hurricanes = uti.load_pickle(hurricane_pickle_path)
        print("Hurricane objects have been loaded from the pickle file.")
    return hurricanes

def load_or_add_noaa_events(hurricane_list, noaa_directory, pickle_path):
    # Check if the pickle file exists
    if os.path.exists(pickle_path):
        # Load NOAA events from the pickle file
        with open(pickle_path, 'rb') as f:
            all_noaa_events = pickle.load(f)
        # Update each hurricane object with its corresponding NOAA events
        for hurricane in hurricane_list:
            key = (hurricane.storm_name, hurricane.occurrence)
            if key in all_noaa_events:
                hurricane.noaa_events = all_noaa_events[key]
        print("NOAA events have been loaded from the existing pickle file.")
    else:
        # Process NOAA events and save to a new pickle file
        all_noaa_events = process_noaa_events(hurricane_list, noaa_directory)
        with open(pickle_path, 'wb') as f:
            pickle.dump(all_noaa_events, f)
        print("NOAA events have been processed and saved to a new pickle file.")

def load_or_add_eagle_i_events(eagle_i_directory, pickle_path):
    """
    Loads Eagle I events from a pickle file or processes and adds them if the pickle file does not exist.

    Parameters:
    eagle_i_directory (str): Directory containing Eagle I event Excel files.
    pickle_path (str): Path to the pickle file for storing Eagle I events.
    """
    # Check if the pickle file exists
    if os.path.exists(pickle_path):
        # Load Eagle I events from the pickle file
        with open(pickle_path, 'rb') as f:
            eagle_i_events = pickle.load(f)
        print("Eagle I events have been loaded from the pickle file.")
    else:
        # Process Eagle I events and save to a new pickle file
        eagle_i_events = extract_eagle_i_events(eagle_i_directory)
        with open(pickle_path, 'wb') as f:
            pickle.dump(eagle_i_events, f)
        print("Eagle I events have been processed and saved to a new pickle file.")
    
    return eagle_i_events
 