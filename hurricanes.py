#Lauren Eckert
#NJSESP Project for Junior Clinic

from datetime import datetime, timedelta
from EagleIEvent import EagleIEvent
from NOAAEvent import NOAAEvent

#Hurricane class
class Hurricane:
    def __init__(self, year, start_date, end_date, storm_name, occurrence, storm_type, comment):
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
        self.storm_name = storm_name
        self.occurrence = occurrence #default to 1 if not specified
        self.storm_type = storm_type
        self.comment = comment
        self.noaa_events = []  # List to store NOAA events
        self.eaglei_events = []  # List to store Eagle I events

        # Attributes for calculated statistics
        self.noaa_event_count = 0
        self.total_property_damage = 0
        self.unique_noaa_regions = set()
        self.unique_noaa_event_types = set()
        self.total_outages_sum = 0
        self.unique_eaglei_regions = set()
        self.total_duration_eaglei = 0

    def add_noaa_event(self, noaa_event):
        self.noaa_events.append(noaa_event)

    def add_eaglei_event(self, eaglei_event):
        self.eaglei_events.append(eaglei_event)

    def find_hurricane_by_name_and_occurrence(hurricanes, storm_name, occurrence):
        for hurricane in hurricanes:
            if hurricane.storm_name == storm_name and hurricane.occurrence == occurrence:
                print(f"Match found for {storm_name} with occurrence {occurrence}")
                return hurricane
        print(f"No match found for {storm_name} with occurrence {occurrence}")
        return None

    def calculate_statistics(self):
        # Number of NOAA events
        self.noaa_event_count = len(self.noaa_events)

        # Total Property Damage
        self.total_property_damage = sum(event.damage_property_num for event in self.noaa_events)

        # Unique NOAA Regions
        self.unique_noaa_regions = {event.cz_name_str for event in self.noaa_events}

        # Unique NOAA Event Types
        self.unique_noaa_event_types = {event.event_type for event in self.noaa_events}

        # Total Sum of Outages
        self.total_outages_sum = sum(event['sum'] for event in self.eaglei_events if 'sum' in event)

        # Unique Eagle I Regions
        self.unique_eaglei_regions = {event['county'] for event in self.eaglei_events if 'county' in event}

        # Calculate total duration of Eagle I outages in hours
        self.total_duration_eaglei = self.calculate_total_eaglei_outage_duration()


    def calculate_total_eaglei_outage_duration(self):
        # Sum of outages in Eagle I events
        total_outages = sum(event['sum'] for event in self.eaglei_events if 'sum' in event)

        # Convert the total sum of outages to duration in minutes (each unit is 15 minutes)
        total_duration_minutes = total_outages * 15

        # Convert minutes to hours
        total_duration_hours = total_duration_minutes / 60

        return total_duration_hours

    def print_statistics(self):
        print(f"\nStats for Hurricane: {self.storm_name}")
        print("-" * 30)
        print(f"No. of NOAA Events: {self.noaa_event_count}")
        print(f"Total Property Damage: ${self.total_property_damage:,}")
        print(f"Unique NOAA Regions: {', '.join(self.unique_noaa_regions)}")
        print(f"Unique NOAA Event Types: {', '.join(self.unique_noaa_event_types)}")
        print(f"Total Sum of Outages: {self.total_outages_sum}")
        print(f"Unique Eagle I Regions: {', '.join(self.unique_eaglei_regions)}")
        print(f"Total Duration of Eagle I Events (Hours): {self.total_duration_eaglei:.2f}")
        print("-" * 30)