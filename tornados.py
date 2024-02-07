#NJSESP Project
#Lauren Eckert
#Version 2

#Tornado class
from natural_hazard import NaturalHazard
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class Tornados(NaturalHazard):
    def __init__(self, type_of_hazard='tornados'):
        super().__init__(type_of_hazard)