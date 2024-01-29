#NJSESP Project
#Lauren Eckert
#Version 2

#Hurricane class
from natural_hazard import NaturalHazard
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class Hurricane(NaturalHazard):
    def __init__(self, type_of_hazard='hurricanes'):
        super().__init__(type_of_hazard)
        self.storm_systems = []  # List to store individual StormSystem objects

    def add_storm_system(self, storm_system):
        self.storm_systems.append(storm_system)

    def print_basic_info(self):
        print(f"Hurricane Hazard Summary:")
        print(f"Type of Hazard: {self.type_of_hazard}")
        print(f"Total Property Damage: {self.total_property_damage}")
        print(f"Total Outages Sum: {self.total_outages_sum}")
        print(f"Risk Score: {self.risk_score}")
        print(f"No. of Associated Storm Systems: {len(self.storm_systems)}")

        # Print sample storm systems
        sample_size = min(5, len(self.storm_systems))  # Adjust sample size as needed
        print(f"\nSample Storm Systems:")
        for i in range(sample_size):
            storm = self.storm_systems[i]
            storm.print_basic_info()  # Call the storm_system's method

    @staticmethod
    def create_default_instances():
        # Create a default instance of Hurricane with default values
        default_hurricane = Hurricane()

        # Initialize inherited attributes from NaturalHazard
        default_hurricane.NRI_data_fields = {}  # Default NRI data fields values
        default_hurricane.noaa_events = []  # Default list of NOAA events
        default_hurricane.noaa_event_count = 0  # Default NOAA event count
        default_hurricane.unique_noaa_regions = set()  # Default set of unique NOAA regions
        default_hurricane.unique_noaa_event_types = set()  # Default set of unique NOAA event types
        default_hurricane.total_outages_sum = 0  # Default total outages sum
        default_hurricane.outage_total_by_county = {}  # Default outage total by county
        default_hurricane.eaglei_events = []  # Default list of Eagle I events
        default_hurricane.unique_eaglei_regions = set()  # Default set of unique Eagle I regions
        default_hurricane.total_duration_eaglei = 0  # Default total duration of Eagle I outages
        default_hurricane.outage_duration_by_county = {}  # Default outage duration by county

        # Initialize inherited attributes from Hazard
        default_hurricane.total_property_damage = 0.0  # Default total property damage
        default_hurricane.property_damage_by_county = {}  # Default property damage by county
        default_hurricane.total_property_damage_annualized = 0.0  # Default annualized property damage
        default_hurricane.percent_customers_affected = 0.0  # Default percent customers affected
        default_hurricane.customers_affected_sum = 0  # Default sum of customers affected
        default_hurricane.total_time_duration_customer_affected = 0.0  # Default total time duration of customers affected
        default_hurricane.time_duration_customer_affected_annualized = 0.0  # Default annualized time duration of customers affected
        default_hurricane.historical_frequency = 0.0  # Default historical frequency
        default_hurricane.future_impact_coefficient = 0.0  # Default future impact coefficient
        default_hurricane.frequency_coefficient = 0.0  # Default frequency coefficient
        default_hurricane.impact_coefficient = 0.0  # Default impact coefficient
        default_hurricane.risk_score = 0.0  # Default risk score

        # Add other default values as required

        return default_hurricane
    
    def calculate_average_peak_outages(self):
        total_peak_outages = 0
        if not self.storm_systems:
            print("No storm systems available.")
            self.customers_affected_sum = 0
            return

        print(f"Calculating peak outages for {len(self.storm_systems)} storm systems...")
        for storm_system in self.storm_systems:
            storm_outages = storm_system.calculate_peak_outages(self.eaglei_events)
            print(f"Total peak outages for {storm_system.storm_name}: {storm_outages}")
            total_peak_outages += storm_outages

        self.customers_affected_sum = total_peak_outages / len(self.storm_systems)
        print(f"Average Peak Outages: {self.customers_affected_sum}")

    def calculate_regression_coefficients(self):
        # Preparing data for Frequency Coefficient
        year_frequency = {}
        year_intensity_sum = {}
        year_intensity_count = {}

        for storm in self.storm_systems:
            year = storm.start_date.year
            year_frequency[year] = year_frequency.get(year, 0) + 1
            year_intensity_sum[year] = year_intensity_sum.get(year, 0) + storm.intensity
            year_intensity_count[year] = year_intensity_count.get(year, 0) + 1

        years = []
        frequencies = []
        average_intensities = []

        for year in year_frequency:
            years.append(year)
            frequencies.append(year_frequency[year])

            if year_intensity_count[year] > 0:
                average_intensity = year_intensity_sum[year] / year_intensity_count[year]
                average_intensities.append(average_intensity)
            else:
                # Handle years with no storm systems
                print(f"No storm systems recorded for the year {year}")
                average_intensities.append(0)  # Or choose to handle this differently

        # Linear Regression for Frequency
        if years:
            slope_freq, intercept, r_value, p_value, std_err = stats.linregress(years, frequencies)
            self.frequency_coefficient = slope_freq + 1

            # Plotting Frequency
            plt.figure(figsize=(10, 5))
            plt.scatter(years, frequencies, color='blue')
            plt.plot(years, intercept + slope_freq * np.array(years), 'r')
            plt.title('Storm Frequency Over Time')
            plt.xlabel('Year')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.show()
        else:
            print("No data available for frequency analysis.")

        # Linear Regression for Average Intensity
        if years:
            slope_intensity, intercept, r_value, p_value, std_err = stats.linregress(years, average_intensities)
            self.intensity_coefficient = slope_intensity + 1

            # Plotting Intensity
            plt.figure(figsize=(10, 5))
            plt.scatter(years, average_intensities, color='green')
            plt.plot(years, intercept + slope_intensity * np.array(years), 'r')
            plt.title('Average Storm Intensity Over Time')
            plt.xlabel('Year')
            plt.ylabel('Average Intensity')
            plt.grid(True)
            plt.show()
        else:
            print("No data available for intensity analysis.")

        return self.frequency_coefficient, self.intensity_coefficient
    
    def analyze_hurricane_data(self):
        hazard_prefix = "HRCN"
        total_property_damage = self.calculate_property_damage(hazard_prefix)
        annualized_frequency = self.calculate_probability(hazard_prefix)

        print(f"Total Property Damage for Hurricanes: {total_property_damage}")
        print(f"Annualized Frequency (Probability) of Hurricanes: {annualized_frequency}")

