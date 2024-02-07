#NJSESP Project
#Lauren Eckert
#Version 2

#Winter storms class
from natural_hazard import NaturalHazard
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class WinterStorms(NaturalHazard):
    def __init__(self, type_of_hazard='winter storms'):
        super().__init__(type_of_hazard)