#NJSESP Project
#Lauren Eckert
#Version 2

#Earthquakes class
from natural_hazard import NaturalHazard
from FEMA_NRI_data import FEMA_NRI_data
import utilities as uti
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

class Earthquakes(NaturalHazard):
    def __init__(self, type_of_hazard='earthquakes'):
        super().__init__(type_of_hazard)