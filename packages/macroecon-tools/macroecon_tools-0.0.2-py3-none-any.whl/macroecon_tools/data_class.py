# Data class
#   Properties
#       data: a single variable in a time table
#       freq: the frequency of that variable
#   Functions
#       trans(form), e.g., 'logdiff', 'diff', 'log', '100log'
#           must also provide number of lags for 'logdiff', 'diff'
#       agg(regate), e.g., 'quarterly', 'monthly', 'yearly'
#           must also provide method (e.g., lastvalue, mean, sum)
#       filter, e.g., 'linear' or 'hamiliton'
#           must first provide D1 (start date) and D2 (end date)
#           and for 'hamilton' p (lag length) and h (lead length)

import pandas as pd
import numpy as np
from scipy.signal import detrend
from datetime import datetime
from dateutil.relativedelta import relativedelta
import quantecon as qe
# get constants
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from constants import Constants

class Data:
    """
    A class used to represent a Data object.

    Attributes
    ----------
    data : pd.DataFrame
        a single variable in a time table
    freq : str
        the frequency of that variable

    Methods
    -------
    trans(form, lags=None)
        Transforms the data using the specified form (e.g., 'logdiff', 'diff', 'log', '100log').
        Must provide number of lags for 'logdiff' and 'diff'.
    agg(timestep, method)
        Aggregates the data using the specified method (e.g., 'quarterly', 'monthly', 'yearly').
        Must provide method (e.g., lastvalue, mean, sum).
    filter(method, D1, D2, p=None, h=None)
        Filters the data using the specified method (e.g., 'linear' or 'hamilton').
        Must provide start date (D1) and end date (D2).
        For 'hamilton', must also provide lag length (p) and lead length (h).
    """

    def __init__(self, dataraw, *args):
        # Variable (optional)
        if len(dataraw["tab"].columns) == 1:
            variableName = dataraw["tab"].columns[0]
        else:
            if not args:
                raise ValueError("data class: must choose on variable")
            else:
                variableName = args[0]
        
         # Initiaize properties
        self.data = dataraw["tab"][variableName]
        self.freq = dataraw["freqs"][variableName]

    def __repr__(self):
        return f"Data:\n{self.data}\nFrequency: {self.freq}"
    
    def copy(self):
        varin = Data.__new__(Data)
        varin.data = self.data.copy()
        varin.freq = self.freq
        return varin

    # Transform data
    def trans(self, func, *args):
        varin = self.copy()
        # Transformation function
        if func == 'logdiff':
            nlag = args[0]
            annpp = Constants.ANNSCALE_MAP[self.freq.lower()] / nlag
            varin.data = annpp * np.log(varin.data / varin.data.shift(nlag))
        elif func == 'diff':
            nlag = args[0]
            varin.data = varin.data - varin.data.shift(nlag)
        elif func == 'log':
            varin.data = np.log(self.data)
        elif func == '100log':
            varin.data = 100 * np.log(varin.data)
        else:
            raise ValueError(f'Not a valid transformation for variable {self}')

        return varin
    
    def agg(self, timestep, method):
        varin = self.copy()
        # Aggregation function
        varin.data = varin.data.resample(Constants.freq_map[timestep]).agg(Constants.agg_map[method])
        varin.freq = timestep
        return varin

    def trunc(self, D1, D2):
        varin = self.copy()
        # Truncate data
        varin.data = varin.data[D1:D2]
        return varin 
    
    def filter(self, D1, D2, filter_type, *args, **kwargs):
        varin = self.copy()
        D1 = datetime.strptime(D1, '%d-%b-%Y')
        D2 = datetime.strptime(D2, '%d-%b-%Y')

        # Filter
        if filter_type == 'linear':
            # Time range
            varin = varin.trunc(D1, D2)
            varin.data = pd.Series(detrend(varin.data, axis=0, type='linear'))
        elif filter_type == 'hamilton':
            # get default lag and lead lengths
            if varin.freq == 'yearly':
                lagLength = 1
                leadLength = 2
            elif varin.freq == 'quarterly':
                lagLength = 4
                leadLength = 8
            elif varin.freq == 'monthly':
                lagLength = 12
                leadLength = 24
            else:
                raise ValueError(f'{self.freq} frequency not supported for Hamilton filter')
            
            # get parameters 
            if 'LagLength' in kwargs:
                lagLength = kwargs['LagLength']
            if 'LeadLength' in kwargs:
                leadLength = kwargs['LeadLength']
            # get the tstart 
            if varin.freq == 'yearly':
                tstart = D1 - relativedelta(years=(lagLength + leadLength - 1))
            elif varin.freq == 'quarterly':
                tstart = D1 - relativedelta(months=3*(lagLength + leadLength - 1))
            elif varin.freq == 'monthly':
                tstart = D1 - relativedelta(months=(lagLength + leadLength - 1))
            trham = varin.data[tstart:D2]
            # Get cyclical component 
            cycle, trend = qe._filter.hamilton_filter(pd.Series(trham), leadLength, lagLength)
            varin.data = pd.Series(cycle.flatten(), index=trham.index)
        else:
            raise ValueError(f'Not a valid filter for variable')
            
        return varin

    def tt(self):
        return self.data