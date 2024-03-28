#NJSESP Project
#Lauren Eckert
#Version 2

#hazards class

from abc import ABC, abstractmethod
import utilities as uti

class Hazard(ABC):
    def __init__(self, type_of_hazard):
        self.type_of_hazard = type_of_hazard

        # Financial attributes
        self.total_property_damage = 0.0
        self.property_damage_by_county = {}  # Key: County, Value: Damage Amount

        # Customer impact attributes
        self.percent_customers_affected = 0.0
        self.customers_affected_sum = 0 #average peak outages

        # Time duration attributes
        self.total_time_duration_customer_affected = 0.0 #for all threat incidents
        self.avg_time_duration_customer_affected = 0.0 #averaged to per threat incident

        #Historical
        self.historical_frequency = 0.0
        #self.historical_frequency_type = '' #not implemented

        # Coefficients for risk assessment
        self.future_impact_coefficient = 0.0
        self.frequency_coefficient = 0.0
        self.intensity_coefficient = 0.0

        # Risk score
        self.risk_score = 0.0

    @abstractmethod
    def calculate_risk(self):
        # Placeholder for risk calculation method
        pass
    
    @abstractmethod
    def calculate_scores(self):
        # Placeholder for method that calculates various scores
        pass
 
    @abstractmethod
    def print_basic_info(self):
        pass