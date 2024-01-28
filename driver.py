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

#Step 1: Check for pickles (pre-loaded and saved data ready to use)
# Check if pickle directory exists
if not os.path.exists(config['pickle_directory']):
    os.makedirs(config['pickle_directory'])

#Step 2: Load or create data source objects
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

#Step 3: Loading and creating natural hazards (Each natural hazard has one object for each subclass to store all the relevant variables in, the subclasses represent the entire risk, not individual events of the risk)

#Hurricanes
# Load or create StormSystem objects for hurricane storms (must do this first cause hurricanes class is a lil diff from other natural hazard subclasses)
storm_systems = StormSystem.load_or_create(
    config['storm_systems_pickle_path'],
    config['storm_systems_file_path'],
    force_recreate=False
)
#Load or create hazard objects with default values
hurricanes = NaturalHazard.load_or_create(config['hurricane_pickle_path'], Hurricane, force_recreate=False)
# Do you want to link the storm systems to the hurricanes hazard and then update the hurricanes pickle?
update_hurricanes_storm_systems_flag = False #This has been done and saved to the existing pickle file already, but you can re-run it if you'd like to update the pickle.
# Check the flag before proceeding
if update_hurricanes_storm_systems_flag:
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
# Print a summary of hurricane data
if hurricanes:
    hurricanes.print_basic_info()

# Similarly, for other natural hazards like Lightning, WinterStorms, etc.

# Initialize list of all hazards
hazards = [hurricanes] # Add other hazards to this list


#Step 4: Assigning data from NOAA, filtering EagleI then assigning, and assigning FEMA NRI data to relevant hazards

#Define the mapping of NOAA event groups to hazards
noaa_event_groups = {
    'Hurricane': {
        'events': noaa_hurricane_events,
        'hazard': hurricanes,
        'type_of_hazard': 'Hurricane'  # Explicitly specify the type of hazard
    },
    # Add other mappings as needed
}


# Call the method to assign and link NOAA events to hazards
#NOAAEvent.assign_and_link_noaa_events_to_hazard(noaa_event_groups) 

# Assign Eagle I events to hazards
EagleIEvent.assign_eagle_i_events_to_hazards(hazards, eagle_i_events, EagleIEvent.noaa_to_eaglei_mapping)
