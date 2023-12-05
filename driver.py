# Lauren Eckert
# NJSESP Project for Junior Clinic
# Driver Script for Hurricane Data Processing

import os
import pickle
import data_processing as dp
import utilities as uti

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
dp.print_data_samples(hurricanes, eagle_i_events)

# Flag to control processing of Eagle I events and updating hurricanes
process_eaglei_events = False  # Set to True to enable processing

if process_eaglei_events:
    # Link Eagle I events to NOAA events
    dp.link_eaglei_to_noaa(hurricanes, eagle_i_events, noaa_to_eaglei_mapping)

    # Save the updated hurricane objects to a pickle file
    hurricane_pickle_path = os.path.join(config['pickle_directory'], 'hurricane_objects.pkl')
    uti.save_to_pickle(hurricanes, hurricane_pickle_path)

    print("Updated hurricane objects have been saved back to the pickle file.")
else:
    print("Processing of Eagle I events and updating of hurricane objects is skipped.")
