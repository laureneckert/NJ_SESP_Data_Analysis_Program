#Lauren Eckert
#NJSESP Project for Junior Clinic
#Functions for Driver

#libraries
import pandas as pd
import os
from datetime import datetime

#imports from other package files
from hurricanes import Hurricane 
from NOAAEvent import NOAAEvent

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

def find_hurricane_by_name_and_occurrence(hurricanes, storm_name, occurrence):
    for hurricane in hurricanes:
        if hurricane.storm_name == storm_name and hurricane.occurrence == occurrence:
            print(f"Match found for {storm_name} with occurrence {occurrence}")
            return hurricane
    print(f"No match found for {storm_name} with occurrence {occurrence}")
    return None

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

def sampleEagleIEvents(eagle_i_events, max_events_to_print=30):
    # Convert event dates to datetime if they are not already
    for event in eagle_i_events:
        if isinstance(event['run_start_time'], str):
            event['run_start_time'] = pd.to_datetime(event['run_start_time'])

    # Group events by year
    events_by_year = {}
    for event in eagle_i_events:
        year = event['run_start_time'].year
        if year in events_by_year:
            events_by_year[year].append(event)
        else:
            events_by_year[year] = [event]

    # Print a sample of events for each year
    for year, events in events_by_year.items():
        print(f"\nYear: {year} - Total events: {len(events)}")
        # Print only the first few events as a sample
        for event in events[:max_events_to_print]:
            print(event)
        # Print a message if there are more events than the sample printed
        if len(events) > max_events_to_print:
            print(f"... and {len(events) - max_events_to_print} more events.")

def get_unique_noaa_regions(hurricanes):
    unique_regions = set()
    for hurricane in hurricanes:
        for noaa_event in hurricane.noaa_events:
            # Ensure that cz_name_str is a string before stripping
            if isinstance(noaa_event.cz_name_str, str):
                unique_regions.add(noaa_event.cz_name_str.strip())
            else:
                # Handle non-string cz_name_str (convert to string or handle differently)
                unique_regions.add(str(noaa_event.cz_name_str))
    return unique_regions

def count_noaa_events_missing_cz_name(hurricanes):
    count = 0
    for hurricane in hurricanes:
        for event in hurricane.noaa_events:
            # Check if cz_name_str is empty or None
            if not event.cz_name_str or (isinstance(event.cz_name_str, str) and event.cz_name_str.strip() == ""):
                count += 1
    return count

def get_unique_eagle_i_counties(eagle_i_events):
    unique_counties = set()

    for event in eagle_i_events:
        if event['county'] is not None:
            unique_counties.add(event['county'].strip())

    return unique_counties

def print_specific_noaa_events(hurricanes, cz_name_str_values):
    for hurricane in hurricanes:
        for event in hurricane.noaa_events:
            if str(event.cz_name_str) in cz_name_str_values:
                print(f"File: {event.filename}, Line: {event.line_number}, Event ID: {event.event_id}, CZ Name: {event.cz_name_str}")

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

# Mapping of NOAA regions to Eagle I counties
noaa_to_eaglei_mapping = {
    "ATLANTIC CO.": "Atlantic",
    "BERGEN (ZONE)": "Bergen",
    "BERGEN CO.": "Bergen",
    "BURLINGTON CO.": "Burlington",
    "CAMDEN (ZONE)": "Camden",
    "CAMDEN CO.": "Camden",
    "CAPE MAY CO.": "Cape May",
    "CUMBERLAND (ZONE)": "Cumberland",
    "CUMBERLAND CO.": "Cumberland",
    "EASTERN ATLANTIC (ZONE)": "Atlantic",
    "EASTERN BERGEN (ZONE)": "Bergen",
    "EASTERN CAPE MAY (ZONE)": "Cape May",
    "EASTERN ESSEX (ZONE)": "Essex",
    "EASTERN MONMOUTH (ZONE)": "Monmouth",
    "EASTERN OCEAN (ZONE)": "Ocean",
    "EASTERN PASSAIC (ZONE)": "Passaic",
    "EASTERN UNION (ZONE)": "Union",
    "ESSEX (ZONE)": "Essex",
    "ESSEX CO.": "Essex",
    "GLOUCESTER (ZONE)": "Gloucester",
    "GLOUCESTER CO.": "Gloucester",
    "HUDSON (ZONE)": "Hudson",
    "HUDSON CO.": "Hudson",
    "HUNTERDON (ZONE)": "Hunterdon",
    "HUNTERDON CO.": "Hunterdon",
    "MERCER (ZONE)": "Mercer",
    "MERCER CO.": "Mercer",
    "MIDDLESEX (ZONE)": "Middlesex",
    "MIDDLESEX CO.": "Middlesex",
    "MONMOUTH CO.": "Monmouth",
    "MORRIS (ZONE)": "Morris",
    "MORRIS CO.": "Morris",
    "NORTHWESTERN BURLINGTON (ZONE)": "Burlington",
    "OCEAN CO.": "Ocean",
    "PASSAIC CO.": "Passaic",
    "SALEM (ZONE)": "Salem",
    "SALEM CO.": "Salem",
    "SOMERSET (ZONE)": "Somerset",
    "SOMERSET CO.": "Somerset",
    "SOUTHEASTERN BURLINGTON (ZONE)": "Burlington",
    "SUSSEX (ZONE)": "Sussex",
    "SUSSEX CO.": "Sussex",
    "UNION (ZONE)": "Union",
    "UNION CO.": "Union",
    "WARREN (ZONE)": "Warren",
    "WARREN CO.": "Warren",
    "WESTERN ATLANTIC (ZONE)": "Atlantic",
    "WESTERN BERGEN (ZONE)": "Bergen",
    "WESTERN CAPE MAY (ZONE)": "Cape May",
    "WESTERN ESSEX (ZONE)": "Essex",
    "WESTERN MONMOUTH (ZONE)": "Monmouth",
    "WESTERN OCEAN (ZONE)": "Ocean",
    "WESTERN PASSAIC (ZONE)": "Passaic",
    "WESTERN UNION (ZONE)": "Union"
}

def parse_date_time(date_str, time_str):
    # Combine date and time into a single datetime object
    datetime_str = f"{date_str} {time_str}"
    return datetime.strptime(datetime_str, '%m/%d/%Y %H%M')

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

