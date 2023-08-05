# -*- coding: utf-8 -*-
"""
Created on April 13,  2022

@author: wang Haihua
"""

from importlib_metadata import entry_points
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({'font.family': 'SimHei', 'mathtext.fontset': 'stix'})

###########################################################################################
###############################   1 Differential Equations  ###############################
###########################################################################################

####***************************     1.1 Population          ****************************###


def pop_estimate_coef(population,year,function_type='exponential'):
    """Calculate the coeficient(s) of a given type of growth model

    Parameters
    ----------
    population : a array or list type of data
    year            : year list.The default year list is range(len(population_list))
    function_type   : the type of grown mode
        - 'exponential' : the exponential growth mode and its function is $x(t) = x_0 * e^{rt}$
        - 'logistic'    : the logistic growth mode and its funciton si $x(t) = \frac{x_m}{1+(\frac{x_m}{x_0})*e^{-rt}}$
        
    Yields
    ------
    coefs : the dict of coeficients in the given function
        - 'r'  : the nature growth rate
        - 'x_0'  : the initial population
        = 'x_m': the environmental carrying capacity

    """

    # convert population_list and year list to array type    
    population = np.array(population).flatten()
    year = np.array(year)    
    
    def logis_func(t,r,x0,xm):
        a1 = xm/x0 - 1
        a2 = np.e**(-r*(t-year[0]))
        return xm/(1+a1*a2)
    
    def exp_func(t,r,x0):
        return x0*np.e**(r*(t-year[0]))
    
    coefs = {'r':np.nan,'x_0':np.nan,'x_m':np.nan,'model_expression':np.nan}
    
    if function_type.lower() == 'exponential':
        pFit,pCov = curve_fit(exp_func,year,population)
        r = pFit[0]
        x0 = pFit[1]
        coefs['r'] = r
        coefs['x_0'] = x0
        coefs['model_expression'] = f'{x0}*e^{r}x'
        print('The nature growth rate is ',r)
        print('The initial population is ',x0)
        return coefs
    else: 
        pFit,pCov = curve_fit(logis_func,year,population,p0=np.ones(3))
        r = pFit[0]
        x0 = pFit[1]
        xm = pFit[2]
        coefs['r'] = r
        coefs['x_0'] = x0
        coefs['x_m'] = xm
        coefs['model_expression'] = f'{xm}/(1+{xm/x0}*e^{r}x'
        print('The nature growth rate is ',r)
        print('The initial population is ',x0)
        print('The environmental carrying capacity is ',xm)
        return coefs