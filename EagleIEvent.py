#NJSESP Project
#Lauren Eckert
#Version 2

import pandas as pd
from datetime import datetime
import os
from DataSource import DataSource

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
        """
        Filters Eagle I events based on matching NOAA events.

        Parameters:
        eagle_i_events (list): List of EagleIEvent objects.
        noaa_events (list): List of NOAAEvent objects.
        noaa_to_eaglei_mapping (dict): Mapping of NOAA region names to Eagle I county names.

        Returns:
        list: Filtered list of EagleIEvent objects.
        """
        filtered_events = []
        for eagle_i_event in eagle_i_events:
            eagle_i_county = eagle_i_event['county']
            eagle_i_time = eagle_i_event['run_start_time']

            # Check if run_start_time is a string and convert it to datetime
            if isinstance(eagle_i_time, str):
                eagle_i_time = datetime.strptime(eagle_i_time, '%Y-%m-%d %H:%M:%S')

            for noaa_event in noaa_events:
                noaa_region = noaa_to_eaglei_mapping.get(noaa_event.cz_name_str, noaa_event.cz_name_str)

                if eagle_i_county == noaa_region:
                    # Pad begin and end times with zeros to ensure correct format
                    noaa_event_start_time = datetime.strptime(f"{noaa_event.begin_date} {noaa_event.begin_time:04d}", '%m/%d/%Y %H%M')
                    noaa_event_end_time = datetime.strptime(f"{noaa_event.end_date} {noaa_event.end_time:04d}", '%m/%d/%Y %H%M')

                    if noaa_event_start_time <= eagle_i_time <= noaa_event_end_time:
                        filtered_events.append(eagle_i_event)
                        # Continues searching for more matches

        print(f"Filtered {len(filtered_events)} matching Eagle I events from {len(eagle_i_events)} original events.")
        return filtered_events

    @staticmethod
    def assign_eagle_i_list_to_hazard(hazard, eagle_i_events):
        """
        Assigns a list of Eagle I events to a given hazard.

        Parameters:
        hazard (Hazard): The hazard to assign events to.
        eagle_i_events (list): List of EagleIEvent objects.
        """
        for event in eagle_i_events:
            hazard.add_eaglei_event(event)

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