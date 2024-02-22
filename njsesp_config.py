# NJSESP Project
# Lauren Eckert
# Version 2

# File paths configuration
config = {
    'data_paths': {
        'hurricanes': {
            'storm_systems_file': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\other_natural_hazard_info\hurricanes.xlsx",
        },
        'noaa' :   {
            'noaa_hurricanes_files_directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\hurricanes",
        },
        'eagle_i': {
            'directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\eaglei_outages",
        },
        'fema_nri': {
            'file_path': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NRI_Table_Counties_NewJersey\NRI_Table_Counties_NewJersey.csv",
        }
    },
    'directories': {
        'pickle_directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles",
        'outages_plot_directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Terminal output\outages visualizations",
    },
    'pickle_paths': {
        #data sources
        'noaa_hurri': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\hurricane_noaa_events.pkl",
        'eagle_i': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\eagle_i_events.pkl",
        'fema_nri': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\FEMA_NRI_data.pkl",
        
        #objects
        'hurricanes': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\hurricane_objects.pkl",
        'storm_systems': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\storm_systems_objects.pkl",
    }
}

def get_pickle_path(hazard_type):
    """Returns the pickle path for a given hazard type."""
    return config['pickle_paths'].get(hazard_type.lower())