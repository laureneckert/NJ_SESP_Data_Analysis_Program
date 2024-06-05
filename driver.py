#NJSESP Project
#Lauren Eckert
#Version 2
#driver

import os
import sys
import utilities as uti
from njsesp_config import config

from DataSource import DataSource
from EagleIEvent import EagleIEvent
from NOAAEvent import NOAAEvent
from FEMA_NRI_data import FEMA_NRI_data
from USGSEvent import USGSEvent

from hazard import Hazard
from natural_hazard import NaturalHazard
from hurricanes import Hurricane
from lightning import Lightning
from winter_storms import WinterStorms
from tornados import Tornados
from wildfire import Wildfires
from flooding import Flooding
from hail import Hail
from strong_wind import StrongWinds
from storm_system import StormSystem
from earthquakes import Earthquakes

driver_config_flags = {

    "force_recreate_noaa_hurricanes_events": False,
    "force_recreate_noaa_lightning_events": False,
    "force_recreate_noaa_winter_storms_events": False,
    "force_recreate_noaa_tornados_events": False,
    "force_recreate_noaa_wildfires_events": False,
    "force_recreate_noaa_flooding_events": False,
    "force_recreate_noaa_hail_events": False,
    "force_recreate_noaa_strong_winds_events": False,
    "force_recreate_usgs_earthquake_events" : False,
    
    "force_recreate_eagle_i_events": False,
    "force_recreate_fema_nri_data": False,
    "force_recreate_usgs_data" : False,
    
    "force_recreate_storm_systems": False,
    "force_recreate_lightning" : False,
    "force_recreate_hurricanes": False,
    "force_recreate_winter_storms" : False,
    "force_recreate_tornados" : False,
    "force_recreate_wildfires" : False,
    "force_recreate_flooding" : False,
    "force_recreate_hail" : False,
    "force_recreate_strong_winds" : False,
    "force_recreate_earthquakes" : False,

    "sort_and_assign_data" : True
}

def check_for_pickles():
    if not os.path.exists(config['directories']['pickle_directory']): # Check if pickle directory exists
        os.makedirs(config['directories']['pickle_directory'])

