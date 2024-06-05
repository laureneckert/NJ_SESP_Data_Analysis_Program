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
            'base_uncleaned_data_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\uncleaned",
            'base_cleaned_data_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA",
            #all cleaned noaa data below
            'noaa_hurricanes_files_directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\hurricanes",
            'noaa_lightning_files_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\lightning",
            'noaa_winter_storms_files_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\winter_storms",
            'noaa_tornados_files_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\tornados",
            'noaa_wildfires_files_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\wildfires",
            'noaa_flooding_files_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\flooding",
            'noaa_hail_files_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\hail",
            'noaa_strong_winds_files_directory' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NOAA\strong_winds",
        },
        'eagle_i': {
            'directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\eaglei_outages",
        },
        'fema_nri': {
            'file_path': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\NRI_Table_Counties_NewJersey\NRI_Table_Counties_NewJersey.csv",
        },
        'usgs' : {
            'file_path' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\other_natural_hazard_info\usgs_nj_earthquakes_2014_2022.csv"
        }
    },
    'directories': {
        'pickle_directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles",
        'outages_by_year_plot_directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Terminal output\outages visualizations\by year",
        'outages_by_storm_system_plot_directory': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Terminal output\outages visualizations\by storm",    
    },
    'pickle_paths': {
        #data sources - noaa
        'noaa_hurri': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\hurricane_noaa_events.pkl",
        'noaa_lightning' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\lightning_noaa_events.pkl",
        'noaa_winter_storms' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\winter_storms_noaa_events.pkl",
        'noaa_tornados': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\tornado_noaa_events.pkl",
        'noaa_wildfires': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\wildfires_noaa_events.pkl",        
        'noaa_flooding': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\flooding_noaa_events.pkl",
        'noaa_hail': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\hail_noaa_events.pkl",
        'noaa_strong_winds': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\strong_wind_noaa_events.pkl",
        #data sources - other
        'eagle_i': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\eagle_i_events.pkl",
        'fema_nri': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\FEMA_NRI_data.pkl",
        'usgs' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\usgs_data.pkl",

        #objects
        'hurricanes': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\hurricane_objects.pkl",
        'storm_systems': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\storm_systems_objects.pkl",
        'lightning' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\lightning_objects.pkl",
        'winter_storms' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\winter_storms_objects.pkl",
        'tornados' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\tornado_objects.pkl",
        'wildfires' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\wildfires_objects.pkl",
        'flooding' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\flooding_objects.pkl",
        'hail' : r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\hail_objects.pkl",
        'strong_winds': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\strong_wind_objects.pkl",
        'earthquakes': r"C:\Users\laure\Dropbox\School\BSE\Coursework\23 Fall\JuniorClinic\risk assessment\NJSESP_Data_Analysis\Data\pickles\earthquakes_objects.pkl"
    }
}

def get_pickle_path(hazard_type):
    """Returns the pickle path for a given hazard type."""
    return config['pickle_paths'].get(hazard_type.lower())