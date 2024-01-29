#NJSESP Project
#Lauren Eckert
#Version 2

import os
import utilities as uti
from njsesp_config import config

from DataSource import DataSource
from EagleIEvent import EagleIEvent
from NOAAEvent import NOAAEvent
from FEMA_NRI_data import FEMA_NRI_data

from hazard import Hazard
from natural_hazard import NaturalHazard
from hurricanes import Hurricane
from storm_system import StormSystem

#Step 1: Check for pickles (pre-loaded and saved data ready to use)
if not os.path.exists(config['directories']['pickle_directory']): # Check if pickle directory exists
    os.makedirs(config['directories']['pickle_directory'])

#Step 2: Load or create data source objects
noaa_hurricane_events = DataSource.load_or_create( # Load or create NOAA hurricane events
    config['pickle_paths']['noaa_hurri'], 
    config['data_paths']['noaa']['noaa_hurricanes_files_directory'],
    NOAAEvent,
    force_recreate=True
)
eagle_i_events = DataSource.load_or_create( #Load or create Eagle I events
    config['pickle_paths']['eagle_i'], 
    config['data_paths']['eagle_i']['directory'],
    EagleIEvent,
    force_recreate=True
)
fema_nri_data = DataSource.load_or_create( # Load or create FEMA NRI data
    config['pickle_paths']['fema_nri'],
    config['data_paths']['fema_nri']['file_path'],
    FEMA_NRI_data,
    force_recreate=True
)

# Print samples using the respective method of each subclass
if noaa_hurricane_events:
    NOAAEvent.print_samples(noaa_hurricane_events, 30)
if eagle_i_events:
    EagleIEvent.print_samples(eagle_i_events, 30)
if fema_nri_data:
    FEMA_NRI_data.print_samples(fema_nri_data, 5)


#Step 3: Loading and creating natural hazards (Each natural hazard has one object for each subclass to store all the relevant variables in, the subclasses represent the entire risk, not individual events of the risk)
#Hurricanes
storm_systems = StormSystem.load_or_create( # Load or create StormSystem objects for hurricane storms
    config['pickle_paths']['storm_systems'],
    config['data_paths']['hurricanes']['storm_systems_file'],
    force_recreate=True
)
#Load or create hazard objects with default values
hurricanes = NaturalHazard.load_or_create(config['pickle_paths']['hurricanes'], Hurricane, force_recreate=False)

update_hurricanes_storm_systems_flag = True # Do you want to link the storm systems to the hurricanes hazard and then update the hurricanes pickle?

if update_hurricanes_storm_systems_flag: # Check the flag before proceeding
    print("Updating Hurricanes with new Storm Systems...")
    
    for storm in storm_systems:    # Loop through storm systems and add them to the Hurricanes object
        print(f"Adding Storm System: {storm.storm_name}, Year: {storm.year}")
        hurricanes.add_storm_system(storm)

    print("Saving updated Hurricanes data to pickle...")
    uti.save_to_pickle(hurricanes, config['pickle_paths']['hurricanes'])    # Save the updated Hurricanes object
    print("Hurricanes data successfully updated and saved.")
else:
    print("Update Hurricanes flag is set to False. Skipping update.")

if hurricanes:
    hurricanes.print_basic_info() # Print a summary of hurricane data

# Similarly, for other natural hazards like Lightning, WinterStorms, etc.

# Initialize list of all hazards
hazards = [hurricanes] # Add other hazards to this list


#Step 4: Assigning data from NOAA, filtering EagleI then assigning, and assigning FEMA NRI data to relevant hazards

#Define the mapping of NOAA event groups to hazards
noaa_event_groups = {
    'Hurricane': {
        'events': noaa_hurricane_events,
        'hazard': hurricanes,
        'type_of_hazard': 'hurricanes'  # Explicitly specify the type of hazard
    },
    # Add other mappings as needed
}


# Call the method to assign and link NOAA events to hazards
NOAAEvent.assign_and_link_noaa_events_to_hazard(noaa_event_groups) 
# Assign Eagle I events to hazards
EagleIEvent.assign_eagle_i_events_to_hazards(hazards, eagle_i_events, EagleIEvent.noaa_to_eaglei_mapping)
#save updated hazards
uti.save_natural_hazards_to_pickle(hazards)


"""
test_eagle_i_events = [
    {'fips_code': '34001', 'county': 'Atlantic', 'state': 'NJ', 'sum': 100, 'run_start_time': '2023-01-01 12:30:00'},
    {'fips_code': '34003', 'county': 'Bergen', 'state': 'NJ', 'sum': 200, 'run_start_time': '2023-02-01 10:30:00'},
    # Add more test events
]
"""