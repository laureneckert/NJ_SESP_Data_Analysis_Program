#NJSESP Project
#Lauren Eckert
#Version 2

#USGS Events Class

import pandas as pd
import os
import csv
import re
import glob
from datetime import datetime, timedelta
import pytz
from njsesp_config import config
from DataSource import DataSource

class USGSEvent(DataSource):
    def __init__(self, time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms, net, id, updated, place, type, horizontalError, depthError, magError, magNst, status, locationSource, magSource):
        super().__init__()
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.mag = mag
        self.magType = magType
        self.nst = nst
        self.gap = gap
        self.dmin = dmin
        self.rms = rms
        self.net = net
        self.id = id
        self.updated = updated
        self.place = place
        self.type = type
        self.horizontalError = horizontalError
        self.depthError = depthError
        self.magError = magError
        self.magNst = magNst
        self.status = status
        self.locationSource = locationSource
        self.magSource = magSource

        self.cleaned_time = None
        self.usgs_window = None

            
    @staticmethod
    def clean_times(events):
        """
        Cleans the time attribute for each USGSEvent object in the list, converting it to a datetime object.
        """
        for event in events:
            original_time = event.time
            print(f"Original time string: {original_time}")

            # Parse the time string into a datetime object, removing 'Z' and converting to timezone aware datetime
            cleaned_time = datetime.strptime(event.time[:-1], '%Y-%m-%dT%H:%M:%S.%f')
            #cleaned_time = cleaned_time.replace(tzinfo=pytz.utc)
            
            print(f"Converted to datetime object: {cleaned_time}")

            event.cleaned_time = cleaned_time  # Update the cleaned time attribute

    @staticmethod
    def create_time_windows(events):
        """
        Creates a tuple of start and end times for each USGSEvent object. The end time is 30 minutes after the start time.
        """
        print("Creating time windows for each USGSEvent object...")
        for event in events:
            end_time = event.cleaned_time + timedelta(minutes=15)
            event.usgs_window = (event.cleaned_time, end_time)
            print(f"Time window for event: Start: {event.cleaned_time}, End: {end_time}")
    
    @staticmethod
    def process_event_times(events):
        """
        Processes the times for a list of USGSEvent objects by cleaning and creating windows.
        """
        print("Processing event times...")
        USGSEvent.clean_times(events)
        USGSEvent.create_time_windows(events)

    @staticmethod
    def extract_data(file_path):
        usgs_entries = []
        try:
            df = pd.read_csv(file_path)
            print(f"Successfully read USGS file: {file_path}")

            for index, row in df.iterrows():
                event = USGSEvent(
                    time=row['time'],
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    depth=row['depth'],
                    mag=row['mag'],
                    magType=row['magType'],
                    nst=row['nst'],
                    gap=row['gap'],
                    dmin=row['dmin'],
                    rms=row['rms'],
                    net=row['net'],
                    id=row['id'],
                    updated=row['updated'],
                    place=row['place'],
                    type=row['type'],
                    horizontalError=row['horizontalError'],
                    depthError=row['depthError'],
                    magError=row['magError'],
                    magNst=row['magNst'],
                    status=row['status'],
                    locationSource=row['locationSource'],
                    magSource=row['magSource']
                )
                usgs_entries.append(event)

        except Exception as e:
            print(f"Error reading USGS file {file_path}: {e}")
            return []

        print(f"Extracted {len(usgs_entries)} USGS entries from {file_path}")
        return usgs_entries
    
    @staticmethod
    def print_samples(usgs_data, sample_size=5):
        """
        Prints a sample of USGS data entries.

        Parameters:
        usgs_data (list): List of USGSEvent instances.
        sample_size (int): Number of samples to print.
        """
        print("\nSample USGS Data:")
        for i, event in enumerate(usgs_data[:sample_size]):
            print(f"Time: {event.time}, Magnitude : {event.mag}, Place : {event.place}")

    