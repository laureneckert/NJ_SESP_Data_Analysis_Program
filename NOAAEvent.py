#NJSESP Project
#Lauren Eckert
#Version 2

#NOAA events class

import pandas as pd
import os
import csv
import re
import glob
from njsesp_config import config
from DataSource import DataSource

class NOAAEvent(DataSource):
    def __init__(self, event_id, cz_name_str, begin_location, begin_date, begin_time, event_type, magnitude, tor_f_scale, deaths_direct,
                 injuries_direct, damage_property_num, damage_crops_num, state_abbr, cz_timezone, magnitude_type, episode_id, cz_type,
                 cz_fips, wfo, injuries_indirect, deaths_indirect, source, flood_cause, tor_length, tor_width, begin_range, begin_azimuth,
                 end_range, end_azimuth, end_location, end_date, end_time, begin_lat, begin_lon, end_lat, end_lon, event_narrative, episode_narrative, absolute_rownumber, weather_event_type, filename=None, line_number=None):
        super().__init__()  # Initialize parent DataSource class        
        self.event_id = event_id
        self.cz_name_str = cz_name_str
        self.begin_location = begin_location
        self.begin_date = begin_date
        self.begin_time = begin_time
        self.event_type = event_type
        self.magnitude = magnitude
        self.tor_f_scale = tor_f_scale
        self.deaths_direct = deaths_direct
        self.injuries_direct = injuries_direct
        self.damage_property_num = damage_property_num
        self.damage_crops_num = damage_crops_num
        self.state_abbr = state_abbr
        self.cz_timezone = cz_timezone
        self.magnitude_type = magnitude_type
        self.episode_id = episode_id
        self.cz_type = cz_type
        self.cz_fips = cz_fips
        self.wfo = wfo
        self.injuries_indirect = injuries_indirect
        self.deaths_indirect = deaths_indirect
        self.source = source
        self.flood_cause = flood_cause
        self.tor_length = tor_length
        self.tor_width = tor_width
        self.begin_range = begin_range
        self.begin_azimuth = begin_azimuth
        self.end_range = end_range
        self.end_azimuth = end_azimuth
        self.end_location = end_location
        self.end_date = end_date
        self.end_time = end_time
        self.begin_lat = begin_lat
        self.begin_lon = begin_lon
        self.end_lat = end_lat
        self.end_lon = end_lon
        self.event_narrative = event_narrative
        self.episode_narrative = episode_narrative
        self.absolute_rownumber = absolute_rownumber
        self.weather_event_type = weather_event_type
        self.filename = filename
        self.line_number = line_number       

    def clean_csv_file(source_file_path, output_file_path): #does not work dont use
        """
        Cleans specific fields in a CSV file to handle problematic characters, with verbose output.

        Parameters:
        source_file_path (str): Path to the source CSV file.
        output_file_path (str): Path to save the cleaned CSV file.
        """
        print(f"Opening source file for cleaning: {source_file_path}")
        with open(source_file_path, mode='r', newline='', encoding='utf-8') as infile, open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                # Clean EPISODE_NARRATIVE
                episode_narrative_original = row.get('EPISODE_NARRATIVE', '')
                episode_narrative_cleaned = episode_narrative_original.replace('\n', ' ').replace('\r', ' ').replace('"', "'")
                row['EPISODE_NARRATIVE'] = episode_narrative_cleaned

                # Clean SOURCE
                source_original = row.get('SOURCE', '')
                source_cleaned = source_original.replace(',', ';')
                row['SOURCE'] = source_cleaned

                # Print what's being cleaned
                if episode_narrative_original != episode_narrative_cleaned:
                    print(f"Cleaned EPISODE_NARRATIVE: \"{episode_narrative_original[:50]}...\" to \"{episode_narrative_cleaned[:50]}...\"")
                if source_original != source_cleaned:
                    print(f"Cleaned SOURCE: \"{source_original}\" to \"{source_cleaned}\"")

                writer.writerow(row)

        print(f"Cleaning complete. File saved to: {output_file_path}")

    @staticmethod
    def clean_noaa_data(): #file handling works but the cleaning method doesnt so cant use
        
        """
        Cleans CSV files in each uncleaned data directory for NOAA hazards and saves them into the corresponding cleaned data directory
        with the prefix 'cleaned_' added to each filename.
        """
        print("Starting cleaning and sorting NOAA data.")

        base_uncleaned_path = config['data_paths']['noaa']['base_uncleaned_data_directory']
        base_cleaned_path = config['data_paths']['noaa']['base_cleaned_data_directory']

        if not os.path.isdir(base_uncleaned_path):
            print(f"Base uncleaned data directory does not exist: {base_uncleaned_path}")
            return

        # Loop through each hazard type directory within the base uncleaned directory
        for hazard_folder in os.listdir(base_uncleaned_path):
            hazard_uncleaned_path = os.path.join(base_uncleaned_path, hazard_folder)
            if not os.path.isdir(hazard_uncleaned_path):
                continue  # Skip if it's not a directory

            print(f"Processing uncleaned NOAA data for {hazard_folder}...")

            csv_files = glob.glob(os.path.join(hazard_uncleaned_path, '*.csv'))
            if not csv_files:
                print(f"No CSV files found for {hazard_folder}.")
                continue

            # Ensure the cleaned data folder exists
            cleaned_hazard_path = os.path.join(base_cleaned_path, hazard_folder)
            if not os.path.exists(cleaned_hazard_path):
                os.makedirs(cleaned_hazard_path)

            for csv_file in csv_files:
                try:
                    filename = os.path.basename(csv_file)
                    cleaned_filename = "cleaned_" + filename
                    cleaned_file_path = os.path.join(cleaned_hazard_path, cleaned_filename)

                    # Clean the CSV and write to the corresponding hazard's cleaned data directory
                    NOAAEvent.clean_csv_file(csv_file, cleaned_file_path)
                    print(f"Cleaned and saved {cleaned_filename} for {hazard_folder}.")
                except Exception as e:
                    print(f"Failed to clean {filename} for {hazard_folder}: {e}")

        print("Completed cleaning and sorting NOAA data.")

    def extract_data(directory_path):
        """
        Reads NOAA event data from CSV files in a directory and creates NOAAEvent objects.

        Parameters:
        directory_path (str): Path to the directory containing NOAA event CSV files.

        Returns:
        list: A list of NOAAEvent objects created from the file data.
        """
        noaa_events = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and file_path.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path)
                    print(f"Successfully read NOAA file: {file_path}")

                    for index, row in df.iterrows():
  
                        event = NOAAEvent(
                            event_id=row.get('EVENT_ID', None),
                            cz_name_str=row.get('CZ_NAME_STR', None),
                            begin_location=row.get('BEGIN_LOCATION', None),
                            begin_date=row.get('BEGIN_DATE', None),  
                            begin_time=row.get('BEGIN_TIME', None),  # Keep as separate fields
                            end_date=row.get('END_DATE', None),
                            end_time=row.get('END_TIME', None),     # Keep as separate fields
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
                            begin_lat=row.get('BEGIN_LAT', None),
                            begin_lon=row.get('BEGIN_LON', None),
                            end_lat=row.get('END_LAT', None),
                            end_lon=row.get('END_LON', None),
                            event_narrative=row.get('EVENT_NARRATIVE', ""),
                            episode_narrative=row.get('EPISODE_NARRATIVE', ""),
                            absolute_rownumber=row.get('ABSOLUTE_ROWNUMBER', None),
                            weather_event_type=os.path.basename(directory_path),
                            filename=os.path.basename(file_path),
                            line_number=index + 1
                        )
                        noaa_events.append(event)
                except Exception as e:
                    print(f"Error reading NOAA file {file_path}: {e}")
                    continue  # Skip to the next file in case of an error
        
        print(f"Extracted {len(noaa_events)} NOAA events from the directory")
        return noaa_events

    @staticmethod
    def assign_and_link_noaa_events_to_hazard(noaa_event_groups):
        """
        Assigns and links NOAA events to their corresponding hazards based on a mapping.
        """
        for hazard_type, events in noaa_event_groups.items():
            hazard = events['hazard']

            print(f"Assigning NOAA events to {hazard.type_of_hazard}...")
            count = 0  # Counter to track the number of successfully processed events
            for event in events['events']:
                try:
                    hazard.add_noaa_event(event)
                    count += 1  # Increment counter upon successful addition
                except Exception as e:
                    print(f"Error in processing NOAA event for {hazard.type_of_hazard}: {e}")
                    continue  # Proceed with the next event

            # Print success message after processing all events for a hazard
            print(f"Successfully assigned {count} NOAA events to {hazard.type_of_hazard}.")
            """
            try:
                # Update hazard data
                pickle_path = config['pickle_paths'][hazard.type_of_hazard.lower()]
                uti.save_to_pickle(hazard, pickle_path)
                print(f"{hazard.type_of_hazard} data successfully updated and saved.")
            except Exception as e:
                print(f"Error in saving updated data for {hazard.type_of_hazard}: {e}")
            """
        print("NOAA events assignment and linking process completed.")

    @staticmethod
    def get_unique_noaa_regions(hazards):
        """
        Returns unique regions from a list of hazards.

        Parameters:
        hazards: List of hazard objects.

        Returns:
        Set of unique regions extracted from NOAA events of the hazards.
        """
        unique_regions = set()
        for hazard in hazards:
            for event in hazard.noaa_events:
                # Check if cz_name_str is a string and add to the set
                if isinstance(event.cz_name_str, str):
                    unique_regions.add(event.cz_name_str.strip())
                else:
                    unique_regions.add(str(event.cz_name_str))
        return unique_regions

    @staticmethod
    def count_noaa_events_missing_cz_name(hazards): #useful for finding the weird bug that occasionally appears in NOAA data source
        """
        Counts NOAA events with missing 'cz_name_str' in a list of hazards.

        Parameters:
        hazards: List of hazard objects.

        Returns:
        Count of NOAA events missing 'cz_name_str'.
        """
        count = 0
        for hazard in hazards:
            for event in hazard.noaa_events:
                if not event.cz_name_str or event.cz_name_str.strip() == "":
                    count += 1
        return count

    @staticmethod
    def print_specific_noaa_events(hazards, cz_name_str_values):
        """
        Prints specific NOAA events based on provided CZ Name values.

        Parameters:
        hazards: List of hazard objects.
        cz_name_str_values: List of CZ Name values to filter the NOAA events.

        Returns:
        None
        """
        for hazard in hazards:
            for event in hazard.noaa_events:
                if str(event.cz_name_str) in cz_name_str_values:
                    print(f"File: {event.filename}, Line: {event.line_number}, Event ID: {event.event_id}, CZ Name: {event.cz_name_str}")

    @staticmethod
    def print_samples(noaa_events, sample_size=15):
        print("\nSample NOAA Event Data:")
        for event in noaa_events[:sample_size]:
            print(f"Event ID: {event.event_id}, Type: {event.weather_event_type}, Date: {event.begin_date} {event.begin_time} to {event.end_date} {event.end_time}, Location: {event.begin_location}")