def load_data():
    #NOAA Hurricanes
    noaa_hurricane_events = DataSource.load_or_create( # Load or create NOAA hurricane events
        config['pickle_paths']['noaa_hurri'], 
        config['data_paths']['noaa']['noaa_hurricanes_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_hurricanes_events"]
        )
    #NOAA lightning
    noaa_lightning_events = DataSource.load_or_create( #Load or create NOAA lightning events
        config['pickle_paths']['noaa_lightning'], 
        config['data_paths']['noaa']['noaa_lightning_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_lightning_events"]
        )
    #NOAA winter storms
    noaa_winter_storms_events = DataSource.load_or_create( #Load or create NOAA winter storms events
        config['pickle_paths']['noaa_winter_storms'], 
        config['data_paths']['noaa']['noaa_winter_storms_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_winter_storms_events"]
        )
    #NOAA tornado
    noaa_tornado_events = DataSource.load_or_create( #Load or create NOAA tornado events
        config['pickle_paths']['noaa_tornados'], 
        config['data_paths']['noaa']['noaa_tornados_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_tornados_events"]
        )
    #NOAA wildfire
    noaa_wildfire_events = DataSource.load_or_create( #Load or create NOAA wildfire events
        config['pickle_paths']['noaa_wildfires'], 
        config['data_paths']['noaa']['noaa_wildfires_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_wildfires_events"]
        )
    #NOAA flooding
    noaa_flooding_events = DataSource.load_or_create( #Load or create NOAA flooding events
        config['pickle_paths']['noaa_flooding'], 
        config['data_paths']['noaa']['noaa_flooding_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_flooding_events"]
        )
    #NOAA hail
    noaa_hail_events = DataSource.load_or_create( #Load or create NOAA hail events
        config['pickle_paths']['noaa_hail'], 
        config['data_paths']['noaa']['noaa_hail_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_hail_events"]
        )
    #NOAA strong wind
    noaa_strong_wind_events = DataSource.load_or_create( #Load or create NOAA strong wind events
        config['pickle_paths']['noaa_strong_winds'], 
        config['data_paths']['noaa']['noaa_strong_winds_files_directory'],
        NOAAEvent,
        force_recreate=driver_config_flags["force_recreate_noaa_strong_winds_events"]
        )

    eagle_i_events = DataSource.load_or_create( #Load or create Eagle I events
        config['pickle_paths']['eagle_i'], 
        config['data_paths']['eagle_i']['directory'],
        EagleIEvent,
        force_recreate=driver_config_flags["force_recreate_eagle_i_events"]
    )
    fema_nri_data = DataSource.load_or_create( # Load or create FEMA NRI data
        config['pickle_paths']['fema_nri'],
        config['data_paths']['fema_nri']['file_path'],
        FEMA_NRI_data,
        force_recreate=driver_config_flags["force_recreate_fema_nri_data"]
    )
    usgs_data = DataSource.load_or_create( #Load or create USGS data
        config['pickle_paths']['usgs'],
        config['data_paths']['usgs']['file_path'],
        USGSEvent,
        force_recreate=driver_config_flags["force_recreate_usgs_data"]
        )
        
    #verification step
    print_data = True # Print data source samples?
    if print_data:
        if noaa_hurricane_events:
            NOAAEvent.print_samples(noaa_hurricane_events, 30)
        else:
            print("No NOAA hurricane events in driver.")
        if noaa_lightning_events:
            NOAAEvent.print_samples(noaa_lightning_events, 30)
        else:
            print("No NOAA lightning events in driver.")
        if noaa_winter_storms_events:
            NOAAEvent.print_samples(noaa_winter_storms_events, 30)
        else:
            print("No NOAA winter storm events in driver.")
        if noaa_flooding_events:
            NOAAEvent.print_samples(noaa_flooding_events, 30)
        else:
            print("No NOAA flooding events in driver.")
        if noaa_tornado_events:
            NOAAEvent.print_samples(noaa_tornado_events, 30)
        else:
            print("No NOAA tornado events in driver.")
        if noaa_wildfire_events:
            NOAAEvent.print_samples(noaa_wildfire_events, 30)
        else:
            print("No NOAA wildfire events in driver.")
        if noaa_hail_events:
            NOAAEvent.print_samples(noaa_hail_events, 30)
        else:
            print("No NOAA hail events in driver.")
        if noaa_strong_wind_events:
            NOAAEvent.print_samples(noaa_strong_wind_events, 30)
        else:
            print("No NOAA strong wind events in driver.")
        
        if eagle_i_events:
            EagleIEvent.print_samples(eagle_i_events, 30)
        if fema_nri_data:
            FEMA_NRI_data.print_samples(fema_nri_data, 5)
        if usgs_data:
            USGSEvent.print_samples(usgs_data, 5)
    else:
        print("Print NOAA, Ealge I, FEMA data sample flag off. Skipping.")

    return noaa_hurricane_events, noaa_lightning_events, noaa_winter_storms_events, noaa_flooding_events, noaa_tornado_events, noaa_wildfire_events, noaa_hail_events, noaa_strong_wind_events, eagle_i_events, fema_nri_data, usgs_data

def load_hazards():
    #Hurricane stuff
    ##Storm Systems
    storm_systems = StormSystem.load_or_create( # Load or create StormSystem objects for hurricane storms
        config['pickle_paths']['storm_systems'],
        config['data_paths']['hurricanes']['storm_systems_file'],
        force_recreate=driver_config_flags["force_recreate_storm_systems"]
    )
    ##Hurricanes
    hurricanes = NaturalHazard.load_or_create(config['pickle_paths']['hurricanes'], Hurricane, force_recreate=driver_config_flags["force_recreate_hurricanes"])
    update_hurricanes_storm_systems_flag = driver_config_flags["force_recreate_hurricanes"] # Do you want to link the storm systems to the hurricanes hazard and then update the hurricanes pickle?
    if update_hurricanes_storm_systems_flag: # Check the flag before proceeding
        print("Updating Hurricanes with new Storm Systems...")
        
        for storm in storm_systems:    # Loop through storm systems and add them to the Hurricanes object
            print(f"Adding Storm System: {storm.storm_name}, Year: {storm.year}")
            hurricanes.add_storm_system(storm)

        print("Saving updated Hurricanes data to pickle...")
        uti.save_to_pickle(hurricanes, config['pickle_paths']['hurricanes'])    # Save the updated Hurricanes object
        print("Hurricanes data successfully updated and saved.")
    else:
        print("Update Hurricanes flag is set to True. Skipping update.")

    ##verification step
    print_data_2 = True # Print a summary of hurricane data?
    if print_data_2:
        if hurricanes:
            hurricanes.print_basic_info() 
    else:
        print("Print hurricane data sample flag off. Skipping.")
    
    #winter storms
    winter_storms = NaturalHazard.load_or_create(config['pickle_paths']['winter_storms'], WinterStorms, force_recreate=driver_config_flags["force_recreate_winter_storms"])
    #tornado
    tornados = NaturalHazard.load_or_create(config['pickle_paths']['tornados'], Tornados, force_recreate=driver_config_flags["force_recreate_tornados"])
    #wildfire
    wildfires = NaturalHazard.load_or_create(config['pickle_paths']['wildfires'], Wildfires, force_recreate=driver_config_flags["force_recreate_wildfires"])
    #flooding
    flooding = NaturalHazard.load_or_create(config['pickle_paths']['flooding'], Flooding, force_recreate=driver_config_flags["force_recreate_flooding"])
    #hail
    hail = NaturalHazard.load_or_create(config['pickle_paths']['hail'], Hail, force_recreate=driver_config_flags["force_recreate_hail"])
    #strong wind
    strong_winds = NaturalHazard.load_or_create(config['pickle_paths']['strong_winds'], StrongWinds, force_recreate=driver_config_flags["force_recreate_strong_winds"])
    #lightning
    lightning = NaturalHazard.load_or_create(config['pickle_paths']['lightning'], Lightning, force_recreate=driver_config_flags["force_recreate_lightning"])
    #earthquakes TODO
    earthquakes = NaturalHazard.load_or_create(config['pickle_paths']['earthquakes'], Earthquakes, force_recreate=driver_config_flags['force_recreate_earthquakes'])

    # Initialize list of all hazards
    hazards = [hurricanes, tornados, wildfires, winter_storms, flooding, hail, strong_winds, lightning, earthquakes] # Add other hazards to this list
    #verification step/previous debugging
    for hazard in hazards:
        try:
            hazard_type = hazard.type_of_hazard
            print(f"\n{hazard} is a {hazard_type}")
        except Exception as e:
            print(f"\n Hazard {hazard} is having an issue with the type of hazard attribute. Issue: {e}")
            hazard.type_of_hazard = 'test'
            continue
        try:
            hazard_type = hazard.type_of_hazard
            print(f"\n{hazard} is definitely a {hazard_type}")
        except Exception as e:
            print(f"\n Hazard {hazard} is STILLLLL having an issue with the type of hazard attribute. Issue: {e}")
            continue
    
    try:
        print("Saving all hazard pickles now...")
        uti.save_natural_hazards_to_pickles(hazards)
    except Exception as e:
        print("Error saving all natural hazard pickles. Error: {e}")

    return storm_systems, hurricanes, winter_storms, tornados, wildfires, flooding, hail, strong_winds, lightning, earthquakes, hazards

def sort_and_assign_data(eagle_i_events, fema_nri_data, noaa_hurricane_events, noaa_lightning_events,
                          noaa_winter_storms_events, noaa_flooding_events, noaa_tornado_events, noaa_wildfire_events, 
                          noaa_hail_events, noaa_strong_wind_events, hurricanes, lightning, winter_storms, flooding,
                          tornados, wildfires, hail, strong_winds, earthquakes, hazards):
    #Define the mapping of NOAA event groups to hazards
    noaa_event_groups = {
        'Hurricane': {
            'events': noaa_hurricane_events,
            'hazard': hurricanes,
            'type_of_hazard': 'hurricanes'  # Explicitly specify the type of hazard
        },    
        'Lightning': {
            'events': noaa_lightning_events,
            'hazard': lightning,
            'type_of_hazard' : 'lightning'
        },
        'WinterStorms' : {
            'events' : noaa_winter_storms_events,
            'hazard' : winter_storms,
            'type_of_hazard' : 'winter_storms'
        },
        'Flooding' : {
            'events' : noaa_flooding_events,
            'hazard' : flooding,
            'type_of_hazard' : 'flooding'
        },
        'Tornados' : {
            'events' : noaa_tornado_events,
            'hazard' : tornados,
            'type_of_hazard' : 'tornados'
        },
        'Wildfires' : {
            'events' : noaa_wildfire_events,
            'hazard' : wildfires,
            'type_of_hazard' : 'wildfires'
        },
        'Hail' : {
            'events' : noaa_hail_events,
            'hazard' : hail,
            'type_of_hazard' : 'hail'
        },
        'StrongWinds' : {
            'events' : noaa_strong_wind_events,
            'hazard' : strong_winds,
            'type_of_hazard' : 'strong_winds'
        }
    }

    sort_and_assign_then_save = driver_config_flags["sort_and_assign_data"] #Do you want to assign the data sources to the hazards? Do this if you just created new natural hazard objects or new data source objects.
    if sort_and_assign_then_save:
        print("Beginning sorting and assigning data sources to hazards")

        FEMA_NRI_data.assign_data_to_hazard(hazards, fema_nri_data, FEMA_NRI_data.hazard_to_fema_prefix)
        
        for hazard in hazards:
            if not isinstance(hazard, Earthquakes):  # Skip processing for earthquake objects cause they use different data sources
                NOAAEvent.assign_and_link_noaa_events_to_hazard(noaa_event_groups) # assign and link NOAA events to hazards
                EagleIEvent.assign_eagle_i_events_to_hazards(hazards, eagle_i_events, EagleIEvent.noaa_to_eaglei_mapping) # Filter & Assign Eagle I events to hazards

        try:
            print("Saving all hazard pickles now...")
            uti.save_natural_hazards_to_pickles(hazards)
        except Exception as e:
            print("Error saving all natural hazard pickles. Error: {e}")
    
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

def process_hurricanes(ewma_data, seasonal_baseline, hurricanes, storm_systems):
    hurricanes.process_noaa_events()
    hurricanes.link_and_print_summary()
    unlinked_noaa_windows = hurricanes.identify_unlinked_noaa_windows() 
    # Assuming the identify_unlinked_noaa_windows method is adjusted to return the list of unlinked windows
    if unlinked_noaa_windows:
        print("Attempting to link unlinked NOAA event windows to storm systems based on file names.")
        hurricanes.link_unlinked_noaa_windows()
    else:
        print("No unlinked NOAA event windows to process.")
    hurricanes.identify_unlinked_noaa_windows(return_unlinked=True)
    hurricanes.print_noaa_window_summary()
    print("-------------------------------------------------")
    print("\nVerifying linked NOAA event windows for each storm system:")

    # Example code for iterating over storm systems to verify linked NOAA event windows
    linked_windows_summary = {}  # Dictionary to keep a summary of linked windows count for each storm
    print("-------------------------------------------------")
    for storm_system in hurricanes.storm_systems:
        print("************")
        linked_windows_count = len(storm_system.processed_noaa_event_windows)
        linked_windows_summary[storm_system.storm_name] = linked_windows_count
        print(f"Storm System: {storm_system.storm_name} (Year: {storm_system.year}) - Linked NOAA Event Windows: {linked_windows_count}")

        # Proceed with further analysis only if the storm system has linked NOAA event windows
        if linked_windows_count > 0:
            total_duration, timestamps_above = hurricanes.calculate_duration_above_baseline_for_windows(
                storm_system.processed_noaa_event_windows, ewma_data, seasonal_baseline)
            
            # Assign the results to the storm system for later use in averaging
            storm_system.outages_above_baseline_duration = total_duration
            storm_system.outages_above_baseline_timestamps = timestamps_above

            # Print or store the results as needed
            print(f"Total Duration Above Baseline: {total_duration}")
            print(f"Timestamps Above Baseline: {timestamps_above}")
        else:
            print(f"No linked NOAA event windows for {storm_system.storm_name}. Skipping duration calculation.")

    # After processing all storm systems, calculate the average duration for the hurricanes hazard
    hurricanes.calculate_average_eaglei_outage_duration()
    #print(f"Average duration per hurricane storm system of Eagle I outages above baseline: {hurricanes.average_duration_above_baseline}")
    #hurricanes.calculate_average_peak_outages()
    #hurricanes.calculate_percent_customers_affected()
    hurricanes.calculate_regression_coefficients()
    hurricanes.calculate_future_impact_coefficient()
    hurricanes.calculate_property_damage()
    hurricanes.calculate_probability()
    hurricanes.print_basic_info()
    
    #Save results
    pickle_path_for_hurricane = config['pickle_paths']['hurricanes']
    uti.save_to_pickle(hurricanes, pickle_path_for_hurricane)
    pickle_path_for_storm_systems = config['pickle_paths']['storm_systems']
    uti.save_to_pickle(storm_systems, pickle_path_for_storm_systems)

def main(args=None):
    """Main entry point of the program."""
    if args is None:
        args = sys.argv[1:]
    
    #Step 1: Check for pickles (pre-loaded and saved data ready to use)
    check_for_pickles()
    #Clean Data
    #NOAAEvent.clean_noaa_data() #not working, just did it manually
    #manually cleaned usgs data
    #Step 2: Load or create data source objects
    noaa_hurricane_events, noaa_lightning_events, noaa_winter_storms_events, noaa_flooding_events, noaa_tornado_events, noaa_wildfire_events, noaa_hail_events, noaa_strong_wind_events, eagle_i_events, fema_nri_data, usgs_data = load_data()
    #Step 3: Loading and creating natural hazards NOTE: Each natural hazard has one object for each subclass to store all the relevant variables in, the subclasses represent the entire risk, not individual events of the risk
    storm_systems, hurricanes, winter_storms, tornados, wildfires, flooding, hail, strong_winds, lightning, earthquakes, hazards = load_hazards()

    #Step 4: Assigning data from NOAA, filtering EagleI then assigning, and assigning FEMA NRI data to relevant hazards
    sort_and_assign_data(eagle_i_events, fema_nri_data, noaa_hurricane_events, noaa_lightning_events, 
                         noaa_winter_storms_events, noaa_flooding_events, noaa_tornado_events, noaa_wildfire_events, 
                         noaa_hail_events, noaa_strong_wind_events, hurricanes, lightning, winter_storms, flooding, 
                         tornados, wildfires, hail, strong_winds, earthquakes, hazards)

    #Step 5: Data processing for natural hazards - calculating EWMA, seasonal baseline, plotting results
    ewma_data, seasonal_baseline = data_processing_for_eaglei(eagle_i_events, noaa_hurricane_events, storm_systems)

    #Step 6: Data Analysis
    #process_hurricanes(ewma_data, seasonal_baseline, hurricanes, storm_systems)

    for hazard in hazards:
        if not isinstance(hazard, Hurricane | Earthquakes):  # Skip processing for Hurricane objects
            print(f"---------------------------------")
            #hazard.process_noaa_events()
            hazard.print_noaa_window_summary()
            print(f"---------------------------------")
            #hazard.calculate_average_eaglei_outage_duration(ewma_data, seasonal_baseline)
            #print(f"---------------------------------")
            #hazard.calculate_average_peak_outages(eagle_i_events)
            #hazard.calculate_percent_customers_affected()
            print(f"---------------------------------")
            hazard.calculate_property_damage()
            hazard.calculate_probability()
            #calc intensity coefficient
            #calc freq coefficient
            #calc FI coefficient
        if isinstance(hazard, Earthquakes):
            print("future processinging for earthquakes")
            #process usgs events - clean datetimes, pad times so they have an end datetime, find window overlaps similar to NOAA
            #print usgs window summary
            #calculate average eagle i outage duration - using usgs windows instead of noaa windows
            #calculate percent customers affected
            #calculate prop damage
            #calculate probability
            hazard.calculate_property_damage()
            hazard.calculate_probability()
            #calc intensity coefficient
            #calc freq coefficient
            #calc FI coefficient

    print("\nSummary of data for hazards:")
    for hazard in hazards:
        hazard.print_basic_info()        
    
    uti.save_natural_hazards_to_pickles(hazards)

if __name__ == "__main__":
    with uti.redirect_stdout_to_file(r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Terminal output\output50.txt"):
        main()