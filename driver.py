#NJSESP Project
#Lauren Eckert
#Version 2

# Import necessary modules and classes
import os
import utilities as uti
from config import config

from DataSource import DataSource
from EagleIEvent import EagleIEvent
from NOAAEvent import NOAAEvent
from FEMA_NRI_data import FEMA_NRI_data

from hazard import Hazard
from natural_hazard import NaturalHazard
from hurricanes import Hurricane
from storm_system import StormSystem

# Check if pickle directory exists
if not os.path.exists(config['pickle_directory']):
    os.makedirs(config['pickle_directory'])

#Load or create data source objects

# Load or create NOAA hurricane events
noaa_hurricane_events = DataSource.load_or_create(
    config['noaa_hurricanes_pickle_path'], 
    config['noaa_hurricane_files_directory'],
    NOAAEvent,
    force_recreate=False  # Set to True to force recreation of data
)

# Load or create Eagle I events
eagle_i_events = DataSource.load_or_create(
    config['eagle_i_pickle_path'], 
    config['eagle_i_directory'],
    EagleIEvent,
    force_recreate=False  # Set to True to force recreation of data
)

# Load or create FEMA NRI data
fema_nri_data = DataSource.load_or_create(
    config['fema_nri_pickle_path'],
    config['fema_nri_file_path'],
    FEMA_NRI_data,
    force_recreate=False # Set to True to force recreation of data
)

# Print samples using the respective method of each subclass
"""
if noaa_hurricane_events:
    NOAAEvent.print_samples(noaa_hurricane_events, 30)

if eagle_i_events:
    EagleIEvent.print_samples(eagle_i_events, 30)

if fema_nri_data:
    FEMA_NRI_data.print_samples(fema_nri_data, 5)
"""

#Loading and creating natural hazards

# Load or create StormSystem objects for hurricane storms
storm_systems = StormSystem.load_or_create(
    config['storm_systems_pickle_path'],
    config['storm_systems_file_path'],
    force_recreate=False
)

#Load or create hazard objects with default values
hurricanes = NaturalHazard.load_or_create(config['hurricane_pickle_path'], Hurricane, force_recreate=True)

# Do you want to link the storm systems to the hurricanes hazard and then update the hurricanes pickle?
update_hurricanes_flag = True
# Check the flag before proceeding
if update_hurricanes_flag:
    print("Updating Hurricanes with new Storm Systems...")

    # Loop through storm systems and add them to the Hurricanes object
    for storm in storm_systems:
        print(f"Adding Storm System: {storm.storm_name}, Year: {storm.year}")
        hurricanes.add_storm_system(storm)

    # Save the updated Hurricanes object
    print("Saving updated Hurricanes data to pickle...")
    uti.save_to_pickle(hurricanes, config['hurricane_pickle_path'])
    print("Hurricanes data successfully updated and saved.")
else:
    print("Update Hurricanes flag is set to False. Skipping update.")



# Similarly, for other natural hazards like Lightning, WinterStorms, etc.
