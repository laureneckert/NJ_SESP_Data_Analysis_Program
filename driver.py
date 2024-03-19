#NJSESP Project
#Lauren Eckert
#Version 2
#driver

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

def check_for_pickles():
    if not os.path.exists(config['directories']['pickle_directory']): # Check if pickle directory exists
        os.makedirs(config['directories']['pickle_directory'])

def load_data():
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
    #verification step
    print_data = False # Print data source samples?
    if print_data:
        if noaa_hurricane_events:
            NOAAEvent.print_samples(noaa_hurricane_events, 30)
        if eagle_i_events:
            EagleIEvent.print_samples(eagle_i_events, 30)
        if fema_nri_data:
            FEMA_NRI_data.print_samples(fema_nri_data, 5)
    else:
        print("Print NOAA, Ealge I, FEMA data sample flag off. Skipping.")

    return noaa_hurricane_events, eagle_i_events, fema_nri_data

def load_hurricane_related_stuff():
    storm_systems = StormSystem.load_or_create( # Load or create StormSystem objects for hurricane storms
        config['pickle_paths']['storm_systems'],
        config['data_paths']['hurricanes']['storm_systems_file'],
        force_recreate=True
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

    #verification step
    print_data_2 = False # Print a summary of hurricane data?
    if print_data_2:
        if hurricanes:
            hurricanes.print_basic_info() 
    else:
        print("Print hurricane data sample flag off. Skipping.")
    
    return storm_systems, hurricanes

def sort_and_assign_data(eagle_i_events, fema_nri_data, hurricanes, hazards):
    #Define the mapping of NOAA event groups to hazards
    noaa_event_groups = {
        'Hurricane': {
            'events': noaa_hurricane_events,
            'hazard': hurricanes,
            'type_of_hazard': 'hurricanes'  # Explicitly specify the type of hazard
        },
    }

    sort_and_assign_then_save = False #Do you want to assign the data sources to the hazards? Do this if you just created new natural hazard objects or new data source objects.
    if sort_and_assign_then_save:
        print("Beginning sorting and assigning data sources to hazards")

        FEMA_NRI_data.assign_data_to_hazard(hazards, fema_nri_data, FEMA_NRI_data.hazard_to_fema_prefix)
        # Save the updated hazard objects
        pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
        uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)
        
        NOAAEvent.assign_and_link_noaa_events_to_hazard(noaa_event_groups) # assign and link NOAA events to hazards
        # Save the updated hazard objects
        pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
        uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)

        EagleIEvent.assign_eagle_i_events_to_hazards(hazards, eagle_i_events, EagleIEvent.noaa_to_eaglei_mapping) # Filter & Assign Eagle I events to hazards
        # Save the updated hazard objects
        pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
        uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)
    
    else:
        print("Sorting and assigning data skipped.")

    #verification step
    for hazard in hazards:
        hazard.print_data_source_samples(sample_size=5) # Print samples of each data source organized by hazard

def data_processing_for_eaglei(eagle_i_events, noaa_hurricane_events, storm_systems):
    # Calculating EWMA and seasonal baseline
    ewma_data = EagleIEvent.calculate_ewma(eagle_i_events)

    # Cap the EWMA data and get the cap value
    capped_ewma, cap_value = EagleIEvent.cap_ewma_and_get_cap_value(ewma_data)

    # Now apply seasonal decomposition to capped EWMA data to get the seasonal baseline
    seasonal_baseline = EagleIEvent.calculate_seasonal_baseline(capped_ewma)

    # Printing samples of the calculated data
    #EagleIEvent.print_df_sample_data(ewma_data, sample_size=50)
    #EagleIEvent.print_df_sample_data(seasonal_baseline, sample_size=80)# Call the method with flags set to your preference

    # Use the capped EWMA, seasonal baseline, and cap value in the plotting method
    #EagleIEvent.plot_outages_over_time_per_year(eagle_i_events, ewma_data, seasonal_baseline, noaa_hurricane_events, storm_systems, cap_value, show_noaa_events=True, show_storm_systems=True)
    #EagleIEvent.plot_zoomed_outages_around_storms(eagle_i_events, ewma_data, seasonal_baseline, noaa_hurricane_events, storm_systems, cap_value)

    return ewma_data, seasonal_baseline

