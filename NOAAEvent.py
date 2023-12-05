#Lauren Eckert
#NJSESP Project for Junior Clinic

#Libraries

#imports from other package files

#NOAA events class
class NOAAEvent:
    def __init__(self, event_id, cz_name_str, begin_location, begin_date, begin_time, event_type, magnitude, tor_f_scale, deaths_direct,
                 injuries_direct, damage_property_num, damage_crops_num, state_abbr, cz_timezone, magnitude_type, episode_id, cz_type,
                 cz_fips, wfo, injuries_indirect, deaths_indirect, source, flood_cause, tor_length, tor_width, begin_range, begin_azimuth,
                 end_range, end_azimuth, end_location, end_date, end_time, begin_lat, begin_lon, end_lat, end_lon, event_narrative, episode_narrative, absolute_rownumber, filename=None, line_number=None):
        self.event_id = event_id
        self.cz_name_str = cz_name_str
        self.begin_location = begin_location
        self.begin_date = begin_date
        self.begin_time = begin_time
        self.event_type = event_type
        self.magnitude = magnitude
        self.tor_f_scale = tor_f_scale
        self.deaths_direct = deaths_direct
        self.injuries_direct = injuries_direct
        self.damage_property_num = damage_property_num
        self.damage_crops_num = damage_crops_num
        self.state_abbr = state_abbr
        self.cz_timezone = cz_timezone
        self.magnitude_type = magnitude_type
        self.episode_id = episode_id
        self.cz_type = cz_type
        self.cz_fips = cz_fips
        self.wfo = wfo
        self.injuries_indirect = injuries_indirect
        self.deaths_indirect = deaths_indirect
        self.source = source
        self.flood_cause = flood_cause
        self.tor_length = tor_length
        self.tor_width = tor_width
        self.begin_range = begin_range
        self.begin_azimuth = begin_azimuth
        self.end_range = end_range
        self.end_azimuth = end_azimuth
        self.end_location = end_location
        self.end_date = end_date
        self.end_time = end_time
        self.begin_lat = begin_lat
        self.begin_lon = begin_lon
        self.end_lat = end_lat
        self.end_lon = end_lon
        self.event_narrative = event_narrative
        self.episode_narrative = episode_narrative
        self.absolute_rownumber = absolute_rownumber
        self.filename = filename
        self.line_number = line_number       

def get_unique_noaa_regions(hurricanes):
    unique_regions = set()
    for hurricane in hurricanes:
        for noaa_event in hurricane.noaa_events:
            # Ensure that cz_name_str is a string before stripping
            if isinstance(noaa_event.cz_name_str, str):
                unique_regions.add(noaa_event.cz_name_str.strip())
            else:
                # Handle non-string cz_name_str (convert to string or handle differently)
                unique_regions.add(str(noaa_event.cz_name_str))
    return unique_regions

def count_noaa_events_missing_cz_name(hurricanes):
    count = 0
    for hurricane in hurricanes:
        for event in hurricane.noaa_events:
            # Check if cz_name_str is empty or None
            if not event.cz_name_str or (isinstance(event.cz_name_str, str) and event.cz_name_str.strip() == ""):
                count += 1
    return count

def print_specific_noaa_events(hurricanes, cz_name_str_values):
    for hurricane in hurricanes:
        for event in hurricane.noaa_events:
            if str(event.cz_name_str) in cz_name_str_values:
                print(f"File: {event.filename}, Line: {event.line_number}, Event ID: {event.event_id}, CZ Name: {event.cz_name_str}")