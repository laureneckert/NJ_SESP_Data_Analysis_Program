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
    force_recreate=False
)
eagle_i_events = DataSource.load_or_create( #Load or create Eagle I events
    config['pickle_paths']['eagle_i'], 
    config['data_paths']['eagle_i']['directory'],
    EagleIEvent,
    force_recreate=False
)
fema_nri_data = DataSource.load_or_create( # Load or create FEMA NRI data
    config['pickle_paths']['fema_nri'],
    config['data_paths']['fema_nri']['file_path'],
    FEMA_NRI_data,
    force_recreate=False
)

print_data = False
# Print samples using the respective method of each subclass
if print_data:
    if noaa_hurricane_events:
        NOAAEvent.print_samples(noaa_hurricane_events, 30)
    if eagle_i_events:
        EagleIEvent.print_samples(eagle_i_events, 30)
    if fema_nri_data:
        FEMA_NRI_data.print_samples(fema_nri_data, 5)
else:
    print("Print NOAA, Ealge I, FEMA data sample flag off. Skipping.")

#Step 3: Loading and creating natural hazards (Each natural hazard has one object for each subclass to store all the relevant variables in, the subclasses represent the entire risk, not individual events of the risk)
#Hurricanes
storm_systems = StormSystem.load_or_create( # Load or create StormSystem objects for hurricane storms
    config['pickle_paths']['storm_systems'],
    config['data_paths']['hurricanes']['storm_systems_file'],
    force_recreate=False
)
#Load or create hazard objects with default values
hurricanes = NaturalHazard.load_or_create(config['pickle_paths']['hurricanes'], Hurricane, force_recreate=False)

update_hurricanes_storm_systems_flag = False # Do you want to link the storm systems to the hurricanes hazard and then update the hurricanes pickle?

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

print_data_2 = False
if print_data_2:
    if hurricanes:
        hurricanes.print_basic_info() # Print a summary of hurricane data
else:
    print("Print hurricane data sample flag off. Skipping.")

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

sort_and_assign_then_save = False
if sort_and_assign_then_save:
    print("Beginning sorting and assigning data sources to hazards")

    FEMA_NRI_data.assign_data_to_hazard(hazards, FEMA_NRI_data.hazard_to_fema_prefix)
    # Save the updated hurricane object
    pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
    uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)

    NOAAEvent.assign_and_link_noaa_events_to_hazard(noaa_event_groups) # assign and link NOAA events to hazards
    # Save the updated hurricane object
    pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
    uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)

    EagleIEvent.assign_eagle_i_events_to_hazards(hazards, eagle_i_events, EagleIEvent.noaa_to_eaglei_mapping) # Filter & Assign Eagle I events to hazards
    # Save the updated hurricane object
    pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
    uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)
else:
    print("Sorting and assigning data skipped.")


for hazard in hazards:
    hazard.print_data_source_samples(sample_size=5) # Print samples of each data source for each hazard


# Calculate the average peak outages and percent customers affected
hurricanes.calculate_average_peak_outages(eagle_i_events)
hurricanes.calculate_percent_customers_affected()
# Print the result for verification
print(f"Average Peak Outages: {hurricanes.customers_affected_sum}")
print(f"Percent Customers Affected: {hurricanes.percent_customers_affected}%")

frequency_coefficient, intensity_coefficient = hurricanes.calculate_regression_coefficients()
print(f"Frequency Coefficient: {frequency_coefficient}")
print(f"Intensity Coefficient: {intensity_coefficient}")

pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)

pickle_path_for_storm_systems = config['pickle_paths']['storm_systems']
uti.save_to_pickle(storm_systems, pickle_path_for_storm_systems)
