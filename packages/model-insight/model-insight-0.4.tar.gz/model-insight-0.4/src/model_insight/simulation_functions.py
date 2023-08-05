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
plt.rcParams.update({'font.family': 'SimHei', 'mathtext.fontset': 'stix'})

###########################################################################################
###############################     1 Queuing Theory        ###############################
###########################################################################################

####***************************     1.1 Normalization       ****************************###

def queue_p0(c,lam,mu):
    """Calculate the probability when there is no people in queue

    Parameters
    ----------
    c: Number of service desks
    lam: Average rate of customer arrivals
    mu: Average rate of system services
        
    Yields
    ------
    p0: the probability when there is no people in queue

    """

    a1 = sum([1/math.factorial(k)*(lam/mu)**k for k in range(c)])
    a2 = (1/math.factorial(c))*(1/(1-lam/(c*mu))*(lam/mu)**c)
    p0 = 1/(a1+a2)
    return p0


def average_queue(c,lam,mu):

    """Calculate the average number of people in queue

    Parameters
    ----------
    c: Number of service desks
    lam: Average rate of customer arrivals
    mu: Average rate of system services
        
    Yields
    ------
    ave_queue: the average number of people in queue

    """
    p0 = queue_p0(c,lam,mu)
    rou = lam/(c*mu)
    b1 = (c*rou)**c*rou
    b2 = math.factorial(c)*(1-rou)**2
    ave_queue = b1/b2*p0
    
    return ave_queue
