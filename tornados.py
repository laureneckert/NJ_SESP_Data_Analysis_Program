#NJSESP Project
#Lauren Eckert
#Version 2

#tornado class
from natural_hazard import NaturalHazard
import utilities as uti
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

class Tornados(NaturalHazard):
    def __init__(self, type_of_hazard='tornados'):
        super().__init__(type_of_hazard)
    
    def get_years_and_intensities(self):
        #tornados intensities denoted by NOAA field 'TOR_F_SCALE'

        return super().get_years_and_intensities()