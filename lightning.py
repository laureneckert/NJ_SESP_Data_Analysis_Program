#NJSESP Project
#Lauren Eckert
#Version 2

#Lightning class
from natural_hazard import NaturalHazard
from FEMA_NRI_data import FEMA_NRI_data
import utilities as uti
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

class Lightning(NaturalHazard):
    def __init__(self, type_of_hazard='lightning'):
        super().__init__(type_of_hazard)

    def calculate_probability(self):
        """
        Calculates the cumulative annualized frequency (probability) of lightning by summing
        the annualized frequencies from all counties under each relevant prefix.

        Returns:
        float: The cumulative annualized frequency of lightning across all relevant counties and prefixes.
        """
        total_frequency = 0.0
        
        # Fetching the prefixes specifically related to the 'lightning' hazard type
        hazard_prefixes = FEMA_NRI_data.hazard_to_fema_prefix.get(self.type_of_hazard, [])

        if not hazard_prefixes:
            print(f"No FEMA data prefixes are mapped to the lightning type: {self.type_of_hazard}.")
            return 0.0

        for hazard_prefix in hazard_prefixes:
            print(f"Starting cumulative frequency calculation for lightning with hazard prefix: {hazard_prefix}")
            if hazard_prefix not in self.NRI_data_fields:
                print(f"No data available for the hazard prefix: {hazard_prefix}")
                continue

            for county, data in self.NRI_data_fields[hazard_prefix].items():
                if "AFREQ" in data:
                    frequency = data["AFREQ"]
                    total_frequency += frequency  # Sum frequencies directly
                    print(f"County: {county}, Frequency: {frequency}")

        self.historical_frequency = total_frequency
        print(f"\nCumulative annualized frequency for lightning: {total_frequency}")
        return total_frequency