#Step 1: Check for pickles (pre-loaded and saved data ready to use)
check_for_pickles()

#Step 2: Load or create data source objects
noaa_hurricane_events, eagle_i_events, fema_nri_data = load_data()

#Step 3: Loading and creating natural hazards NOTE: Each natural hazard has one object for each subclass to store all the relevant variables in, the subclasses represent the entire risk, not individual events of the risk
#Hurricanes
storm_systems, hurricanes = load_hurricane_related_stuff()
#winter storms
#tornados
#flooding
#lightning

# Initialize list of all hazards
hazards = [hurricanes] # Add other hazards to this list

#Step 4: Assigning data from NOAA, filtering EagleI then assigning, and assigning FEMA NRI data to relevant hazards
sort_and_assign_data(eagle_i_events, fema_nri_data, hurricanes, hazards)

#Step 5: Data processing for natural hazards - calculating EWMA, seasonal baseline, plotting results
ewma_data, seasonal_baseline = data_processing_for_eaglei(eagle_i_events, noaa_hurricane_events, storm_systems)

#5.2 processing the noaa events to get the event windows without overlaps
hurricanes.process_noaa_events()
hurricanes.link_and_print_summary()
unlinked_noaa_windows = hurricanes.identify_unlinked_noaa_windows()
# Assuming the identify_unlinked_noaa_windows method is adjusted to return the list of unlinked windows
if unlinked_noaa_windows:
    print("Attempting to link unlinked NOAA event windows to storm systems based on file names.")
    hurricanes.link_unlinked_noaa_windows()
else:
    print("No unlinked NOAA event windows to process.")
hurricanes.identify_unlinked_noaa_windows(return_unlinked=False)
#hurricanes.print_noaa_window_summary()

# After processing NOAA events and linking unlinked windows
print("\nVerifying linked NOAA event windows for each storm system:")

# Example code for iterating over storm systems to verify linked NOAA event windows
linked_windows_summary = {}  # Dictionary to keep a summary of linked windows count for each storm

for storm_system in hurricanes.storm_systems:
    linked_windows_count = len(storm_system.processed_noaa_event_windows)
    linked_windows_summary[storm_system.storm_name] = linked_windows_count
    print(f"Storm System: {storm_system.storm_name} (Year: {storm_system.year}) - Linked NOAA Event Windows: {linked_windows_count}")

    # Proceed with further analysis only if the storm system has linked NOAA event windows
    if linked_windows_count > 0:
        total_duration, timestamps_above = hurricanes.calculate_duration_above_baseline_for_windows(
            storm_system.processed_noaa_event_windows, ewma_data, seasonal_baseline)
        
        # Print or store the results as needed
        print(f"Total Duration Above Baseline: {total_duration}")
        print(f"Timestamps Above Baseline: {timestamps_above}")
    else:
        print(f"No linked NOAA event windows for {storm_system.storm_name}. Skipping duration calculation.")



"""
#Hurricanes   
hurricanes.calculate_average_peak_outages() #NOT CORRECT LOL IM DUMB
hurricanes.calculate_percent_customers_affected()  #SEE ABOVE
frequency_coefficient, intensity_coefficient = hurricanes.calculate_regression_coefficients() #pretty sure this ones fine tho
hurricanes.analyze_hurricane_data() #need to adjust this function cause IT DONT WORK

#Print the result for verification
print(f"Average Peak Outages: {hurricanes.customers_affected_sum}")
print(f"Percent Customers Affected: {hurricanes.percent_customers_affected}%")

print(f"Frequency Coefficient: {frequency_coefficient}")
print(f"Intensity Coefficient: {intensity_coefficient}")
#print(f"Future Impact Coefficient: *****here")

#Save results
pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)
pickle_path_for_storm_systems = config['pickle_paths']['storm_systems']
uti.save_to_pickle(storm_systems, pickle_path_for_storm_systems)
"""