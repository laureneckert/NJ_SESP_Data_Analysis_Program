#NJSESP Project
#Lauren Eckert
#Version 2

#wildfire class
from natural_hazard import NaturalHazard
import utilities as uti
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

class Wildfires(NaturalHazard):
    def __init__(self, type_of_hazard='wildfires'):
        super().__init__(type_of_hazard)