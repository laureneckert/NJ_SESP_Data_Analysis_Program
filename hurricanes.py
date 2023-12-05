#Lauren Eckert
#NJSESP Project for Junior Clinic

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

    def add_noaa_event(self, noaa_event):
        self.noaa_events.append(noaa_event)

    def add_eaglei_event(self, eaglei_event):
        self.eaglei_events.append(eaglei_event)
