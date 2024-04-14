#NJSESP Project
#Lauren Eckert
#Version 2

import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import itertools
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL
import os
from DataSource import DataSource
from njsesp_config import config


class EagleIEvent(DataSource):
    def __init__(self, fips_code, county, state, sum, run_start_time):
        super().__init__()  # Initialize parent DataSource class
        self.fips_code = fips_code
        self.county = county
        self.state = state
        self.sum = sum
        self.run_start_time = run_start_time

    def extract_data(eagle_i_directory):
        """
        Extracts Eagle I events from a given Excel file.

        Parameters:
        file_path (str): Path to the Excel file containing Eagle I events.

        Returns:
        list: A list of EagleIEvent objects extracted from the file.
        # Initialize a list to store events outside of the for loop
        """
        events = []

        print(f"Starting to extract Eagle I events from directory: {eagle_i_directory}")
        for year in range(2014, 2023):
            file_path = os.path.join(eagle_i_directory, f"New Jersey {year}.xlsx")
            print(f"Looking for file: {file_path}")
            
            if os.path.exists(file_path):
                print(f"Processing file: {file_path}")
                df = pd.read_excel(file_path)

                # Log the number of rows found
                print(f"Found {len(df)} rows in {file_path}")

                # Iterate through the DataFrame and create a dictionary for each row
                for index, row in df.iterrows():
                    event = {
                        'fips_code': row['fips_code'],
                        'county': row['county'],
                        'state': row['state'],
                        'sum': row['sum'],
                        'run_start_time': row['run_start_time']
                    }
                    events.append(event)
                print(f"Added {len(df)} events from {file_path}")
            else:
                print(f"File not found: {file_path}")
        
        print(f"Extraction complete. {len(events)} total events extracted.")
        return events

    @staticmethod
    def filter_eagle_i_with_noaa(eagle_i_events, noaa_events, noaa_to_eaglei_mapping):
        # Preprocess NOAA events: Group by region and sort by start time
        noaa_events_processed = defaultdict(list)
        for noaa_event in noaa_events:
            region = noaa_to_eaglei_mapping.get(noaa_event.cz_name_str, noaa_event.cz_name_str)
            start_time = datetime.strptime(f"{noaa_event.begin_date} {noaa_event.begin_time:04d}", '%m/%d/%Y %H%M')
            end_time = datetime.strptime(f"{noaa_event.end_date} {noaa_event.end_time:04d}", '%m/%d/%Y %H%M')
            noaa_events_processed[region].append((start_time, end_time))

        for region in noaa_events_processed:
            noaa_events_processed[region].sort(key=lambda x: x[0])

        # Dictionary to keep track of the last checked index for NOAA events in each region
        last_checked_index_per_region = {region: 0 for region in noaa_events_processed}
        # After initializing the dictionary
        print("Regions available in NOAA data:", last_checked_index_per_region.keys())

        filtered_events = []
        non_match_counter = 0  # Counter for non-matching events
        missing_region_warnings = defaultdict(int)  # Count occurrences of missing region warnings

        for eagle_i_event in eagle_i_events:
            eagle_i_time = eagle_i_event['run_start_time']
            # Check if the time is a string and convert it to datetime if needed
            if isinstance(eagle_i_time, str):
                eagle_i_time = datetime.strptime(eagle_i_time, '%Y-%m-%d %H:%M:%S')
            elif isinstance(eagle_i_time, pd.Timestamp):
                eagle_i_time = eagle_i_time.to_pydatetime()

            region = eagle_i_event['county']

            # Check if the region is present in the processed NOAA events
            if region not in last_checked_index_per_region:
                missing_region_warnings[region] += 1
                if missing_region_warnings[region] % 1000 == 0:
                    print(f"Warning: No NOAA events found for the region '{region}' {missing_region_warnings[region]} times. Skipping this Eagle I event.")
                continue


            match_found = False
            for i in range(last_checked_index_per_region[region], len(noaa_events_processed[region])):
                noaa_event_start_time, noaa_event_end_time = noaa_events_processed[region][i]

                if eagle_i_time < noaa_event_start_time:
                    non_match_counter += 1
                    break  # No further NOAA events will match this Eagle I event

                if noaa_event_start_time <= eagle_i_time <= noaa_event_end_time:
                    filtered_events.append(eagle_i_event)  # Match found
                    match_found = True
                    break  # Move to next Eagle I event

                last_checked_index_per_region[region] = i  # Update last checked index

            if not match_found:
                non_match_counter += 1
                if non_match_counter % 500000 == 0:
                    print(f"Checked {non_match_counter} non-matching events so far.")

        print(f"Filtered {len(filtered_events)} matching Eagle I events from {len(eagle_i_events)} original events.")
        return filtered_events
    
    @staticmethod
    def assign_eagle_i_events_to_hazards(hazards, eagle_i_events, noaa_to_eaglei_mapping):
        for hazard in hazards:
            print(f"Processing {hazard.type_of_hazard}...")
            filtered_eagle_i_events = EagleIEvent.filter_eagle_i_with_noaa(
                eagle_i_events, hazard.noaa_events, noaa_to_eaglei_mapping
            )

            for event in filtered_eagle_i_events:
                hazard.add_eaglei_event(event)
            print(f"Added {len(filtered_eagle_i_events)} Eagle I events to {hazard.type_of_hazard}.")

    @staticmethod
    def print_samples(eagle_i_events, sample_size=30):
        """
        Prints a sample of Eagle I events, grouped by year.

        Parameters:
        eagle_i_events (list): List of EagleIEvent objects.
        max_events_to_print (int): Maximum number of events to print per year.
        """
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
            for event in events[:sample_size]:
                print(event)
            # Print a message if there are more events than the sample printed
            if len(events) > sample_size:
                print(f"... and {len(events) - sample_size} more events.")

    @staticmethod
    def get_unique_eagle_i_counties(eagle_i_events):
        """
        Returns a set of unique counties from a list of Eagle I events.

        Parameters:
        eagle_i_events (list): List of EagleIEvent objects.

        Returns:
        set: A set of unique county names.
        """
        unique_counties = set()

        for event in eagle_i_events:
            if event['county'] is not None:
                unique_counties.add(event['county'].strip())

        return unique_counties

    @staticmethod
    def plot_outages_over_time_per_year(eagle_i_events, ewma_data, seasonal_baseline, noaa_events, storm_systems, cap_value, show_noaa_events=True, show_storm_systems=True):
        """
        Plots the Eagle I outages over time for each year and optionally marks the start and end dates of NOAA events and storm systems.

        Parameters:
        eagle_i_events (list): A list of EagleIEvent objects.
        ewma_data (pd.Series): Exponentially weighted moving average data.
        seasonal_baseline (pd.Series): Seasonal baseline data.
        noaa_events (list): A list of NOAAEvent objects.
        storm_systems (list): A list of StormSystem objects.
        show_noaa_events (bool): Flag to show or hide NOAA event markings.
        show_storm_systems (bool): Flag to show or hide storm system periods.
        """
        # Check for terminal output directory
        plot_dir = config['directories']['outages_by_year_plot_directory']
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        # Define a color palette for storm systems
        storm_system_colors = itertools.cycle(['cyan', 'lightblue', 'skyblue', 'powderblue', 'lightcyan'])

        # Convert eagle_i_events to DataFrame and group by timestamp
        df = pd.DataFrame(eagle_i_events)
        df['run_start_time'] = pd.to_datetime(df['run_start_time'])
        grouped_data = df.groupby('run_start_time').sum().reset_index()

        # Group Eagle I events by year
        events_by_year = grouped_data.groupby(grouped_data['run_start_time'].dt.year)

        # Plot for each year
        for year, events in events_by_year:
            fig, ax = plt.subplots(figsize=(15, 7))

            # Sort events by run_start_time and plot
            times = events['run_start_time']
            outages = events['sum']
            ax.plot_date(times, outages, 'b-', label='Eagle I Outages')

            # Plot EWMA for the same year if available
            ewma_year = ewma_data[ewma_data.index.year == year]
            if not ewma_year.empty:
                ax.plot(ewma_year.index, ewma_year, 'r-', label='EWMA')

            # Plot Seasonal Baseline
            baseline_year = seasonal_baseline[seasonal_baseline.index.year == year]
            if not baseline_year.empty:
                ax.plot(baseline_year.index, baseline_year, 'g-', label='Seasonal Trendline')

            # Initialize flag for NOAA events label
            noaa_event_label_added = False

            # Highlight NOAA event periods if flag is True
            if show_noaa_events:
                for noaa_event in noaa_events:
                    if pd.to_datetime(noaa_event.begin_date).year == year:
                        if not noaa_event_label_added:
                            ax.axvspan(pd.to_datetime(noaa_event.begin_date), pd.to_datetime(noaa_event.end_date), color='orange', alpha=0.5, label='NOAA Event Period')
                            noaa_event_label_added = True
                        else:
                            ax.axvspan(pd.to_datetime(noaa_event.begin_date), pd.to_datetime(noaa_event.end_date), color='orange', alpha=0.5)

            # Highlight storm system periods if flag is True
            if show_storm_systems:
                for system in storm_systems:
                    if system.year == year:
                        color = next(storm_system_colors)
                        ax.axvspan(pd.to_datetime(system.start_date), pd.to_datetime(system.end_date), color=color, alpha=0.5, label=f'Storm: {system.storm_name}')

            # Plot the cap value as a horizontal line
            ax.axhline(y=cap_value, color='magenta', linestyle='--', label='Outlier Cap')

            # Formatting the plot
            # Set major locator to every 7 days
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=14))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate()
            plt.title(f'Outages over Time for {year}', fontsize=16)
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Outage Sum', fontsize=14)
            plt.legend()
            plt.tight_layout()
            plt.show()

            # Determine the version number for the file
            version = 1
            while os.path.exists(os.path.join(plot_dir, f"outages_by_year_{year}_v{version}.png")):
                version += 1

            # Save the plot
            fig.savefig(os.path.join(plot_dir, f"outages_by_year_{year}_v{version}.png"))
            plt.close(fig)

    @staticmethod
    def plot_zoomed_outages_around_storms(eagle_i_events, ewma_data, seasonal_baseline, noaa_events, storm_systems, cap_value, after_2014=True):
        # Check for terminal output directory
        plot_dir = config['directories']['outages_by_storm_system_plot_directory']
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        # Define the color for storm systems
        storm_system_color = 'cyan'

        # Convert eagle_i_events to DataFrame and group by timestamp
        df = pd.DataFrame(eagle_i_events)
        df['run_start_time'] = pd.to_datetime(df['run_start_time'])
        df_grouped = df.groupby('run_start_time').sum().reset_index()

        # Filter storm systems based on the year, if after_2014 is True
        if after_2014:
            storm_systems = [system for system in storm_systems if system.year > 2014]

        for system in storm_systems:
            # Determine the window for the storm system with 7-day padding
            start_window = system.start_date - pd.Timedelta(days=7)
            end_window = system.end_date + pd.Timedelta(days=7)

            # Prepare to plot
            fig, ax = plt.subplots(figsize=(15, 7))

            # Highlight the storm system window
            ax.axvspan(system.start_date, system.end_date, color=storm_system_color, alpha=0.3, label=f'Storm: {system.storm_name}')

            # Filter eagle_i_events within the window and plot
            filtered_events = df_grouped[(df_grouped['run_start_time'] >= start_window) & (df_grouped['run_start_time'] <= end_window)]
            ax.plot_date(filtered_events['run_start_time'], filtered_events['sum'], 'b-', label='Eagle I Outages')

            # Filter EWMA and Seasonal Baseline data for the window and plot if available
            ewma_filtered = ewma_data[(ewma_data.index >= start_window) & (ewma_data.index <= end_window)]
            baseline_filtered = seasonal_baseline[(seasonal_baseline.index >= start_window) & (seasonal_baseline.index <= end_window)]
            if not ewma_filtered.empty:
                ax.plot(ewma_filtered.index, ewma_filtered, 'r-', label='EWMA')
            if not baseline_filtered.empty:
                ax.plot(baseline_filtered.index, baseline_filtered, 'g-', label='Seasonal Baseline')

            # Highlight NOAA event periods with a single label
            noaa_event_added = False
            for noaa_event in noaa_events:
                start_noaa = pd.to_datetime(noaa_event.begin_date)
                end_noaa = pd.to_datetime(noaa_event.end_date)
                if start_window <= start_noaa <= end_window or start_window <= end_noaa <= end_window:
                    if not noaa_event_added:
                        ax.axvspan(start_noaa, end_noaa, color='orange', alpha=0.5, label='NOAA Event Period')
                        noaa_event_added = True
                    else:
                        ax.axvspan(start_noaa, end_noaa, color='orange', alpha=0.5)

            # Plot the EWMA cap value as a horizontal line
            ax.axhline(y=cap_value, color='magenta', linestyle='--', label='Outlier Cap')

            # Formatting the plot
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate()
            plt.title(f'Outages around {system.storm_name}', fontsize=16)
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Outage Sum', fontsize=14)
            plt.legend()
            plt.tight_layout()

            # Determine the version number for the file and save the plot
            version = 1
            filename = f"zoomed_outages_around_{system.storm_name}_{system.year}_v{version}.png"
            while os.path.exists(os.path.join(plot_dir, filename)):
                version += 1
                filename = f"zoomed_outages_around_{system.storm_name}_{system.year}_v{version}.png"
            
            fig.savefig(os.path.join(plot_dir, filename))
            plt.close(fig)
            print(f"Saved plot fir {filename}")

    @staticmethod
    def calculate_ewma(eagle_i_events, span=48):
        """
        Calculates the exponentially weighted moving average (EWMA) for the outage data.

        Parameters:
        eagle_i_events (list): List of EagleIEvent objects.
        span (int): The span for EWMA calculation.

        4 = 1 hour
        48 = 12 hour

        Returns:
        pd.Series: EWMA of outages.
        """
        print("Calculating EWMA for outage data...")
        df = pd.DataFrame(eagle_i_events)
        df['run_start_time'] = pd.to_datetime(df['run_start_time'])
        df.set_index('run_start_time', inplace=True)
        df = df.groupby(df.index).sum()  # Sum the outages for all counties at each timestamp
        ewma = df['sum'].ewm(span=span, adjust=False).mean()
        print("EWMA calculation completed.")
        return ewma
    
    @staticmethod
    def calculate_seasonal_baseline(ewma, decomposition_period=2920):
        """
        Applies seasonal decomposition to the EWMA data to extract the baseline.

        Parameters:
        ewma (pd.Series): EWMA data.
        decomposition_period (int): The number of observations in each cycle. 
        
            For annual seasonality with 15-minute data, this is set to 35040.
            For quarterly, 8760.
            For monthly, 2920.

        Returns:
        pd.Series: Seasonal baseline extracted from seasonal decomposition.
        """
        print("Applying seasonal decomposition to extract baseline...")
        
        # Ensure ewma is a Series with a datetime index
        if not isinstance(ewma.index, pd.DatetimeIndex):
            print("EWMA data index must be a DatetimeIndex.")
            return

        # Check if the series has enough data points for decomposition
        if len(ewma) < 2 * decomposition_period:
            print(f"EWMA series does not have enough data points for seasonal decomposition. Required: {2 * decomposition_period}, Found: {len(ewma)}")
            return
        
        # Apply seasonal decomposition
        decomposition = sm.tsa.seasonal_decompose(ewma, model='additive', period=decomposition_period)
        
        # Extract and return the trend component as the baseline
        baseline = decomposition.trend

        print("Seasonal decomposition and baseline extraction completed.")
        return baseline

    @staticmethod
    def cap_ewma_and_get_cap_value(ewma_data, multiplier=1):
        """
        Caps the EWMA data based on the IQR method for outlier detection and returns the capped data along with the cap value.

        Parameters:
        ewma_data (pd.Series): The exponentially weighted moving average data.
        multiplier (float): The multiplier for the IQR to define what is considered an outlier.

        Returns:
        pd.Series: The capped EWMA data.
        float: The cap value used.
        """
        q1 = ewma_data.quantile(0.25)
        q3 = ewma_data.quantile(0.75)
        iqr = q3 - q1
        cap_value = q3 + (iqr * multiplier)

        # Cap the data
        capped_ewma = ewma_data.clip(upper=cap_value)

        return capped_ewma, cap_value
    
    @staticmethod
    def print_df_sample_data(data, sample_size=100):
        """
        Prints a sample of the calculated data.

        Parameters:
        data (pd.Series or pd.DataFrame): The data to print samples from.
        sample_size (int): The number of samples to print.
        """
        print("Sample Data:")
        if isinstance(data, pd.DataFrame):
            print(data.head(sample_size))
        elif isinstance(data, pd.Series):
            print(data.head(sample_size).to_frame())
        else:
            print("Data format not recognized.")

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