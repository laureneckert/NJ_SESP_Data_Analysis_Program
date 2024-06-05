#NJSESP Project
#Lauren Eckert
#Version 2

#USGS Events Class

import pandas as pd
import os
import csv
import re
import glob
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
            
    def extract_data(file_path):
        """
        Reads USGS data from a CSV file and creates USGSEvent objects.

        Parameters:
        file_path (str): Path to the CSV file containing data.

        Returns:
        list: A list of USGSEvent objects created from the file data.
        """
        usgs_entries = []
        try:
            df = pd.read_csv(file_path)
            print(f"Successfully read USGS file: {file_path}")

            for index, row in df.iterrows():
                event = USGSEvent( 
                    time=row.get('time', ""),
                    latitude=row.get('latitude', None),
                    longitude=row.get('longitude', None),
                    depth=row.get('depth', 0),
                    mag=row.get('mag', 0),
                    magType=row.get('magType', ""),
                    nst=row.get('nst', None),
                    gap=row.get('gap', 0),
                    dmin=row.get('dmin', 0),
                    rms=row.get('rms', 0),
                    net=row.get('net', ""),
                    id=row.get('id', ""),
                    updated=row.get('updated', ""),
                    place=row.get('place', ""),
                    type=row.get('type', ""),
                    horizontalError=row.get('horizontalError', 0),
                    depthError=row.get('depthError', 0),
                    magError=row.get('magError', 0),
                    magNst=row.get('magNst', 0),
                    status=row.get('status', ""),
                    locationSource=row.get('locationSource', ""),
                    magSource=row.get('magSource', "")
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
