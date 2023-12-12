# Lauren Eckert
# NJSESP Project for Junior Clinic
# Driver Script for Hurricane Data Processing

import os
import pickle
import data_processing as dp
import utilities as uti
import data_analysis as da


from EagleIEvent import noaa_to_eaglei_mapping
from config import config

# Ensure the pickle directory exists
if not os.path.exists(config['pickle_directory']):
    os.makedirs(config['pickle_directory'])

# Load or create hurricane objects
hurricanes = dp.load_or_create_hurricanes(config['hurricanes_excel_file_path'], config['pickle_directory'])

# Load or add NOAA events
dp.load_or_add_noaa_events(hurricanes, config['noaa_files_directory'], config['noaa_pickle_path'])

# Load or add Eagle I events
eagle_i_events = dp.load_or_add_eagle_i_events(config['eagle_i_directory'], config['eagle_i_pickle_path'])

# Call the function with your data
#dp.print_data_samples(hurricanes, eagle_i_events)

# Flag to control processing of Eagle I events and updating hurricanes
process_eaglei_events = False  # Set to True to enable processing

if process_eaglei_events:
    # Link Eagle I events to NOAA events
    dp.link_eaglei_to_noaa(hurricanes, eagle_i_events, noaa_to_eaglei_mapping)

    # Save the updated hurricane objects to a pickle file
    uti.save_to_pickle(hurricanes, config['hurricane_pickle_path'])

    print("Updated hurricane objects have been saved back to the pickle file.")
else:
    print("Processing of Eagle I events and updating of hurricane objects is skipped.")

calculate_and_update_hurricane_stats = False # Set to True to enable processing

if calculate_and_update_hurricane_stats:
    # Assuming 'hurricanes' is your list of Hurricane objects
    for hurricane in hurricanes:
        hurricane.calculate_statistics()

    with open(config['hurricane_pickle_path'], 'wb') as file:
        pickle.dump(hurricanes, file)

    print(f"Updated hurricane objects have been saved to {config['hurricane_pickle_path']}.")
else:
    print(f"Calculating and updating individual hurricane stats skipped.")

aggregate_stats = da.calculate_aggregate_hurricane_statistics(hurricanes)

#"""
file_path = r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Terminal output\terminal_output3.txt"
with uti.redirect_stdout_to_file(file_path):
    # All print statements inside this block will be redirected to the specified file
    for hurricane in hurricanes:
        hurricane.print_statistics()    
    print("*"*30)
    da.print_aggregate_stats(aggregate_stats)
    # Add your function calls or any other code that produces terminal output here

#"""

# Plotting Property Damage
da.plot_property_damage_over_time(hurricanes)

# Plotting Outages
da.plot_outages_over_time(hurricanes)