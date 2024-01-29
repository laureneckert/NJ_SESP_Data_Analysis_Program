#NJSESP Project
#Lauren Eckert
#Version 2

import pandas as pd
import utilities as uti
import os
from datetime import timedelta

class StormSystem:
    def __init__(self, year, start_date, end_date, storm_name, occurrence=1, storm_type=None, intensity=None, comment=None):
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
        self.storm_name = storm_name
        self.occurrence = occurrence
        self.storm_type = storm_type
        self.intensity = intensity
        self.comment = comment

        self.peak_outages_by_county = {}  # Stores peak outages for each county
        self.total_peak_outages = 0  # Stores total peak outages for the storm system


    @staticmethod
    def extract_data(file_path):
        """
        Reads data from an Excel file and creates StormSystem objects.
        """
        storm_systems = []
        try:
            df = pd.read_excel(file_path)
            print(f"Successfully read file: {file_path}")

            for index, row in df.iterrows():
                print(f"Processing row {index}: {row}")  # Debugging statement

                # Set the start date to the beginning of the day
                start_date = pd.to_datetime(row['Start Date']).normalize()
                print(f"Start date set to: {start_date}")  # Debugging statement

                # Handling 'End Date'
                if pd.isnull(row['End Date']):
                    # Set end date to the end of the start date's day
                    end_date = start_date + timedelta(days=1) - timedelta(seconds=1)
                else:
                    # Set end date to the end of the provided end date's day
                    end_date = pd.to_datetime(row['End Date']).normalize() + timedelta(days=1) - timedelta(seconds=1)
                print(f"End date set to: {end_date}")  # Debugging statement

                # Create a StormSystem object
                storm = StormSystem(
                    year=row['Year'],
                    start_date=start_date,
                    end_date=end_date,
                    storm_name=row['Storm Name'],
                    occurrence=row.get('Occurrence', 1),
                    storm_type=row.get('Storm Type', None),
                    intensity=row.get('Intensity', None),
                    comment=row.get('Comment', None)
                )
                storm_systems.append(storm)

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []

        print(f"Extracted {len(storm_systems)} storm systems from {file_path}")
        return storm_systems

    def print_basic_info(self):
        print(f"Storm System: {self.storm_name}, Year: {self.year}, Occurrence: {self.occurrence}")
        print(f"Start Date: {self.start_date}, End Date: {self.end_date}")
        print(f"Type: {self.storm_type}, Intensity: {self.intensity}")
        print(f"Comment: {self.comment}")

    def find_storm_system_by_name_and_occurrence(self, storm_name, occurrence=1):
        for system in self.storm_systems:
            if system.storm_name == storm_name and system.occurrence == occurrence:
                return system
        return None

    @staticmethod
    def load_or_create(pickle_path, excel_file_path, force_recreate=False):
        """
        Loads StormSystem objects from a pickle file or creates new ones from an Excel file.

        Parameters:
        pickle_path (str): Path to the pickle file.
        excel_file_path (str): Path to the Excel file.
        force_recreate (bool): Flag to force recreation of data from Excel file.

        Returns:
        list: A list of StormSystem objects.
        """
        if os.path.exists(pickle_path) and not force_recreate:
            print(f"Loading Storm Systems from pickle: {pickle_path}")
            storm_systems = uti.load_pickle(pickle_path)
            print(f"Loaded {len(storm_systems)} Storm Systems from pickle")
        else:
            if force_recreate:
                print(f"Force recreate is enabled. Creating Storm Systems from Excel file: {excel_file_path}")
            else:
                print(f"No pickle found. Creating Storm Systems from Excel file: {excel_file_path}")
            storm_systems = StormSystem.extract_data(excel_file_path)
            print(f"Saving {len(storm_systems)} Storm Systems to pickle: {pickle_path}")
            uti.save_to_pickle(storm_systems, pickle_path)

        return storm_systems
    
    def calculate_peak_outages(self, eaglei_events):
        peak_outages_by_county = {}
        for event in eaglei_events:
            if event.run_start_time >= self.start_date and event.run_end_time <= self.end_date:
                if event.county in peak_outages_by_county:
                    peak_outages_by_county[event.county] = max(peak_outages_by_county[event.county], event.outage)
                else:
                    peak_outages_by_county[event.county] = event.outage
        return sum(peak_outages_by_county.values())