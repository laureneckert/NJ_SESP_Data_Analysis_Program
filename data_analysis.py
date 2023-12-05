#data_analysis.py

# Imports
from hurricanes import Hurricane
from NOAAEvent import NOAAEvent
from EagleIEvent import EagleIEvent

def print_hurricane_summaries(hurricanes):
    """
    Prints a summary of all attributes for each hurricane in the provided list.

    Parameters:
    hurricanes (list): A list of Hurricane objects.
    """
    for hurricane in hurricanes:
        print(f"Hurricane Name: {hurricane.storm_name}")
        print(f"Year: {hurricane.year}")
        print(f"Start Date: {hurricane.start_date}")
        print(f"End Date: {hurricane.end_date}")
        print(f"Storm Type: {hurricane.storm_type}")
        print(f"Comment: {hurricane.comment}")
        print(f"Occurrence: {hurricane.occurrence}")
        print("NOAA Events:")
        for event in hurricane.noaa_events:
            print(f"  - Event ID: {event.event_id}, Type: {event.event_type}, Date: {event.begin_date}")
        print("Eagle I Events:")
        for event in hurricane.eaglei_events:
            print(f"  - County: {event['county']}, Start Time: {event['run_start_time']}")
        print("\n")
