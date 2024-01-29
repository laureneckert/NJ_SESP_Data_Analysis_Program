#NJSESP Project
#Lauren Eckert
#Version 2

import pandas as pd
from datetime import datetime
from collections import defaultdict
import os
from DataSource import DataSource
import utilities as uti
import njsesp_config as config

class EagleIEvent(DataSource):
    def __init__(self, fips_code, county, state, sum, run_start_time):
        super().__init__()  # Initialize parent DataSource class
        self.fips_code = fips_code
        self.county = county
        self.state = state
        self.sum = sum
        self.run_start_time = run_start_time

    def extract_data(eagle_i_directory):
        """
        Extracts Eagle I events from a given Excel file.

        Parameters:
        file_path (str): Path to the Excel file containing Eagle I events.

        Returns:
        list: A list of EagleIEvent objects extracted from the file.
        # Initialize a list to store events outside of the for loop
        """
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

    @staticmethod
    def filter_eagle_i_with_noaa(eagle_i_events, noaa_events, noaa_to_eaglei_mapping):
        # Preprocess NOAA events: Group by region and sort by start time
        noaa_events_processed = defaultdict(list)
        for noaa_event in noaa_events:
            region = noaa_to_eaglei_mapping.get(noaa_event.cz_name_str, noaa_event.cz_name_str)
            start_time = datetime.strptime(f"{noaa_event.begin_date} {noaa_event.begin_time:04d}", '%m/%d/%Y %H%M')
            end_time = datetime.strptime(f"{noaa_event.end_date} {noaa_event.end_time:04d}", '%m/%d/%Y %H%M')
            noaa_events_processed[region].append((start_time, end_time))

        for region in noaa_events_processed:
            noaa_events_processed[region].sort(key=lambda x: x[0])

        # Dictionary to keep track of the last checked index for NOAA events in each region
        last_checked_index_per_region = {region: 0 for region in noaa_events_processed}
        
        filtered_events = []
        non_match_counter = 0  # Counter for non-matching events

        for eagle_i_event in eagle_i_events:
            eagle_i_time = eagle_i_event['run_start_time']
            # Check if the time is a string and convert it to datetime if needed
            if isinstance(eagle_i_time, str):
                eagle_i_time = datetime.strptime(eagle_i_time, '%Y-%m-%d %H:%M:%S')
            elif isinstance(eagle_i_time, pd.Timestamp):
                eagle_i_time = eagle_i_time.to_pydatetime()

            region = eagle_i_event['county']

            match_found = False
            for i in range(last_checked_index_per_region[region], len(noaa_events_processed[region])):
                noaa_event_start_time, noaa_event_end_time = noaa_events_processed[region][i]

                if eagle_i_time < noaa_event_start_time:
                    non_match_counter += 1
                    break  # No further NOAA events will match this Eagle I event

                if noaa_event_start_time <= eagle_i_time <= noaa_event_end_time:
                    filtered_events.append(eagle_i_event)  # Match found
                    #print(f"Match found: Eagle I event in {region} on {eagle_i_time} matches NOAA event between {noaa_event_start_time} and {noaa_event_end_time}.")
                    match_found = True
                    break  # Move to next Eagle I event

                last_checked_index_per_region[region] = i  # Update last checked index

            if not match_found:
                non_match_counter += 1
                if non_match_counter % 500000 == 0:
                    print(f"Checked {non_match_counter} non-matching events so far.")

        print(f"Filtered {len(filtered_events)} matching Eagle I events from {len(eagle_i_events)} original events.")
        return filtered_events
    
    @staticmethod
    def assign_eagle_i_events_to_hazards(hazards, eagle_i_events, noaa_to_eaglei_mapping):
        for hazard in hazards:
            print(f"Processing {hazard.type_of_hazard}...")
            filtered_eagle_i_events = EagleIEvent.filter_eagle_i_with_noaa(
                eagle_i_events, hazard.noaa_events, noaa_to_eaglei_mapping
            )

            for event in filtered_eagle_i_events:
                hazard.add_eaglei_event(event)
            print(f"Added {len(filtered_eagle_i_events)} Eagle I events to {hazard.type_of_hazard}.")

    @staticmethod
    def print_samples(eagle_i_events, sample_size=30):
        """
        Prints a sample of Eagle I events, grouped by year.

        Parameters:
        eagle_i_events (list): List of EagleIEvent objects.
        max_events_to_print (int): Maximum number of events to print per year.
        """
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
            for event in events[:sample_size]:
                print(event)
            # Print a message if there are more events than the sample printed
            if len(events) > sample_size:
                print(f"... and {len(events) - sample_size} more events.")

    @staticmethod
    def get_unique_eagle_i_counties(eagle_i_events):
        """
        Returns a set of unique counties from a list of Eagle I events.

        Parameters:
        eagle_i_events (list): List of EagleIEvent objects.

        Returns:
        set: A set of unique county names.
        """
        unique_counties = set()

        for event in eagle_i_events:
            if event['county'] is not None:
                unique_counties.add(event['county'].strip())

        return unique_counties

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