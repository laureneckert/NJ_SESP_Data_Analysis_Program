#Lauren Eckert
#NJSESP Project for Junior Clinic

#Libraries
import pandas as pd

#Eagle I events class
class EagleIEvent:
    def __init__(self, fips_code, county, state, sum, run_start_time):
        self.fips_code = fips_code
        self.county = county
        self.state = state
        self.sum = sum
        self.run_start_time = run_start_time

def sampleEagleIEvents(eagle_i_events, max_events_to_print=30):
    # Convert event dates to datetime if they are not already
    for event in eagle_i_events:
        if isinstance(event['run_start_time'], str):
            event['run_start_time'] = pd.to_datetime(event['run_start_time'])

    # Group events by year
    events_by_year = {}
    for event in eagle_i_events:
        year = event['run_start_time'].year
        if year in events_by_year:
            events_by_year[year].append(event)
        else:
            events_by_year[year] = [event]

    # Print a sample of events for each year
    for year, events in events_by_year.items():
        print(f"\nYear: {year} - Total events: {len(events)}")
        # Print only the first few events as a sample
        for event in events[:max_events_to_print]:
            print(event)
        # Print a message if there are more events than the sample printed
        if len(events) > max_events_to_print:
            print(f"... and {len(events) - max_events_to_print} more events.")

def get_unique_eagle_i_counties(eagle_i_events):
    unique_counties = set()

    for event in eagle_i_events:
        if event['county'] is not None:
            unique_counties.add(event['county'].strip())

    return unique_counties

# Mapping of NOAA regions to Eagle I counties
noaa_to_eaglei_mapping = {
    "ATLANTIC CO.": "Atlantic",
    "BERGEN (ZONE)": "Bergen",
    "BERGEN CO.": "Bergen",
    "BURLINGTON CO.": "Burlington",
    "CAMDEN (ZONE)": "Camden",
    "CAMDEN CO.": "Camden",
    "CAPE MAY CO.": "Cape May",
    "CUMBERLAND (ZONE)": "Cumberland",
    "CUMBERLAND CO.": "Cumberland",
    "EASTERN ATLANTIC (ZONE)": "Atlantic",
    "EASTERN BERGEN (ZONE)": "Bergen",
    "EASTERN CAPE MAY (ZONE)": "Cape May",
    "EASTERN ESSEX (ZONE)": "Essex",
    "EASTERN MONMOUTH (ZONE)": "Monmouth",
    "EASTERN OCEAN (ZONE)": "Ocean",
    "EASTERN PASSAIC (ZONE)": "Passaic",
    "EASTERN UNION (ZONE)": "Union",
    "ESSEX (ZONE)": "Essex",
    "ESSEX CO.": "Essex",
    "GLOUCESTER (ZONE)": "Gloucester",
    "GLOUCESTER CO.": "Gloucester",
    "HUDSON (ZONE)": "Hudson",
    "HUDSON CO.": "Hudson",
    "HUNTERDON (ZONE)": "Hunterdon",
    "HUNTERDON CO.": "Hunterdon",
    "MERCER (ZONE)": "Mercer",
    "MERCER CO.": "Mercer",
    "MIDDLESEX (ZONE)": "Middlesex",
    "MIDDLESEX CO.": "Middlesex",
    "MONMOUTH CO.": "Monmouth",
    "MORRIS (ZONE)": "Morris",
    "MORRIS CO.": "Morris",
    "NORTHWESTERN BURLINGTON (ZONE)": "Burlington",
    "OCEAN CO.": "Ocean",
    "PASSAIC CO.": "Passaic",
    "SALEM (ZONE)": "Salem",
    "SALEM CO.": "Salem",
    "SOMERSET (ZONE)": "Somerset",
    "SOMERSET CO.": "Somerset",
    "SOUTHEASTERN BURLINGTON (ZONE)": "Burlington",
    "SUSSEX (ZONE)": "Sussex",
    "SUSSEX CO.": "Sussex",
    "UNION (ZONE)": "Union",
    "UNION CO.": "Union",
    "WARREN (ZONE)": "Warren",
    "WARREN CO.": "Warren",
    "WESTERN ATLANTIC (ZONE)": "Atlantic",
    "WESTERN BERGEN (ZONE)": "Bergen",
    "WESTERN CAPE MAY (ZONE)": "Cape May",
    "WESTERN ESSEX (ZONE)": "Essex",
    "WESTERN MONMOUTH (ZONE)": "Monmouth",
    "WESTERN OCEAN (ZONE)": "Ocean",
    "WESTERN PASSAIC (ZONE)": "Passaic",
    "WESTERN UNION (ZONE)": "Union"
}