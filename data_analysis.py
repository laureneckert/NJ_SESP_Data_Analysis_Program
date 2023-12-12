#data_analysis.py

# Imports
from hurricanes import Hurricane
from NOAAEvent import NOAAEvent
from EagleIEvent import EagleIEvent
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


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
        print("NOAA Events: ", len(hurricane.noaa_events))
        for event in hurricane.noaa_events:
            print(f"  - Event ID: {event.event_id}, Type: {event.event_type}, Date: {event.begin_date}")
        print("Eagle I Events: ", len(hurricane.eaglei_events))
        for event in hurricane.eaglei_events:
            print(f"  - County: {event['county']}, Start Time: {event['run_start_time']}")
        print("\n")

def calculate_aggregate_hurricane_statistics(hurricanes):
    total_property_damage = 0
    total_eaglei_outage_hours = 0

    # Summing up the total property damage and total Eagle I outage hours
    for hurricane in hurricanes:
        total_property_damage += hurricane.total_property_damage
        total_eaglei_outage_hours += hurricane.total_duration_continuous_eaglei

    # Calculating annualized values using class variables
    noaa_years = NOAAEvent.END_YEAR - NOAAEvent.START_YEAR + 1
    eaglei_years = EagleIEvent.END_YEAR - EagleIEvent.START_YEAR + 1

    annualized_property_damage = total_property_damage / noaa_years if noaa_years > 0 else 0
    annualized_eaglei_outage_hours = total_eaglei_outage_hours / eaglei_years if eaglei_years > 0 else 0

    return {
        'total_property_damage': total_property_damage,
        'total_eaglei_outage_hours': total_eaglei_outage_hours,
        'annualized_property_damage': annualized_property_damage,
        'annualized_eaglei_outage_hours': annualized_eaglei_outage_hours
    }

def print_aggregate_stats(aggregate_stats):
    print("\nAggregate Hurricane Statistics:")
    print("-" * 40)
    
    print(f"Total Property Damage: ${aggregate_stats['total_property_damage']:,}")
    print(f"Total Eagle I Outage Hours: {aggregate_stats['total_eaglei_outage_hours']:.2f} hours")

    print("\nAnnualized Statistics:")
    print(f"Property Damage (Annualized for {NOAAEvent.START_YEAR}-{NOAAEvent.END_YEAR}): ${aggregate_stats['annualized_property_damage']:,}/year")
    print(f"Eagle I Outage Hours (Annualized for {EagleIEvent.START_YEAR}-{EagleIEvent.END_YEAR}): {aggregate_stats['annualized_eaglei_outage_hours']:.2f} hours/year")

    print("-" * 40)
    print("Note: Annualized statistics are averaged over the respective data ranges for NOAA and Eagle I datasets.")
    print("-" * 40)

def plot_property_damage_over_time(hurricanes):
    property_damage_by_year = {}
    for hurricane in hurricanes:
        year = hurricane.year
        property_damage_by_year[year] = property_damage_by_year.get(year, 0) + hurricane.total_property_damage

    years = sorted(property_damage_by_year.keys())
    total_damages = [property_damage_by_year.get(year, 0) for year in years]

    plt.figure(figsize=(14, 7))
    bars = plt.bar(years, total_damages, color='royalblue')

    plt.title("Hurricane Related Property Damage Over Time (2000 to 2022)", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Total Property Damage (USD)", fontsize=14)

    plt.yscale('log')
    # Add data source annotation
    plt.text(0.95, 0.01, 'Data source: NOAA Weather Events Database', fontsize=9, color='gray', ha='right', va='bottom', transform=plt.gcf().transFigure)
    
    # Label each bar with non-zero value
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:  # Only label bars with non-zero values
            plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{int(yval):,}', 
                     ha='center', va='bottom', fontsize=8, color='black')

    plt.xticks(years, rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which="both", axis='y', linestyle='--', linewidth=0.5, color='grey')
    plt.show()

def plot_outages_over_time(hurricanes):
    outages_by_year = {}
    for hurricane in hurricanes:
        year = hurricane.year
        if year >= 2014:  # Starting year for outage data
            outages_by_year[year] = outages_by_year.get(year, 0) + hurricane.total_duration_eaglei

    years = sorted(outages_by_year.keys())
    total_outages = [outages_by_year.get(year, 0) for year in years]

    plt.figure(figsize=(14, 7))
    bars = plt.bar(years, total_outages, color='tomato')

    plt.title("Hurricane Related Outages Duration Over Time (2014-2022)", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Total Outages Duration (Hours)", fontsize=14)

    plt.yscale('log')
    
    # Add data source annotation
    plt.text(0.95, 0.01, 'Data source: Eagle I Outages Database', fontsize=9, color='gray', ha='right', va='bottom', transform=plt.gcf().transFigure)

    # Label each bar with non-zero value
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:  # Only label bars with non-zero values
            plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{int(yval):,}', 
                     ha='center', va='bottom', fontsize=8, color='black')

    plt.xticks(years, rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which="both", axis='y', linestyle='--', linewidth=0.5, color='grey')
    plt.show()
