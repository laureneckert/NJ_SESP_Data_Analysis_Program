#NJSESP Project
#Lauren Eckert
#Version 2

#FEMA NRI Data class
from DataSource import DataSource
import pandas as pd

class FEMA_NRI_data(DataSource):
    def __init__(self, data):
        super().__init__()  # Initialize parent DataSource class
        attributes = [
            # Basic information
            "OID_", "NRI_ID", "STATE", "STATEABBRV", "STATEFIPS", "COUNTY", "COUNTYTYPE", "COUNTYFIPS", "STCOFIPS", 
            "POPULATION", "BUILDVALUE", "AGRIVALUE", "AREA", "RISK_VALUE", "RISK_SCORE", "RISK_RATNG", "RISK_SPCTL", 
            "EAL_SCORE", "EAL_RATNG", "EAL_SPCTL", "EAL_VALT", "EAL_VALB", "EAL_VALP", "EAL_VALPE", "EAL_VALA", 
            "ALR_VALB", "ALR_VALP", "ALR_VALA", "ALR_NPCTL", "ALR_VRA_NPCTL", "SOVI_SCORE", "SOVI_RATNG", "SOVI_SPCTL", 
            "RESL_SCORE", "RESL_RATNG", "RESL_SPCTL", "RESL_VALUE", "CRF_VALUE",

            # Avalanche (AVLN)
            "AVLN_EVNTS", "AVLN_AFREQ", "AVLN_EXP_AREA", "AVLN_EXPB", "AVLN_EXPP", "AVLN_EXPPE", "AVLN_EXPT", 
            "AVLN_HLRB", "AVLN_HLRP", "AVLN_HLRR", "AVLN_EALB", "AVLN_EALP", "AVLN_EALPE", "AVLN_EALT", "AVLN_EALS", 
            "AVLN_EALR", "AVLN_ALRB", "AVLN_ALRP", "AVLN_ALR_NPCTL", "AVLN_RISKV", "AVLN_RISKS", "AVLN_RISKR", 

            # Coastal Flooding (CFLD)
            "CFLD_EVNTS", "CFLD_AFREQ", "CFLD_EXP_AREA", "CFLD_EXPB", "CFLD_EXPP", "CFLD_EXPPE", "CFLD_EXPT", 
            "CFLD_HLRB", "CFLD_HLRP", "CFLD_HLRR", "CFLD_EALB", "CFLD_EALP", "CFLD_EALPE", "CFLD_EALT", "CFLD_EALS", 
            "CFLD_EALR", "CFLD_ALRB", "CFLD_ALRP", "CFLD_ALR_NPCTL", "CFLD_RISKV", "CFLD_RISKS", "CFLD_RISKR", 

            # Cold Wave (CWAV)
            "CWAV_EVNTS", "CWAV_AFREQ", "CWAV_EXP_AREA", "CWAV_EXPB", "CWAV_EXPP", "CWAV_EXPPE", "CWAV_EXPA", "CWAV_EXPT",
            "CWAV_HLRB", "CWAV_HLRP", "CWAV_HLRA", "CWAV_HLRR", "CWAV_EALB", "CWAV_EALP", "CWAV_EALPE", "CWAV_EALA",
            "CWAV_EALT", "CWAV_EALS", "CWAV_EALR", "CWAV_ALRB", "CWAV_ALRP", "CWAV_ALRA", "CWAV_ALR_NPCTL", "CWAV_RISKV",
            "CWAV_RISKS", "CWAV_RISKR", 

            # Drought (DRGT)
            "DRGT_EVNTS", "DRGT_AFREQ", "DRGT_EXP_AREA", "DRGT_EXPA", "DRGT_EXPT", "DRGT_HLRA", "DRGT_HLRR", "DRGT_EALA", 
            "DRGT_EALT", "DRGT_EALS", "DRGT_EALR", "DRGT_ALRA", "DRGT_ALR_NPCTL", "DRGT_RISKV", "DRGT_RISKS", "DRGT_RISKR", 
            
            # Earthquake (ERQK)
            "ERQK_EVNTS", "ERQK_AFREQ", "ERQK_EXP_AREA", "ERQK_EXPB", "ERQK_EXPP", "ERQK_EXPPE", 
            "ERQK_EXPT", "ERQK_HLRB", "ERQK_HLRP", "ERQK_HLRR", "ERQK_EALB", "ERQK_EALP", "ERQK_EALPE", "ERQK_EALT", 
            "ERQK_EALS", "ERQK_EALR", "ERQK_ALRB", "ERQK_ALRP", "ERQK_ALR_NPCTL", "ERQK_RISKV", "ERQK_RISKS", 
            "ERQK_RISKR", 
            
            # Hail (HAIL)
            "HAIL_EVNTS", "HAIL_AFREQ", "HAIL_EXP_AREA", "HAIL_EXPB", "HAIL_EXPP", "HAIL_EXPPE", 
            "HAIL_EXPA", "HAIL_EXPT", "HAIL_HLRB", "HAIL_HLRP", "HAIL_HLRA", "HAIL_HLRR", "HAIL_EALB", "HAIL_EALP", 
            "HAIL_EALPE", "HAIL_EALA", "HAIL_EALT", "HAIL_EALS", "HAIL_EALR", "HAIL_ALRB", "HAIL_ALRP", "HAIL_ALRA", 
            "HAIL_ALR_NPCTL", "HAIL_RISKV", "HAIL_RISKS", "HAIL_RISKR", 
            
            # Heat Wave (HWAV)
            "HWAV_EVNTS", "HWAV_AFREQ", "HWAV_EXP_AREA", 
            "HWAV_EXPB", "HWAV_EXPP", "HWAV_EXPPE", "HWAV_EXPA", "HWAV_EXPT", "HWAV_HLRB", "HWAV_HLRP", "HWAV_HLRA", 
            "HWAV_HLRR", "HWAV_EALB", "HWAV_EALP", "HWAV_EALPE", "HWAV_EALA", "HWAV_EALT", "HWAV_EALS", "HWAV_EALR", 
            "HWAV_ALRB", "HWAV_ALRP", "HWAV_ALRA", "HWAV_ALR_NPCTL", "HWAV_RISKV", "HWAV_RISKS", "HWAV_RISKR", 
            
            # Hurricane (HRCN)
            "HRCN_EVNTS", "HRCN_AFREQ", "HRCN_EXP_AREA", "HRCN_EXPB", "HRCN_EXPP", "HRCN_EXPPE", "HRCN_EXPA", 
            "HRCN_EXPT", "HRCN_HLRB", "HRCN_HLRP", "HRCN_HLRA", "HRCN_HLRR", "HRCN_EALB", "HRCN_EALP", "HRCN_EALPE", 
            "HRCN_EALA", "HRCN_EALT", "HRCN_EALS", "HRCN_EALR", "HRCN_ALRB", "HRCN_ALRP", "HRCN_ALRA", "HRCN_ALR_NPCTL", 
            "HRCN_RISKV", "HRCN_RISKS", "HRCN_RISKR", 

            # Ice Storm (ISTM)
            "ISTM_EVNTS", "ISTM_AFREQ", "ISTM_EXP_AREA", "ISTM_EXPB", 
            "ISTM_EXPP", "ISTM_EXPPE", "ISTM_EXPT", "ISTM_HLRB", "ISTM_HLRP", "ISTM_HLRR", "ISTM_EALB", "ISTM_EALP", 
            "ISTM_EALPE", "ISTM_EALT", "ISTM_EALS", "ISTM_EALR", "ISTM_ALRB", "ISTM_ALRP", "ISTM_ALR_NPCTL", 
            "ISTM_RISKV", "ISTM_RISKS", "ISTM_RISKR", 
            
            # Landslide (LNDS)
            "LNDS_EVNTS", "LNDS_AFREQ", "LNDS_EXP_AREA", "LNDS_EXPB", 
            "LNDS_EXPP", "LNDS_EXPPE", "LNDS_EXPT", "LNDS_HLRB", "LNDS_HLRP", "LNDS_HLRR", "LNDS_EALB", "LNDS_EALP", 
            "LNDS_EALPE", "LNDS_EALT", "LNDS_EALS", "LNDS_EALR", "LNDS_ALRB", "LNDS_ALRP", "LNDS_ALR_NPCTL", 
            "LNDS_RISKV", "LNDS_RISKS", "LNDS_RISKR", 
            
            # Lightning (LTNG)
            "LTNG_EVNTS", "LTNG_AFREQ", "LTNG_EXP_AREA", "LTNG_EXPB", 
            "LTNG_EXPP", "LTNG_EXPPE", "LTNG_EXPT", "LTNG_HLRB", "LTNG_HLRP", "LTNG_HLRR", "LTNG_EALB", "LTNG_EALP", 
            "LTNG_EALPE", "LTNG_EALT", "LTNG_EALS", "LTNG_EALR", "LTNG_ALRB", "LTNG_ALRP", "LTNG_ALR_NPCTL", "LTNG_RISKV", 
            "LTNG_RISKS", "LTNG_RISKR", 
            
            # Riverine Flooding (RFLD)
            "RFLD_EVNTS", "RFLD_AFREQ", "RFLD_EXP_AREA", "RFLD_EXPB", "RFLD_EXPP", "RFLD_EXPPE", "RFLD_EXPA", 
            "RFLD_EXPT", "RFLD_HLRB", "RFLD_HLRP", "RFLD_HLRA", "RFLD_HLRR", "RFLD_EALB", "RFLD_EALP", "RFLD_EALPE", 
            "RFLD_EALA", "RFLD_EALT", "RFLD_EALS", "RFLD_EALR", "RFLD_ALRB", "RFLD_ALRP", "RFLD_ALRA", "RFLD_ALR_NPCTL", 
            "RFLD_RISKV", "RFLD_RISKS", "RFLD_RISKR", 
           
            # Strong Wind (SWND)
            "SWND_EVNTS", "SWND_AFREQ", "SWND_EXP_AREA", "SWND_EXPB", 
            "SWND_EXPP", "SWND_EXPPE", "SWND_EXPA", "SWND_EXPT", "SWND_HLRB", "SWND_HLRP", "SWND_HLRA", "SWND_HLRR", 
            "SWND_EALB", "SWND_EALP", "SWND_EALPE", "SWND_EALA", "SWND_EALT", "SWND_EALS", "SWND_EALR", "SWND_ALRB", 
            "SWND_ALRP", "SWND_ALRA", "SWND_ALR_NPCTL", "SWND_RISKV", "SWND_RISKS", "SWND_RISKR", 
            
            # Tornado (TRND)
            "TRND_EVNTS", 
            "TRND_AFREQ", "TRND_EXP_AREA", "TRND_EXPB", "TRND_EXPP", "TRND_EXPPE", "TRND_EXPA", "TRND_EXPT", 
            "TRND_HLRB", "TRND_HLRP", "TRND_HLRA", "TRND_HLRR", "TRND_EALB", "TRND_EALP", "TRND_EALPE", "TRND_EALA", 
            "TRND_EALT", "TRND_EALS", "TRND_EALR", "TRND_ALRB", "TRND_ALRP", "TRND_ALRA", "TRND_ALR_NPCTL", "TRND_RISKV", 
            "TRND_RISKS", "TRND_RISKR", 
            
            # Tsunami (TSUN)
            "TSUN_EVNTS", "TSUN_AFREQ", "TSUN_EXP_AREA", "TSUN_EXPB", "TSUN_EXPP", 
            "TSUN_EXPPE", "TSUN_EXPT", "TSUN_HLRB", "TSUN_HLRP", "TSUN_HLRR", "TSUN_EALB", "TSUN_EALP", "TSUN_EALPE", 
            "TSUN_EALT", "TSUN_EALS", "TSUN_EALR", "TSUN_ALRB", "TSUN_ALRP", "TSUN_ALR_NPCTL", "TSUN_RISKV", 
            "TSUN_RISKS", "TSUN_RISKR", 
           
            # Volcanic Activity (VLCN)
            "VLCN_EVNTS", "VLCN_AFREQ", "VLCN_EXP_AREA", "VLCN_EXPB", "VLCN_EXPP", 
            "VLCN_EXPPE", "VLCN_EXPT", "VLCN_HLRB", "VLCN_HLRP", "VLCN_HLRR", "VLCN_EALB", "VLCN_EALP", "VLCN_EALPE", 
            "VLCN_EALT", "VLCN_EALS", "VLCN_EALR", "VLCN_ALRB", "VLCN_ALRP", "VLCN_ALR_NPCTL", "VLCN_RISKV", 
            "VLCN_RISKS", "VLCN_RISKR", 
           
            # Wildfire (WFIR)
            "WFIR_EVNTS", "WFIR_AFREQ", "WFIR_EXP_AREA", "WFIR_EXPB", "WFIR_EXPP", 
            "WFIR_EXPPE", "WFIR_EXPA", "WFIR_EXPT", "WFIR_HLRB", "WFIR_HLRP", "WFIR_HLRA", "WFIR_HLRR", "WFIR_EALB", 
            "WFIR_EALP", "WFIR_EALPE", "WFIR_EALA", "WFIR_EALT", "WFIR_EALS", "WFIR_EALR", "WFIR_ALRB", "WFIR_ALRP", 
            "WFIR_ALRA", "WFIR_ALR_NPCTL", "WFIR_RISKV", "WFIR_RISKS", "WFIR_RISKR", 
            
            # Winter Weather (WNTW)
            "WNTW_EVNTS", "WNTW_AFREQ", "WNTW_EXP_AREA", "WNTW_EXPB", "WNTW_EXPP", "WNTW_EXPPE", "WNTW_EXPA", 
            "WNTW_EXPT", "WNTW_HLRB", "WNTW_HLRP", "WNTW_HLRA", "WNTW_HLRR", "WNTW_EALB", "WNTW_EALP", "WNTW_EALPE", 
            "WNTW_EALA", "WNTW_EALT", "WNTW_EALS", "WNTW_EALR", "WNTW_ALRB", "WNTW_ALRP", "WNTW_ALRA", "WNTW_ALR_NPCTL", 
            "WNTW_RISKV", "WNTW_RISKS", "WNTW_RISKR",

            # Version of NRI Data
            "NRI_VER"
        ]

        for attr in attributes:
            setattr(self, attr, data.get(attr))

    def get_attributes():
        # List of attributes as defined earlier
        return [
        # Basic information
        "OID_", "NRI_ID", "STATE", "STATEABBRV", "STATEFIPS", "COUNTY", "COUNTYTYPE", "COUNTYFIPS", "STCOFIPS", 
        "POPULATION", "BUILDVALUE", "AGRIVALUE", "AREA", "RISK_VALUE", "RISK_SCORE", "RISK_RATNG", "RISK_SPCTL", 
        "EAL_SCORE", "EAL_RATNG", "EAL_SPCTL", "EAL_VALT", "EAL_VALB", "EAL_VALP", "EAL_VALPE", "EAL_VALA", 
        "ALR_VALB", "ALR_VALP", "ALR_VALA", "ALR_NPCTL", "ALR_VRA_NPCTL", "SOVI_SCORE", "SOVI_RATNG", "SOVI_SPCTL", 
        "RESL_SCORE", "RESL_RATNG", "RESL_SPCTL", "RESL_VALUE", "CRF_VALUE",

        # Avalanche (AVLN)
        "AVLN_EVNTS", "AVLN_AFREQ", "AVLN_EXP_AREA", "AVLN_EXPB", "AVLN_EXPP", "AVLN_EXPPE", "AVLN_EXPT", 
        "AVLN_HLRB", "AVLN_HLRP", "AVLN_HLRR", "AVLN_EALB", "AVLN_EALP", "AVLN_EALPE", "AVLN_EALT", "AVLN_EALS", 
        "AVLN_EALR", "AVLN_ALRB", "AVLN_ALRP", "AVLN_ALR_NPCTL", "AVLN_RISKV", "AVLN_RISKS", "AVLN_RISKR", 

        # Coastal Flooding (CFLD)
        "CFLD_EVNTS", "CFLD_AFREQ", "CFLD_EXP_AREA", "CFLD_EXPB", "CFLD_EXPP", "CFLD_EXPPE", "CFLD_EXPT", 
        "CFLD_HLRB", "CFLD_HLRP", "CFLD_HLRR", "CFLD_EALB", "CFLD_EALP", "CFLD_EALPE", "CFLD_EALT", "CFLD_EALS", 
        "CFLD_EALR", "CFLD_ALRB", "CFLD_ALRP", "CFLD_ALR_NPCTL", "CFLD_RISKV", "CFLD_RISKS", "CFLD_RISKR", 

        # Cold Wave (CWAV)
        "CWAV_EVNTS", "CWAV_AFREQ", "CWAV_EXP_AREA", "CWAV_EXPB", "CWAV_EXPP", "CWAV_EXPPE", "CWAV_EXPA", "CWAV_EXPT",
        "CWAV_HLRB", "CWAV_HLRP", "CWAV_HLRA", "CWAV_HLRR", "CWAV_EALB", "CWAV_EALP", "CWAV_EALPE", "CWAV_EALA",
        "CWAV_EALT", "CWAV_EALS", "CWAV_EALR", "CWAV_ALRB", "CWAV_ALRP", "CWAV_ALRA", "CWAV_ALR_NPCTL", "CWAV_RISKV",
        "CWAV_RISKS", "CWAV_RISKR", 

        # Drought (DRGT)
        "DRGT_EVNTS", "DRGT_AFREQ", "DRGT_EXP_AREA", "DRGT_EXPA", "DRGT_EXPT", "DRGT_HLRA", "DRGT_HLRR", "DRGT_EALA", 
        "DRGT_EALT", "DRGT_EALS", "DRGT_EALR", "DRGT_ALRA", "DRGT_ALR_NPCTL", "DRGT_RISKV", "DRGT_RISKS", "DRGT_RISKR", 
        
        # Earthquake (ERQK)
        "ERQK_EVNTS", "ERQK_AFREQ", "ERQK_EXP_AREA", "ERQK_EXPB", "ERQK_EXPP", "ERQK_EXPPE", 
        "ERQK_EXPT", "ERQK_HLRB", "ERQK_HLRP", "ERQK_HLRR", "ERQK_EALB", "ERQK_EALP", "ERQK_EALPE", "ERQK_EALT", 
        "ERQK_EALS", "ERQK_EALR", "ERQK_ALRB", "ERQK_ALRP", "ERQK_ALR_NPCTL", "ERQK_RISKV", "ERQK_RISKS", 
        "ERQK_RISKR", 
        
        # Hail (HAIL)
        "HAIL_EVNTS", "HAIL_AFREQ", "HAIL_EXP_AREA", "HAIL_EXPB", "HAIL_EXPP", "HAIL_EXPPE", 
        "HAIL_EXPA", "HAIL_EXPT", "HAIL_HLRB", "HAIL_HLRP", "HAIL_HLRA", "HAIL_HLRR", "HAIL_EALB", "HAIL_EALP", 
        "HAIL_EALPE", "HAIL_EALA", "HAIL_EALT", "HAIL_EALS", "HAIL_EALR", "HAIL_ALRB", "HAIL_ALRP", "HAIL_ALRA", 
        "HAIL_ALR_NPCTL", "HAIL_RISKV", "HAIL_RISKS", "HAIL_RISKR", 
        
        # Heat Wave (HWAV)
        "HWAV_EVNTS", "HWAV_AFREQ", "HWAV_EXP_AREA", 
        "HWAV_EXPB", "HWAV_EXPP", "HWAV_EXPPE", "HWAV_EXPA", "HWAV_EXPT", "HWAV_HLRB", "HWAV_HLRP", "HWAV_HLRA", 
        "HWAV_HLRR", "HWAV_EALB", "HWAV_EALP", "HWAV_EALPE", "HWAV_EALA", "HWAV_EALT", "HWAV_EALS", "HWAV_EALR", 
        "HWAV_ALRB", "HWAV_ALRP", "HWAV_ALRA", "HWAV_ALR_NPCTL", "HWAV_RISKV", "HWAV_RISKS", "HWAV_RISKR", 
        
        # Hurricane (HRCN)
        "HRCN_EVNTS", "HRCN_AFREQ", "HRCN_EXP_AREA", "HRCN_EXPB", "HRCN_EXPP", "HRCN_EXPPE", "HRCN_EXPA", 
        "HRCN_EXPT", "HRCN_HLRB", "HRCN_HLRP", "HRCN_HLRA", "HRCN_HLRR", "HRCN_EALB", "HRCN_EALP", "HRCN_EALPE", 
        "HRCN_EALA", "HRCN_EALT", "HRCN_EALS", "HRCN_EALR", "HRCN_ALRB", "HRCN_ALRP", "HRCN_ALRA", "HRCN_ALR_NPCTL", 
        "HRCN_RISKV", "HRCN_RISKS", "HRCN_RISKR", 

        # Ice Storm (ISTM)
        "ISTM_EVNTS", "ISTM_AFREQ", "ISTM_EXP_AREA", "ISTM_EXPB", 
        "ISTM_EXPP", "ISTM_EXPPE", "ISTM_EXPT", "ISTM_HLRB", "ISTM_HLRP", "ISTM_HLRR", "ISTM_EALB", "ISTM_EALP", 
        "ISTM_EALPE", "ISTM_EALT", "ISTM_EALS", "ISTM_EALR", "ISTM_ALRB", "ISTM_ALRP", "ISTM_ALR_NPCTL", 
        "ISTM_RISKV", "ISTM_RISKS", "ISTM_RISKR", 
        
        # Landslide (LNDS)
        "LNDS_EVNTS", "LNDS_AFREQ", "LNDS_EXP_AREA", "LNDS_EXPB", 
        "LNDS_EXPP", "LNDS_EXPPE", "LNDS_EXPT", "LNDS_HLRB", "LNDS_HLRP", "LNDS_HLRR", "LNDS_EALB", "LNDS_EALP", 
        "LNDS_EALPE", "LNDS_EALT", "LNDS_EALS", "LNDS_EALR", "LNDS_ALRB", "LNDS_ALRP", "LNDS_ALR_NPCTL", 
        "LNDS_RISKV", "LNDS_RISKS", "LNDS_RISKR", 
        
        # Lightning (LTNG)
        "LTNG_EVNTS", "LTNG_AFREQ", "LTNG_EXP_AREA", "LTNG_EXPB", 
        "LTNG_EXPP", "LTNG_EXPPE", "LTNG_EXPT", "LTNG_HLRB", "LTNG_HLRP", "LTNG_HLRR", "LTNG_EALB", "LTNG_EALP", 
        "LTNG_EALPE", "LTNG_EALT", "LTNG_EALS", "LTNG_EALR", "LTNG_ALRB", "LTNG_ALRP", "LTNG_ALR_NPCTL", "LTNG_RISKV", 
        "LTNG_RISKS", "LTNG_RISKR", 
        
        # Riverine Flooding (RFLD)
        "RFLD_EVNTS", "RFLD_AFREQ", "RFLD_EXP_AREA", "RFLD_EXPB", "RFLD_EXPP", "RFLD_EXPPE", "RFLD_EXPA", 
        "RFLD_EXPT", "RFLD_HLRB", "RFLD_HLRP", "RFLD_HLRA", "RFLD_HLRR", "RFLD_EALB", "RFLD_EALP", "RFLD_EALPE", 
        "RFLD_EALA", "RFLD_EALT", "RFLD_EALS", "RFLD_EALR", "RFLD_ALRB", "RFLD_ALRP", "RFLD_ALRA", "RFLD_ALR_NPCTL", 
        "RFLD_RISKV", "RFLD_RISKS", "RFLD_RISKR", 
        
        # Strong Wind (SWND)
        "SWND_EVNTS", "SWND_AFREQ", "SWND_EXP_AREA", "SWND_EXPB", 
        "SWND_EXPP", "SWND_EXPPE", "SWND_EXPA", "SWND_EXPT", "SWND_HLRB", "SWND_HLRP", "SWND_HLRA", "SWND_HLRR", 
        "SWND_EALB", "SWND_EALP", "SWND_EALPE", "SWND_EALA", "SWND_EALT", "SWND_EALS", "SWND_EALR", "SWND_ALRB", 
        "SWND_ALRP", "SWND_ALRA", "SWND_ALR_NPCTL", "SWND_RISKV", "SWND_RISKS", "SWND_RISKR", 
        
        # Tornado (TRND)
        "TRND_EVNTS", 
        "TRND_AFREQ", "TRND_EXP_AREA", "TRND_EXPB", "TRND_EXPP", "TRND_EXPPE", "TRND_EXPA", "TRND_EXPT", 
        "TRND_HLRB", "TRND_HLRP", "TRND_HLRA", "TRND_HLRR", "TRND_EALB", "TRND_EALP", "TRND_EALPE", "TRND_EALA", 
        "TRND_EALT", "TRND_EALS", "TRND_EALR", "TRND_ALRB", "TRND_ALRP", "TRND_ALRA", "TRND_ALR_NPCTL", "TRND_RISKV", 
        "TRND_RISKS", "TRND_RISKR", 
        
        # Tsunami (TSUN)
        "TSUN_EVNTS", "TSUN_AFREQ", "TSUN_EXP_AREA", "TSUN_EXPB", "TSUN_EXPP", 
        "TSUN_EXPPE", "TSUN_EXPT", "TSUN_HLRB", "TSUN_HLRP", "TSUN_HLRR", "TSUN_EALB", "TSUN_EALP", "TSUN_EALPE", 
        "TSUN_EALT", "TSUN_EALS", "TSUN_EALR", "TSUN_ALRB", "TSUN_ALRP", "TSUN_ALR_NPCTL", "TSUN_RISKV", 
        "TSUN_RISKS", "TSUN_RISKR", 
        
        # Volcanic Activity (VLCN)
        "VLCN_EVNTS", "VLCN_AFREQ", "VLCN_EXP_AREA", "VLCN_EXPB", "VLCN_EXPP", 
        "VLCN_EXPPE", "VLCN_EXPT", "VLCN_HLRB", "VLCN_HLRP", "VLCN_HLRR", "VLCN_EALB", "VLCN_EALP", "VLCN_EALPE", 
        "VLCN_EALT", "VLCN_EALS", "VLCN_EALR", "VLCN_ALRB", "VLCN_ALRP", "VLCN_ALR_NPCTL", "VLCN_RISKV", 
        "VLCN_RISKS", "VLCN_RISKR", 
        
        # Wildfire (WFIR)
        "WFIR_EVNTS", "WFIR_AFREQ", "WFIR_EXP_AREA", "WFIR_EXPB", "WFIR_EXPP", 
        "WFIR_EXPPE", "WFIR_EXPA", "WFIR_EXPT", "WFIR_HLRB", "WFIR_HLRP", "WFIR_HLRA", "WFIR_HLRR", "WFIR_EALB", 
        "WFIR_EALP", "WFIR_EALPE", "WFIR_EALA", "WFIR_EALT", "WFIR_EALS", "WFIR_EALR", "WFIR_ALRB", "WFIR_ALRP", 
        "WFIR_ALRA", "WFIR_ALR_NPCTL", "WFIR_RISKV", "WFIR_RISKS", "WFIR_RISKR", 
        
        # Winter Weather (WNTW)
        "WNTW_EVNTS", "WNTW_AFREQ", "WNTW_EXP_AREA", "WNTW_EXPB", "WNTW_EXPP", "WNTW_EXPPE", "WNTW_EXPA", 
        "WNTW_EXPT", "WNTW_HLRB", "WNTW_HLRP", "WNTW_HLRA", "WNTW_HLRR", "WNTW_EALB", "WNTW_EALP", "WNTW_EALPE", 
        "WNTW_EALA", "WNTW_EALT", "WNTW_EALS", "WNTW_EALR", "WNTW_ALRB", "WNTW_ALRP", "WNTW_ALRA", "WNTW_ALR_NPCTL", 
        "WNTW_RISKV", "WNTW_RISKS", "WNTW_RISKR",

        # Version of NRI Data
        "NRI_VER"
        ]

    def extract_data(file_path):
        """
        Reads FEMA NRI data from a CSV file and creates FEMA_NRI_Data objects.

        Parameters:
        file_path (str): Path to the CSV file containing FEMA NRI data.

        Returns:
        list: A list of FEMA_NRI_Data objects created from the file data.
        """
        fema_nri_entries = []
        try:
            df = pd.read_csv(file_path)
            print(f"Successfully read FEMA NRI file: {file_path}")

            for index, row in df.iterrows():
                data = {attr: row.get(attr, None) for attr in FEMA_NRI_data.get_attributes()}
                fema_entry = FEMA_NRI_data(data)
                fema_nri_entries.append(fema_entry)

        except Exception as e:
            print(f"Error reading FEMA NRI file {file_path}: {e}")
            return []

        print(f"Extracted {len(fema_nri_entries)} FEMA NRI entries from {file_path}")
        return fema_nri_entries

    @staticmethod
    def print_samples(fema_nri_data_list, sample_size=5):
        """
        Prints a sample of FEMA NRI data entries, specifically for hurricane-related attributes.

        Parameters:
        fema_nri_data_list (list): List of FEMA_NRI_data instances.
        sample_size (int): Number of samples to print.
        """
        print("\nSample FEMA NRI Data:")
        for i, fema_data in enumerate(fema_nri_data_list[:sample_size]):
            print(f"\nSample {i+1}:")
            print(f"County: {fema_data.COUNTY}, State: {fema_data.STATEABBRV}")
            print(f"Population: {fema_data.POPULATION}, Building Value: {fema_data.BUILDVALUE}")
            # Printing hurricane-specific attributes
            print(f"Hurricane Events: {fema_data.HRCN_EVNTS}")
            print(f"Hurricane Annualized Frequency: {fema_data.HRCN_AFREQ}")
            print(f"Hurricane Exposure Area: {fema_data.HRCN_EXP_AREA}")
            print(f"Hurricane Exposure - Building Value: {fema_data.HRCN_EXPB}")
            print(f"Hurricane Exposure - Population: {fema_data.HRCN_EXPP}")
            print(f"Hurricane Exposure - Population Equivalence: {fema_data.HRCN_EXPPE}")
            print(f"Hurricane Exposure - Agriculture Value: {fema_data.HRCN_EXPA}")
            print(f"Hurricane Exposure - Total: {fema_data.HRCN_EXPT}")
            print(f"Hurricane Historic Loss Ratio - Buildings: {fema_data.HRCN_HLRB}")
            print(f"Hurricane Historic Loss Ratio - Population: {fema_data.HRCN_HLRP}")
            print(f"Hurricane Historic Loss Ratio - Agriculture: {fema_data.HRCN_HLRA}")
            print(f"Hurricane Historic Loss Ratio - Total Rating: {fema_data.HRCN_HLRR}")
            print(f"Hurricane EAL - Buildings: {fema_data.HRCN_EALB}")
            print(f"Hurricane EAL - Population: {fema_data.HRCN_EALP}")
            print(f"Hurricane EAL - Population Equivalence: {fema_data.HRCN_EALPE}")
            print(f"Hurricane EAL - Agriculture: {fema_data.HRCN_EALA}")
            print(f"Hurricane EAL - Total: {fema_data.HRCN_EALT}")
            print(f"Hurricane EAL - Society: {fema_data.HRCN_EALS}")
            print(f"Hurricane EAL - Risk: {fema_data.HRCN_EALR}")
            print(f"Hurricane ALR - Buildings: {fema_data.HRCN_ALRB}")
            print(f"Hurricane ALR - Population: {fema_data.HRCN_ALRP}")
            print(f"Hurricane ALR - Agriculture: {fema_data.HRCN_ALRA}")
            print(f"Hurricane ALR - NPCTL: {fema_data.HRCN_ALR_NPCTL}")
            print(f"Hurricane Risk Value: {fema_data.HRCN_RISKV}")
            print(f"Hurricane Risk Score: {fema_data.HRCN_RISKS}")
            print(f"Hurricane Risk Rank: {fema_data.HRCN_RISKR}")

        if len(fema_nri_data_list) > sample_size:
            print(f"\n... and {len(fema_nri_data_list) - sample_size} more entries.")

    @staticmethod
    def assign_data_to_hazard(hazards, fema_nri_entries, fema_to_hazard_mapping):
        """
        Assigns FEMA data to each hazard based on their type and FEMA data prefixes, while maintaining county information.

        Parameters:
        hazards (list): List of hazard objects.
        fema_nri_entries (list): List of FEMA_NRI_data instances.
        fema_to_hazard_mapping (dict): Mapping of FEMA data field prefixes to hazard types.
        """
        print("Starting assignment of FEMA NRI data to hazards...")
        for hazard in hazards:
            hazard_type = hazard.type_of_hazard
            print(f"\nAssigning FEMA data to {hazard_type} hazard...")

            if hazard_type in fema_to_hazard_mapping:
                prefixes = fema_to_hazard_mapping[hazard_type]

                for prefix in prefixes:
                    print(f"\nProcessing FEMA data for {hazard_type} with prefix {prefix}...")

                    # Initialize a nested dictionary to store FEMA data by county for this prefix
                    hazard.NRI_data_fields[prefix] = {}

                    for fema_entry in fema_nri_entries:
                        county_name = fema_entry.COUNTY
                        if county_name not in hazard.NRI_data_fields[prefix]:
                            hazard.NRI_data_fields[prefix][county_name] = {}

                        for attr in FEMA_NRI_data.get_attributes():
                            if attr.startswith(prefix):
                                # Extract the county-specific part of the attribute
                                county_specific_attr = attr.replace(prefix + "_", "")
                                value = getattr(fema_entry, attr, None)
                                hazard.NRI_data_fields[prefix][county_name][county_specific_attr] = value

                        print(f"Assigned FEMA data for {county_name} with prefix {prefix} to {hazard_type} hazard.")

            else:
                print(f"No FEMA data mapping found for {hazard_type} hazard. Skipping...")

        print("Completed assignment of FEMA NRI data to hazards.")

    # Mapping of hazard types to their FEMA NRI data prefixes
    hazard_to_fema_prefix = {
        'hurricanes': ['HRCN'],               # Hurricane
        'earthquake': ['ERQK'],              # Earthquake
        'flooding': ['RFLD', 'CFLD'],        # Flooding (Riverine Flooding, Coastal Flooding)
        'avalanche': ['AVLN'],               # Avalanche
        'drought': ['DRGT'],                 # Drought
        'hail': ['HAIL'],                    # Hail
        'heat_wave': ['HWAV'],               # Heat Wave
        'landslide': ['LNDS'],               # Landslide
        'lightning': ['LTNG'],               # Lightning
        'strong_wind': ['SWND'],             # Strong Wind
        'tornado': ['TRND'],                 # Tornado
        'tsunami': ['TSUN'],                 # Tsunami
        'volcanic_activity': ['VLCN'],       # Volcanic Activity
        'wildfire': ['WFIR'],                # Wildfire
        'winter_storms': ['CWAV', 'ISTM', 'WNTW'],  # Winter Storms (Cold Wave, Ice Storm, Winter Weather) #three prefixes might cause a bug - need to verify when doing winter storms
    }

    def print_data_source_samples(self, sample_size=5):
        """
        Prints samples from each data source associated with the hazard.

        Parameters:
        sample_size (int): The number of samples to print from each data source.
        """
        print(f"\n{self.type_of_hazard.upper()} Hazard Data Samples:")

        # Print NOAA Event Samples
        print("\nNOAA Event Samples:")
        for i, event in enumerate(self.noaa_events[:sample_size]):
            print(f"Sample {i+1}: {event}")

        # Print Eagle I Event Samples
        print("\nEagle I Event Samples:")
        for i, event in enumerate(self.eaglei_events[:sample_size]):
            print(f"Sample {i+1}: {event}")

        # Print FEMA NRI Data Samples
        print("\nFEMA NRI Data Samples:")
        for i, (prefix, data_fields) in enumerate(self.NRI_data_fields.items()):
            if i >= sample_size:
                break
            print(f"\nSample {i+1} for {prefix}:")
            for key, value in data_fields.items():
                print(f"{key}: {value}")

        print("\nEnd of Data Samples")

