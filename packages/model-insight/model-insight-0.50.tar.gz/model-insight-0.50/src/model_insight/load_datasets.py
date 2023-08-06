# -*- coding: utf-8 -*-
"""
Created on April 13,  2022

@author: wang Haihua
"""

from importlib_metadata import entry_points
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import datetime

from torch import swapdims 
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

###########################################################################################
###############################     1 MCDM         ###############################
###########################################################################################

####***************************     1.1 Supplier Selection       ****************************###

def load_supplier():
    """ Supplier data
    

    Yields:
    -------
    supplier : a pandas DataFrame object that contains 100 samples with the columns of 
        'Warranty Terms', 'Payment Terms', 'Technical Support',
       'Sustainability Efforts', 'Finp.nancial Stability', 'Unit Cost',
       'Lead Time (Days)' and 'On Time Delivery'

    Use :
        For evaluation model practice

    Reference:
        https://github.com/LinBaiTao/Supplier_Selection_Methods 

    """
    data = np.array([[ 2.42,  2.8 ,  8.25,  3.09,  8.21,  1.05,  8.  ,  0.75],
       [ 6.51,  1.88,  3.6 ,  6.45,  4.31,  1.21, 13.  ,  0.83],
       [ 8.51,  1.06,  2.97,  9.36,  5.06,  1.22, 12.  ,  0.91],
       [ 4.63,  4.6 ,  5.84,  7.34,  9.2 ,  1.01,  9.  ,  0.72],
       [ 4.62,  7.44,  1.5 ,  8.93,  4.01,  1.03,  7.  ,  0.97],
       [ 7.87,  6.58,  2.93,  6.88,  6.3 ,  1.18, 14.  ,  0.83],
       [ 8.87,  5.94,  3.32,  7.45,  3.  ,  1.13,  6.  ,  1.  ],
       [ 9.15,  4.35,  1.28,  9.2 ,  3.07,  1.04, 15.  ,  0.81],
       [ 8.16,  2.39,  1.74,  8.8 ,  9.41,  1.02,  8.  ,  0.95],
       [ 1.66,  7.7 ,  4.11,  5.76,  5.72,  1.1 , 11.  ,  0.98],
       [ 4.84,  1.58,  9.35,  6.22,  6.59,  1.15,  5.  ,  0.72],
       [ 9.9 ,  2.64,  6.02,  2.34,  8.75,  1.18,  3.  ,  0.71],
       [ 2.91,  1.63,  8.38,  9.87,  1.63,  1.15, 13.  ,  0.87],
       [ 9.05,  9.7 ,  7.03,  7.59,  2.77,  1.04,  8.  ,  0.9 ],
       [ 2.73,  4.66,  1.26,  5.32,  8.42,  1.27, 15.  ,  0.86],
       [ 2.87,  8.49,  8.87,  4.37,  4.04,  1.05, 15.  ,  0.99],
       [ 7.89,  8.75,  4.84,  3.36,  7.51,  1.27,  5.  ,  0.99],
       [ 5.49,  5.26,  9.72,  6.11,  8.87,  1.15, 13.  ,  0.93],
       [ 9.48,  8.47,  3.42,  7.91,  2.62,  1.25,  2.  ,  0.83],
       [ 3.85,  1.16,  9.08,  7.28,  1.05,  1.24, 10.  ,  0.71],
       [ 9.97,  3.4 ,  7.98,  6.43,  9.3 ,  1.07,  6.  ,  0.86],
       [ 7.71,  1.43,  7.12,  3.16,  2.33,  1.26, 11.  ,  0.97],
       [ 5.94,  2.92,  7.56,  4.93,  9.69,  1.28,  7.  ,  0.73],
       [ 3.17,  2.97,  6.01,  2.99,  8.24,  1.15,  3.  ,  0.79],
       [ 2.32,  8.54,  8.21,  5.44,  4.09,  1.02, 11.  ,  0.82],
       [ 8.84,  2.85,  9.89,  7.04,  3.89,  1.05, 14.  ,  0.89],
       [ 6.2 ,  9.97,  3.9 ,  9.54,  7.04,  1.07, 13.  ,  0.73],
       [ 4.37,  7.5 ,  2.15,  9.57,  5.18,  1.23, 13.  ,  0.9 ],
       [ 1.23,  6.58,  2.16,  2.53,  1.65,  1.07,  9.  ,  0.71],
       [ 7.31,  9.63,  6.1 ,  1.19,  3.31,  1.21,  8.  ,  0.83],
       [ 2.05,  3.17,  3.27,  6.93,  4.12,  1.16,  2.  ,  0.82],
       [ 6.32,  5.18,  5.99,  4.46,  4.61,  1.13,  6.  ,  0.95],
       [ 2.18,  2.7 ,  4.14,  4.91,  6.24,  1.02,  2.  ,  0.95],
       [ 3.52,  4.51,  5.25,  2.08,  9.53,  1.2 , 15.  ,  0.75],
       [ 9.09,  4.62,  6.14,  1.77,  1.7 ,  1.05, 13.  ,  0.78],
       [ 8.85,  7.46,  7.86,  7.3 ,  4.18,  1.06, 10.  ,  0.78],
       [ 4.33,  5.27,  7.56,  2.76,  5.09,  1.19,  5.  ,  0.92],
       [ 7.08,  9.1 ,  2.77,  7.08,  7.8 ,  1.27,  2.  ,  0.8 ],
       [ 5.16,  8.31,  1.24,  2.08,  7.01,  1.17, 12.  ,  0.99],
       [ 9.34,  3.97,  7.94,  1.09,  1.3 ,  1.14,  9.  ,  0.78],
       [ 5.67,  8.87,  6.1 ,  6.99,  5.51,  1.03, 10.  ,  0.83],
       [ 1.52,  5.67,  2.64,  6.55,  5.07,  1.01,  9.  ,  0.97],
       [ 9.77,  3.18,  8.64,  2.08,  2.26,  1.1 ,  7.  ,  0.75],
       [ 5.79,  2.63,  1.59,  4.97,  3.71,  1.06, 11.  ,  0.86],
       [ 8.93,  1.16,  5.54,  2.65,  5.89,  1.13,  4.  ,  0.85],
       [ 6.97,  7.13,  5.71,  7.73,  6.76,  1.22,  8.  ,  0.93],
       [ 1.89,  5.08,  1.25,  4.88,  3.43,  1.17,  7.  ,  0.82],
       [ 9.34,  5.29,  7.61,  8.26,  9.71,  1.21,  8.  ,  0.75],
       [ 1.74,  2.12,  6.17,  4.61,  6.9 ,  1.09,  2.  ,  0.94],
       [ 8.96,  2.02,  5.52,  5.1 ,  8.33,  1.04, 13.  ,  0.71],
       [ 8.45,  6.51,  7.1 ,  6.31,  8.14,  1.28, 14.  ,  0.87],
       [ 6.83,  9.46,  1.55,  2.19,  8.23,  1.3 ,  6.  ,  0.97],
       [ 2.43,  9.18,  2.6 ,  4.55,  8.02,  1.13,  2.  ,  0.84],
       [ 2.58,  8.2 ,  9.54,  3.71,  4.64,  1.08,  3.  ,  0.9 ],
       [ 3.92,  6.28,  8.99,  4.01,  4.59,  1.12,  6.  ,  0.96],
       [ 3.52,  2.53,  4.3 ,  8.52,  9.81,  1.19,  3.  ,  0.9 ],
       [ 6.28,  6.16,  9.7 ,  9.14,  7.34,  1.11, 13.  ,  0.75],
       [ 6.61,  2.74,  5.61,  8.7 ,  6.19,  1.21,  6.  ,  0.7 ],
       [ 7.72,  9.74,  9.4 ,  8.36,  2.39,  1.19,  3.  ,  0.78],
       [ 6.14,  8.44,  3.67,  2.22,  7.78,  1.3 , 13.  ,  0.8 ],
       [ 9.65,  8.21,  4.28,  6.35,  4.43,  1.21,  5.  ,  0.72],
       [ 2.44,  8.12,  1.69,  1.64,  2.92,  1.14,  4.  ,  0.84],
       [ 1.72,  1.12,  4.46,  5.47,  8.23,  1.29,  4.  ,  0.73],
       [ 9.36,  8.77,  5.19,  2.4 ,  6.  ,  1.21,  8.  ,  0.87],
       [ 1.41,  5.75,  8.66,  8.02,  3.3 ,  1.21,  5.  ,  0.95],
       [ 1.41,  9.27,  2.75,  1.37,  2.75,  1.07,  2.  ,  0.7 ],
       [ 1.4 ,  4.99,  7.81,  5.59,  2.06,  1.1 ,  7.  ,  0.97],
       [ 6.84,  6.79,  6.57,  6.  ,  8.2 ,  1.17,  4.  ,  0.9 ],
       [ 9.94,  9.48,  9.12,  2.16,  7.14,  1.15,  2.  ,  0.9 ],
       [ 8.39,  2.26,  9.22,  4.23,  1.39,  1.21,  3.  ,  0.78],
       [ 7.22,  6.58,  3.63,  3.98,  1.39,  1.21, 11.  ,  0.89],
       [ 3.05,  1.88,  8.85,  1.68,  9.1 ,  1.07,  6.  ,  1.  ],
       [ 5.15,  2.13,  9.86,  7.81,  7.89,  1.24,  2.  ,  0.79],
       [ 7.8 ,  3.83,  2.02,  2.97,  8.03,  1.22,  2.  ,  0.71],
       [ 6.2 ,  6.81,  9.82,  1.83,  3.64,  1.14,  6.  ,  0.92],
       [ 1.22,  6.97,  6.55,  7.39,  9.1 ,  1.28, 11.  ,  0.76],
       [ 3.58,  1.99,  8.13,  4.22,  1.04,  1.02,  8.  ,  0.84],
       [ 9.85,  2.84,  5.07,  8.7 ,  3.57,  1.06, 11.  ,  0.86],
       [ 8.05,  4.59,  6.97,  7.89,  6.96,  1.21,  2.  ,  0.81],
       [ 5.18,  2.12,  2.34,  9.27,  7.61,  1.16,  3.  ,  0.74],
       [ 4.74,  2.03,  1.07,  7.62,  3.75,  1.27,  4.  ,  0.88],
       [ 6.52,  7.53,  2.89,  2.67,  5.79,  1.02, 15.  ,  0.72],
       [ 4.48,  8.22,  5.41,  9.34,  6.71,  1.28,  8.  ,  0.71],
       [ 6.73,  4.39,  8.63,  1.11,  3.04,  1.21,  8.  ,  0.92],
       [ 7.14,  8.41,  1.07,  8.1 ,  9.32,  1.22,  3.  ,  0.8 ],
       [ 1.96,  4.49,  4.47,  3.69,  2.82,  1.1 , 15.  ,  0.7 ],
       [ 3.97,  4.45,  7.6 ,  5.41,  2.7 ,  1.28,  8.  ,  0.93],
       [ 2.69,  8.84,  9.69,  5.81,  6.2 ,  1.07,  6.  ,  0.83],
       [ 6.86,  3.49,  3.24,  5.41,  4.34,  1.06,  4.  ,  0.99],
       [ 3.39,  2.74,  8.46,  2.83,  3.08,  1.06, 13.  ,  0.8 ],
       [ 3.68,  9.76,  4.93,  7.37,  5.3 ,  1.26, 11.  ,  0.97],
       [ 6.72,  1.5 ,  5.09,  7.41,  9.08,  1.25,  5.  ,  0.74],
       [ 5.76,  1.9 ,  1.79,  4.09,  1.54,  1.04, 15.  ,  0.76],
       [ 4.92,  7.8 ,  5.26,  7.15,  1.84,  1.25, 15.  ,  0.82],
       [ 3.44,  6.82,  5.43,  5.97,  8.91,  1.27, 12.  ,  0.83],
       [ 8.89,  7.72,  4.19,  7.64,  4.14,  1.14,  3.  ,  0.84],
       [ 7.57,  5.47,  4.67,  4.54,  9.68,  1.16, 15.  ,  0.85],
       [ 7.65,  2.07,  9.68,  9.75,  4.2 ,  1.28,  3.  ,  0.87],
       [ 8.88,  6.09,  6.65,  1.49,  3.98,  1.09, 10.  ,  0.96],
       [ 6.76,  9.71,  6.19,  2.13,  5.5 ,  1.11,  8.  ,  0.98]])
    index = [  1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
             14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,
             27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
             40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
             53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,
             66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
             79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,
             92,  93,  94,  95,  96,  97,  98,  99, 100]
    feature_names = ['Warranty Terms', 'Payment Terms', 'Technical Support',
       'Sustainability Efforts', 'Finp.nancial Stability', 'Unit Cost',
       'Lead Time (Days)', 'On Time Delivery']
    supplier = pd.DataFrame(data=data,index = index,columns = feature_names)
    return supplier


####***************************     1.2 Roller Cosater       ****************************###

def load_roller20():
    """ Roller coaster data
    

    Yields:
    -------
    Roller : a pandas DataFrame object that contains 20 samples with the columns of 
        'Name', 'Park', 'City/Region', 'City/State/Region', 'Country/Region',
       'Geographic Region', 'Construction', 'Type', 'Status',
       'Year/Date Opened', 'Height (feet)', ' Speed (mph)', 'Length (feet)',
       'Inversions (YES or NO)', 'Number of Inversions', 'Drop (feet)',
       'Duration (min:sec)', 'G Force', 'Vertical Angle (degrees)'

    Use :
        For evaluation model practice

    Reference:
        https://www.comap.com/highschool/contests/himcm/COMAP_RollerCoasterData_2018.xlsx

    """
    data = np.array([['10 Inversion Roller Coaster', 'Chimelong Paradise', 'Panyu',
        'Guangzhou, Guangdong', 'China', 'Asia', 'Steel', 'Sit Down',
        'Operating', 2006, 98.4, 45.0, 2788.8, 'YES', 10, np.nan,
        datetime.time(1, 32), np.nan, np.nan],
       ['Abismo', 'Parque de Atracciones de Madrid', 'Madrid', 'Madrid',
        'Spain', 'Europe', 'Steel', 'Sit Down', 'Operating', 2006, 151.6,
        65.2, 1476.4, 'YES', 2, np.nan, datetime.time(1, 0), 4, np.nan],
       ['Adrenaline Peak', 'Oaks Amusement Park', 'Portland', 'Oregon',
        'United States', 'North America', 'Steel', 'Sit Down',
        'Operating ', 2018, 72, 45.0, 1050.0, 'YES', 3, np.nan, np.nan, np.nan,
        97.0],
       ['Afterburn', 'Carowinds', 'Charlotte', 'North Carolina',
        'United States', 'North America', 'Steel', 'Inverted',
        'Operating', 1999, 113, 62.0, 2956.0, 'YES', 6, np.nan,
        datetime.time(2, 47), np.nan, np.nan],
       ['Alpengeist', 'Busch Gardens Williamsburg', 'Williamsburg',
        'Virginia', 'United States', 'North America', 'Steel',
        'Inverted', 'Operating', 1997, 195, 67.0, 3828.0, 'YES', 6, 170,
        datetime.time(3, 10), 3.7, np.nan],
       ['Alpina Blitz', 'Nigloland', 'Dolancourt', 'Champagne-Ardenne',
        'France', 'Europe', 'Steel', 'Sit Down', 'Operating', 2014,
        108.3, 51.6, 2358.9, 'NO', 0, np.nan, np.nan, 4.3, np.nan],
       ['Altair', 'Cinecittà World', 'Rome', 'Rome', 'Italy', 'Europe',
        'Steel', 'Sit Down', 'Operating', 2014, 108.3, 52.8, 2879.8,
        'YES', 10, np.nan, np.nan, np.nan, np.nan],
       ['American Eagle', 'Six Flags Great America', 'Gurnee',
        'Illinois', 'United States', 'North America', 'Wood', 'Sit Down',
        'Operating', 1981, 127, 66.0, 4650.0, 'NO', 0, 147,
        datetime.time(2, 23), np.nan, 55.0],
       ['Anaconda', 'Walygator Parc', 'Maizieres-les-Metz ', 'Lorraine',
        'France', 'Europe', 'Wood', 'Sit Down', 'Operating', 1989, 118.1,
        55.9, 3937.0, 'NO', 0, 40, datetime.time(2, 10), np.nan, np.nan],
       ['Apocalypse', 'Six Flags America', 'Upper Marlboro', 'Maryland',
        'United States', 'North America', 'Steel', 'Stand Up',
        'Operating', 2012, 100, 55.0, 2900.0, 'YES', 2, 90,
        datetime.time(2, 0), np.nan, np.nan],
       ['Apocalypse the Ride', 'Six Flags Magic Mountain', 'Valencia',
        'California', 'United States', 'North America', 'Wood',
        'Sit Down', 'Operating', 2009, 95, 50.1, 2877.0, 'NO', 0, 87.3,
        datetime.time(3, 0), np.nan, np.nan],
       ["Apollo's Chariot", 'Busch Gardens Williamsburg', 'Williamsburg',
        'Virginia', 'United States', 'North America', 'Steel',
        'Sit Down', 'Operating', 1999, 170, 73.0, 4882.0, 'NO', 0, 210,
        datetime.time(2, 15), 4.1, 65.0],
       ['Atlantica SuperSplash', 'Europa Park', 'Rust ',
        'Baden Wuerttemberg', 'Germany', 'Europe', 'Steel', 'Sit Down',
        'Operating', 2005, 98.4, 49.7, 1279.5, 'NO', 0, np.nan,
        datetime.time(3, 20), np.nan, np.nan],
       ['Backlot Stunt Coaster', 'Kings Island', 'Kings Mills', 'Ohio',
        'United States', 'North America', 'Steel', 'Sit Down',
        'Operating', 2005, 45.2, 40.0, 1960.0, 'NO', 0, 31.2,
        datetime.time(1, 4), np.nan, np.nan],
       ['Balder', 'Liseberg', 'Gothenburg', 'Vastra Gotaland', 'Sweden',
        'Europe', 'Wood', 'Sit Down', 'Operating', 2003, 118.1, 55.9,
        3510.5, 'NO', 0, np.nan, datetime.time(2, 8), np.nan, 70.0],
       ['Bandit', 'Movie Park Germany', 'Bottrop ',
        'North Rhine-Westphali', 'Germany', 'Europe', 'Wood', 'Sit Down',
        'Operating', 1999, 91.2, 49.7, 3605.7, 'NO', 0, 81.7,
        datetime.time(1, 30), np.nan, np.nan],
       ['Banshee', 'Kings Island', 'Mason', 'Ohio', 'United States',
        'North America', 'Steel', 'Inverted', 'Operating', 2014, 167,
        68.0, 4124.0, 'YES', 7, 150, datetime.time(2, 40), np.nan, np.nan],
       ['Bat', 'Kings Island', 'Kings Mills', 'Ohio', 'United States',
        'North America', 'Steel', 'Suspended', 'Operating', 1993, 78,
        51.0, 2352.0, 'NO', 0, np.nan, datetime.time(1, 52), np.nan, np.nan],
       ['Batman - The Dark Knight', 'Six Flags New England', 'Agawam',
        'Massachusetts', 'United States', 'North America', 'Steel',
        'Sit Down', 'Operating ', 2002, 117.8, 55.0, 2600.0, 'YES', 5,
        np.nan, datetime.time(2, 20), np.nan, np.nan],
       ['Batman The Ride', 'Six Flags Great America', 'Gurnee',
        'Illinois', 'United States', 'North America', 'Steel',
        'Inverted', 'Operating', 1992, 100, 50.0, 2700.0, 'YES', 5, np.nan,
        datetime.time(2, 0), np.nan, np.nan]])
    index = range(len(data))
    feature_names = ['Name', 'Park', 'City/Region', 'City/State/Region', 'Country/Region',
       'Geographic Region', 'Construction', 'Type', 'Status',
       'Year/Date Opened', 'Height (feet)', ' Speed (mph)', 'Length (feet)',
       'Inversions (YES or NO)', 'Number of Inversions', 'Drop (feet)',
       'Duration (min:sec)', 'G Force', 'Vertical Angle (degrees)']
    roller = pd.DataFrame(data=data,index = index,columns = feature_names)
    return roller

def fetch_roller():
    """ Roller coaster data(download data from 
    https://www.comap.com/highschool/contests/himcm/COMAP_RollerCoasterData_2018.xlsx)
    

    Yields:
    -------
    roller_all : a pandas DataFrame object that contains 48 samples with the columns of 
        'Name', 'Park', 'City/Region', 'City/State/Region', 'Country/Region',
       'Geographic Region', 'Construction', 'Type', 'Status',
       'Year/Date Opened', 'Height (feet)', ' Speed (mph)', 'Length (feet)',
       'Inversions (YES or NO)', 'Number of Inversions', 'Drop (feet)',
       'Duration (min:sec)', 'G Force', 'Vertical Angle (degrees)'

    Use :
        For evaluation model practice

    Reference:
        https://www.comap.com/highschool/contests/himcm/COMAP_RollerCoasterData_2018.xlsx

    """    
    url = 'https://www.comap.com/highschool/contests/himcm/COMAP_RollerCoasterData_2018.xlsx'
    roller_all = pd.read_excel(url)
    return roller_all


####***************************     1.3 Aircraft       ****************************###

def load_aircraft():
    """ Aircraft data
    

    Yields:
    -------
    aircraft : a pandas DataFrame object that contains 5 samples with the columns of 
        '最大速度(马赫)', '飞行范围(km)', '最大负载(磅)', '费用(美元)', '可靠性', '灵敏性'

    Use :
        For evaluation model practice

    Reference:
        Python数学实验与建模/司守奎,孙玺菁

    """

    data = np.array([[2.0e+00, 1.5e+03, 2.0e+04, 5.5e+06, 5.0e-01, 1.0e+00],
       [2.5e+00, 2.7e+03, 1.8e+04, 6.5e+06, 3.0e-01, 5.0e-01],
       [1.8e+00, 2.0e+03, 2.1e+04, 4.5e+06, 7.0e-01, 7.0e-01],
       [2.2e+00, 1.8e+03, 2.0e+04, 5.0e+06, 5.0e-01, 5.0e-01]])
    index = list('ABCD')
    feature_names = ['最大速度(马赫)', '飞行范围(km)', '最大负载(磅)', '费用(美元)', '可靠性', '灵敏性']
    aircraft = pd.DataFrame(data=data,index = index,columns = feature_names)
    return aircraft


####***************************     1.4 Hospital       ****************************###

def load_hospital():
    """ Hospital data
    

    Yields:
    -------
    Roller : a pandas DataFrame object that contains 11 samples with the columns of 
        'X1','X2',...,'X9'

    Use :
        For evaluation model practice

    Reference:
        Unkown

    """
    data = np.array([[100,90,100,84,90,100,100,100,100],
    [100,100,78.6,100,90,100,100,100,100],
    [75,100,85.7,100,90,100,100,100,100],
    [100,100,78.6,100,90,100,94.4,100,100],
    [100,90,100,100,100,90,100,100,80],
    [100,100,100,100,90,100,100,85.7,100],
    [100 ,100 ,78.6,100 ,90 , 100, 55.6,    100, 100],
    [87.5,100,85.7, 100 ,100 ,100, 100 ,100 ,100],
    [100 ,100, 92.9 , 100 ,80 , 100 ,100 ,100 ,100],
    [100,90 ,100 ,100,100, 100, 100, 100, 100],
    [100,100 ,92.9 , 100, 90 , 100, 100 ,100 ,100]])

    index = list('ABCDEFGHIJK')
    columns = ['X'+str(i) for i in range(1,10)]
    hospital= pd.DataFrame(data=data,index=index,columns=columns)
    return hospital

####***************************     1.5 Battery       ****************************###
def load_battery():
    """ Battery data
    

    Yields:
    -------
    battery : a pandas DataFrame object that contains 80 samples with the columns of 
        'Price(USD)', 'Weight(pounds)', 'Power Rating Capability(kWh)',
       'steady', 'peak', 'Length(inch)', 'Width(inch)', 'Height(inch)',
       'Depth of Discharge(DoD)%', 'Circles of Life Time',
       'Round Trip Efficiency(RET)%', 'Warranty(year)', 'Low Temperature',
       'High Temperature', 'Battery Type'

    Use :
        For evaluation model practice

    Reference:
        The author(Wang Haihua) collected data from the Internet

    """
    data = np.array([[10000.0, 297.0, 14.0, 5.0, 5.0, 20.8, 15.7, 41.0, 90.0, 6000,
        97.0, 15.0, 0.0, 50.0, 'LFP'],
       [13000.0, 297.0, 13.0, 2.0, 3.3, 20.8, 15.7, 41.0, 90.0, 6000,
        97.0, 10.0, 0.0, 50.0, 'NMC'],
       [9500.0, 348.0, 10.0, 2.0, 3.3, 68.0, 26.0, 11.0, 100.0, 10000,
        85.0, 10.0, -4.24, 36.72, 'LFP'],
       [5950.0, 331.0, 2.5, 2.0, 3.3, 25.0, 15.0, 56.0, 90.0, 10000,
        81.6, 10.0, -4.24, 36.72, 'LFP'],
       [11900.0, 381.0, 5.0, 2.0, 3.3, 25.0, 15.0, 56.0, 90.0, 10000,
        81.6, 10.0, -4.24, 36.72, 'LFP'],
       [17850.0, 474.0, 7.5, 2.0, 3.3, 25.0, 15.0, 56.0, 90.0, 10000,
        81.6, 10.0, -4.24, 36.72, 'LFP'],
       [23800.0, 585.0, 10.0, 2.0, 3.3, 25.0, 15.0, 56.0, 90.0, 10000,
        81.6, 10.0, -4.24, 36.72, 'LFP'],
       [5950.0, 735.0, 2.5, 2.0, 3.3, 25.0, 15.0, 56.0, 90.0, 10000,
        81.6, 10.0, -4.24, 36.72, 'LFP'],
       [8500.0, 269.0, 13.5, 5.8, 7.6, 45.3, 29.6, 5.75, 100.0, 3200,
        90.0, 10.0, -20.0, 50.0, 'NMC'],
       [7800.0, 214.0, 6.4, 3.3, 5.0, 51.3, 34.0, 7.2, 80.0, 3000, 92.5,
        10.0, -20.0, 50.0, 'NMC'],
       [15000.0, 106.0, 11.4, 3.0, 4.8, 39.0, 17.6, 5.9, 90.0, 5000,
        84.0, 10.0, -25.0, -70.0, 'Lithium-ion'],
       [20000.0, 106.0, 11.4, 3.0, 4.8, 39.0, 17.6, 5.9, 90.0, 5000,
        84.0, 10.0, -25.0, -70.0, 'Lithium-ion'],
       [1976.0, 55.12, 2.85, 5.0, 10.0, 17.32, 17.72, 2.13, 99.0, 5000,
        84.0, 10.0, -10.0, 50.0, 'Lithium-ion'],
       [5880.0, 214.0, 9.8, 5.0, 7.0, 35.7, 29.7, 8.1, 90.0, 4000, 95.0,
        10.0, -30.0, 55.0, 'NMC'],
       [12420.0, 476.0, 18.5, 5.0, 12.0, 38.8, 19.2, 21.3, 80.0, 6000,
        98.0, 10.0, 15.0, 35.0, 'Lithium-ion'],
       [20000.0, 318.036129032258, 15.9, 3.0, 10.0, 68.0, 22.0, 10.0,
        84.5, 6200, 96.5, 10.0, 12.0, 30.0, 'LFP'],
       [4500.0, 276.0, 4.2, 3.0, 6.0, 48.42, 35.0, 8.66, 80.0, 1000,
        91.17241379310343, 10.06451612903226, 15.0, 38.0, 'Lithium-ion'],
       [2995.0, 86.0, 3.4, 3.870769230769231, 6.85, 13.5, 14.0, 8.0,
        100.0, 10000, 80.0, 10.0, -20.0, 60.0, 'LFP'],
       [14990.0, 600.0, 11.6, 5.0, 8.5, 34.0, 14.0, 76.0, 85.0, 8000,
        92.5, 10.0, -4.24, 36.72, 'Lithium-ion'],
       [3000.0, 284.0, 6.0, 3.870769230769231, 6.85, 33.05793103448276,
        21.21137931034483, 34.07965517241379, 89.9423076923077, 6200,
        91.17241379310343, 10.06451612903226, 10.0, 35.0, 'NMC'],
       [16000.0, 318.036129032258, 10.0, 3.870769230769231, 6.85, 50.0,
        39.0, 9.84, 89.9423076923077, 5000, 91.17241379310343,
        10.06451612903226, 12.0, 55.0, 'LFP'],
       [10000.0, 287.0, 9.0, 3.4, 10.0, 22.0, 10.0, 68.0, 84.0, 6200,
        96.5, 10.0, -10.0, 45.0, 'Lithium-ion'],
       [7400.0, 318.036129032258, 6.3, 3.870769230769231, 6.85, 22.44,
        32.7, 17.7, 80.0, 6200, 96.0, 10.0, 10.0, 30.0, np.nan],
       [13000.0, 346.0, 10.0, 5.0, 7.6, 27.5, 50.0, 9.0,
        89.9423076923077, 6200, 96.6, 10.0, 0.0, 50.0, 'LiFePO4'],
       [15000.0, 346.0, 15.0, 3.870769230769231, 6.85, 33.05793103448276,
        21.21137931034483, 34.07965517241379, 89.9423076923077, 6200,
        96.6, 10.0, 0.0, 50.0, 'LiFePO4'],
       [19000.0, 346.0, 20.0, 3.870769230769231, 6.85, 33.05793103448276,
        21.21137931034483, 34.07965517241379, 89.9423076923077, 6200,
        96.6, 10.0, 0.0, 50.0, 'LiFePO4'],
       [10500.0, 326.0, 15.36, 12.8, 19.2, 25.0, 15.0, 9.0,
        89.9423076923077, 6200, 95.2, 10.0, -10.0, 50.0, 'LFP'],
       [15000.0, 487.0, 7.2, 4.0, 6.0, 39.0, 10.63, 26.77, 90.0, 6000,
        92.0, 15.0, 20.0, 50.0, 'Lithium-ion'],
       [11320.88235294118, 318.036129032258, 17.28, 5.0, 10.0,
        33.05793103448276, 21.21137931034483, 34.07965517241379,
        89.9423076923077, 6200, 91.17241379310343, 10.0, -4.24, 36.72,
        np.nan],
       [11320.88235294118, 318.036129032258, 9.799714285714288,
        3.870769230769231, 6.85, 33.05793103448276, 21.21137931034483,
        34.07965517241379, 89.9423076923077, 6200, 91.17241379310343,
        10.06451612903226, -4.24, 36.72, 'Lithium-ion'],
       [18000.0, 341.0, 10.1, 3.84, 5.0, 42.13, 26.14, 12.56, 100.0,
        4000, 96.0, 10.0, 0.0, 30.0, 'LFP'],
       [4299.0, 372.0, 12.0, 3.870769230769231, 6.85, 25.5, 14.0, 42.5,
        89.9423076923077, 3000, 100.0, 10.0, -4.24, 36.72, 'LiFePO4'],
       [2000.0, 30.0, 1.2, 1.5, 3.0, 33.05793103448276,
        21.21137931034483, 34.07965517241379, 100.0, 2000, 100.0, 7.0,
        -30.0, 55.0, np.nan],
       [20000.0, 218.0, 6.8, 3.870769230769231, 6.85, 16.57, 25.0, 191.0,
        80.0, 6600, 95.0, 5.0, 0.0, 50.0, 'Lithium-ion'],
       [7700.0, 360.0, 13.5, 3.870769230769231, 6.85, 23.6, 9.84, 70.0,
        96.0, 6200, 91.17241379310343, 10.0, -4.24, 36.72, 'Lithium-ion'],
       [12000.0, 266.0, 9.8, 5.0, 13.5, 33.05793103448276,
        21.21137931034483, 34.07965517241379, 89.9423076923077, 6200,
        91.17241379310343, 10.06451612903226, 0.0, 40.0, 'Lithium-ion']])

    index = range(1,data.shape[0]+1)
    columns = ['Price(USD)', 'Weight(pounds)', 'Power Rating Capability(kWh)',
       'steady', 'peak', 'Length(inch)', 'Width(inch)', 'Height(inch)',
       'Depth of Discharge(DoD)%', 'Circles of Life Time',
       'Round Trip Efficiency(RET)%', 'Warranty(year)', 'Low Temperature',
       'High Temperature', 'Battery Type']
    battery= pd.DataFrame(data=data,index=index,columns=columns)
    return battery

####***************************     1.6 University       ****************************###
def load_university():
    """ University data
    

    Yields:
    -------
    university : a pandas DataFrame object that contains 5 samples with the columns of 
       '人均专著' '生师比' '科研经费' '逾期毕业率'

    Use :
        For evaluation model practice

    Reference:
        unknown

    """

    university = pd.DataFrame(
    {'人均专著': [0.1, 0.2, 0.4, 0.9, 1.2], '生师比': [5, 6, 7, 10, 2], '科研经费': [5000, 6000, 7000, 10000, 400],
     '逾期毕业率': [4.7, 5.6, 6.7, 2.3, 1.8]}, index=['院校' + i for i in list('ABCDE')])
    return university

###########################################################################################
###############################     2 Optimization         ###############################
###########################################################################################

####***************************     2.1 Portfolio       ****************************###

def load_portfolio():
    """ Portfolio data
    

    Yields:
    -------
    portfolio : a pandas DataFrame object that contains 4 samples with the columns of 
       'r(%)','q(%)','p(%)','u(RMB)'

    Use :
        For optimization model practice

    Reference:
        Python数学实验与建模/司守奎,孙玺菁

    """
    data = np.array([[28,2.5,1,103],[21,1.5,2,198],[23,5.5,4.5,52],[25,2.6,6.5,40]])
    index = ['s'+str(i) for i in range(1,5)]
    columns = ['r(%)','q(%)','p(%)','u(RMB)']
    portfolio= pd.DataFrame(data=data,index=index,columns=columns)
    return portfolio

####***************************     2.2 Ambulance       ****************************###

def load_ambulance():
    """ Ambulance data
    

    Yields:
    -------
    ambulance : a pandas DataFrame object that contains 80 samples with the columns of 
       1,2,3,4,5,6

    Use :
        For optimization model practice

    Reference:
        https://www.comap.com/highschool/contests/himcm/2013problems.html

    """
    data = np.array([[1,1,0,0,0,0],
                    [1,1,1,0,0,0],
                    [0,0,1,0,1,1],
                    [0,0,1,1,0,0],
                    [0,0,0,1,1,1],
                    [0,0,1,0,1,1]])
    index = range(6)
    columns = range(6)
    ambulance = pd.DataFrame(data=data,index=index,columns=columns)
    return ambulance

####***************************     2.3 Oil       *************************************###
def load_oil():
    """ Oil data 

    Yields:
    -------
    oil : a pandas DataFrame object that contains 5 samples with the columns of 
       '价格','硬度'

    Use :
        For optimization model practice

    Reference:
        Python数学实验与建模/司守奎,孙玺菁

    """
    data = np.array([[110, 120, 130, 110, 115],[8.8,6.1,2.0,4.2,5.0]])
    index = ['价格','硬度']
    columns = ['VEG1','VEG2','OIL1','OIL2','OIL3']
    oil = pd.DataFrame(data=data,index=index,columns=columns).T
    return oil

####***************************     2.4 Factory(clothes) ****************************###
def load_factory_clothes():
    """ factory data 

    Yields:
    -------
    factory_clothes : a pandas DataFrame object that contains 3 samples with the columns of 
       '设备租金(元)', '材料成本(元/件)', '销售价格(元/件)', '人工工时(小时/件)', '设备工时(小时/件)',
       '设备可用工时'

    Use :
        For optimization model practice

    Reference:
        Unknown

    """
    data = np.array([[5000, 280, 400, 5, 3.0, 300],[2000, 30, 40, 1, 0.5, 300],
       [2000, 200, 300, 4, 2.0, 300]])
    index = list('ABC')
    columns = ['设备租金(元)', '材料成本(元/件)', '销售价格(元/件)', '人工工时(小时/件)', '设备工时(小时/件)',
       '设备可用工时']
    factory_clothes = pd.DataFrame(data=data,index=index,columns=columns)
    return factory_clothes

####***************************     2.5 Swim           ****************************###
def load_swim():
    """ Relay swimming data 

    Yields:
    -------
    swim : a pandas DataFrame object that contains 3 samples with the columns of 
       '泳姿1', '泳姿2', '泳姿3', '泳姿4'

    Use :
        For optimization model practice

    Reference:
        Unknown

    """
    data = np.array([[ 56, 74, 61, 63],
       [63, 69, 65, 71],
       [57, 77, 63, 67],
       [ 55, 76, 62, 62]])
    index = ['A','B', 'C','D']
    columns = ['泳姿1', '泳姿2', '泳姿3', '泳姿4']
    swim = pd.DataFrame(data=data,index=index,columns=columns)
    return swim

####***************************     2.6 Plants           ****************************###
def load_plant():
    """ Plant data 

    Yields:
    -------
    plant : a pandas DataFrame object that contains 48 samples with the columns of 
       'Name', 'comp_rate', 'MinAgeRequirement', 'MinDiplomaRequirement',
       'MinExperienceRequirementYear', 'PhysicalorIntellectual', 'WeeklyHour',
       'WeeklyWageRate', 'Type', 'Experience', 'Remote'

    Use :
        For optimization model practice

    Reference:
        https://www.comap.com/highschool/contests/himcm/HiMCM2020ProblemB_ThreatenedPlantsData.xlsx

    """
    data = np.array([['1-Flowering Plants-502', 0.66, 0.67, 0.6, 11616.17065,
        6053.241613, 5993.308527, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 23662.72079, 3],
       ['1-Flowering Plants-436', 0.66, 0.67, 0.22, 12356.61827,
        10136.97114, 10036.60509, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 32530.1945, 3],
       ['1-Flowering Plants-536', 0.99, 0.67, 0.87, 20849.6076,
        20643.17584, 20438.78797, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 61931.57141, 3],
       ['1-Flowering Plants-486', 0.66, 0.67, 0.71, 27820.04342,
        16009.42339, 10659.56679, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 78777.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0, 133266.0336, 10],
       ['1-Flowering Plants-183', 0.66, 0.67, 0.11, 22163.13537,
        18663.07903, 18478.29607, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 59304.51046999999, 3],
       ['1-Flowering Plants-480', 0.66, 0.67, 0.23, 34006.86642,
        25589.32522, 20002.07808, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 79598.26972, 3],
       ['1-Flowering Plants-135', 0.66, 0.67, 0.42, 30379.46733,
        28731.87394, 20446.5687, 5281.076721, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0, 84838.986691, 4],
       ['1-Flowering Plants-481', 0.66, 0.67, 0.72, 49766.12059,
        32021.64813, 26310.62443, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 108098.39315, 3],
       ['1-Flowering Plants-176', 0.66, 0.67, 0.38, 51068.48141,
        36324.25226, 35024.76457, 11166.43515, 4606.615162, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0, 138190.548552, 5],
       ['1-Flowering Plants-475', 0.66, 0.67, 0.27, 57432.7096,
        50302.83019, 47639.35705, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 155374.89684, 3],
       ['1-Flowering Plants-546', 0.66, 0.67, 0.49, 58550.24719,
        47101.06519, 42791.1973, 7610.93211, 7535.576346, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0, 163589.018136, 5],
       ['1-Flowering Plants-558', 0.66, 0.67, 0.75, 40739.62292,
        40336.26032, 39936.89141, 27010.727, 26743.29406, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0, 174766.79571, 5],
       ['1-Flowering Plants-553', 0.66, 0.67, 0.65, 71007.44136,
        68173.96111, 39374.39998, 4873.069304, 4824.821093, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0, 188253.692847, 5],
       ['1-Flowering Plants-442', 0.66, 0.67, 0.49, 45043.10422,
        38915.96946, 38530.66284, 38149.17113, 37771.45656, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0, 198410.36421, 5],
       ['1-Flowering Plants-537', 0.66, 0.67, 0.74, 89655.86031,
        67463.81568, 44999.31426, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 202118.99025, 3],
       ['1-Flowering Plants-548', 0.49, 0.67, 0.86, 53485.79576,
        52956.23342, 52431.91428, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 158873.94346, 3],
       ['1-Flowering Plants-426', 0.49, 0.67, 0.31, 62350.13418,
        61732.80612, 61121.59021, 10126.25454, 10025.9946, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0, 205356.77965, 5],
       ['1-Flowering Plants-452', 0.99, 0.67, 0.52, 130248.7251,
        127501.9685, 95942.07527, 34282.88255, 33943.44807, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0, 421919.09949, 5],
       ['1-Flowering Plants-173', 0.66, 0.67, 0.14, 59035.9201,
        27474.85445, 27202.82619, 13730.79947, 13594.85096, 13460.24848,
        13326.97869, 13195.02841, 13064.38456, 12935.03422, 12806.96458,
        12680.16295, 12554.61678, 12430.31364, 12307.24123, 12185.38736,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 281985.61207, 16],
       ['1-Flowering Plants-455', 0.66, 1.0, 0.27, 145790.7244,
        143253.7121, 141835.3585, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0, 430879.795, 3]])
    columns = ['Name', 'comp_rate', 'MinAgeRequirement', 'MinDiplomaRequirement',
       'MinExperienceRequirementYear', 'PhysicalorIntellectual', 'WeeklyHour',
       'WeeklyWageRate', 'Type', 'Experience', 'Remote']
    plant = pd.DataFrame(data=data,columns=columns)
    return plant

####***************************  2.7 Air tickets price   ****************************###
def load_tickets():
    """ Air ticket price data 

    Yields:
    -------
    tickets : a pandas DataFrame object constructed by the adjacency matrix between six cities

    Use :
        For optimization model practice

    Reference:
        司守奎 数学建模算法与应用,P41,例4.1

    """
    tickets = pd.DataFrame([[0, 50, 0, 40, 25, 10],  
                      [50, 0, 15, 20, 0, 25],
                      [0, 15, 0, 10, 20, 0],
                      [40, 20, 10, 0, 10, 25],
                      [25, 0, 20, 10, 0 ,55],
                      [10, 25, 0, 25, 55, 0]],index=list('ABCDEF'),columns=list('ABCDEF'))
    return tickets
    
    
####***************************  2.8 Fire station   ****************************###
def load_firestation():
    """ Fire station data 

    Yields:
    -------
    firestation : a pandas DataFrame object constructed by the weighted adjacency matrix between eight district;
        aij is the distance from i district to j district
    Use :
        For optimization model practice

    Reference:
        youcans Python小白的数学建模课 https://www.zhihu.com/column/c_1381900867424075776

    """
    firestation = pd.DataFrame(np.array([[ 7, 12, 18, 20, 24, 26, 25, 28],
       [14,  5,  8, 15, 16, 18, 18, 18],
       [19,  9,  4, 14, 10, 22, 16, 13],
       [14, 15, 15, 10, 18, 15, 14, 18],
       [20, 18, 12, 20,  9, 25, 14, 12],
       [18, 21, 20, 16, 20,  6, 10, 15],
       [22, 18, 20, 15, 16, 15,  5,  9],
       [30, 22, 15, 20, 14, 18,  8,  6]]))
    return firestation
    

###########################################################################################
###############################     3 Change        ###############################
###########################################################################################

####***************************     3.1 Shanghai Confirms(from March 1)       ****************************###

def load_shanghaicases():
    """ Epidemic data in Shanghai(2022)

    Yields:
    -------
    shanghai : a pandas DataFrame object that contains 41 samples with the columns of 
       '新增确诊', '新增无症状', '无症状者转归', '隔离管控确诊', '隔离管控无症状'

    Use :
        For change model practice

    Reference:
        The official account "Shanghai Release"

    """    
    data = np.array([[1.0000e+00, 1.0000e+00,        np.nan,        np.nan, 1.0000e+00],
       [3.0000e+00, 5.0000e+00,        np.nan,        np.nan, 5.0000e+00],
       [2.0000e+00, 1.4000e+01,        np.nan,        np.nan, 1.4000e+01],
       [3.0000e+00, 1.6000e+01,        np.nan,        np.nan, 1.5000e+01],
       [0.0000e+00, 2.8000e+01,        np.nan,        np.nan, 2.8000e+01],
       [3.0000e+00, 4.5000e+01,        np.nan,        np.nan, 4.4000e+01],
       [4.0000e+00, 5.1000e+01,        np.nan,        np.nan, 5.1000e+01],
       [3.0000e+00, 6.2000e+01,        np.nan,        np.nan, 6.1000e+01],
       [4.0000e+00, 7.6000e+01,        np.nan,        np.nan, 6.4000e+01],
       [1.1000e+01, 6.4000e+01,        np.nan, 0.0000e+00, 6.1000e+01],
       [5.0000e+00, 7.8000e+01,        np.nan, 4.0000e+00, 5.7000e+01],
       [1.0000e+00, 6.4000e+01,        np.nan, 1.0000e+00, 6.0000e+01],
       [4.1000e+01, 1.2800e+02, 2.0000e+00, 3.2000e+01, 9.0000e+01],
       [9.0000e+00, 1.3000e+02,        np.nan, 5.0000e+00, 1.0200e+02],
       [5.0000e+00, 1.9700e+02,        np.nan, 4.0000e+00, 1.3500e+02],
       [8.0000e+00, 1.5000e+02, 1.0000e+00, 2.0000e+00, 6.9000e+01],
       [5.7000e+01, 2.0300e+02,        np.nan, 2.0000e+00, 1.0300e+02],
       [8.0000e+00, 3.6600e+02,        np.nan, 4.0000e+00, 1.7800e+02],
       [1.7000e+01, 4.9200e+02, 6.0000e+00, 9.0000e+00, 2.3200e+02],
       [2.4000e+01, 7.3400e+02,        np.nan, 2.2000e+01, 6.5200e+02],
       [3.1000e+01, 8.6500e+02,        np.nan, 3.0000e+01, 7.4900e+02],
       [4.0000e+00, 9.7700e+02,        np.nan, 3.0000e+00, 8.8600e+02],
       [4.0000e+00, 9.7900e+02,        np.nan, 4.0000e+00, 8.7800e+02],
       [2.9000e+01, 1.5800e+03,        np.nan, 1.2000e+01, 1.4550e+03],
       [3.8000e+01, 2.2310e+03, 5.0000e+00, 3.0000e+00, 1.7730e+03],
       [4.5000e+01, 2.6310e+03,        np.nan, 2.7000e+01, 2.3630e+03],
       [5.0000e+01, 3.4500e+03,        np.nan, 1.7000e+01, 2.8330e+03],
       [9.6000e+01, 4.3810e+03, 2.1000e+01, 7.0000e+00, 3.8240e+03],
       [3.2600e+02, 5.6560e+03, 1.8000e+01, 1.7000e+01, 5.1310e+03],
       [3.5500e+02, 5.2980e+03, 1.6000e+01, 1.0000e+01, 4.4770e+03],
       [3.5800e+02, 4.1440e+03, 2.0000e+01, 8.0000e+00, 3.7100e+03],
       [2.6000e+02, 6.0510e+03, 8.0000e+00, 4.0200e+02, 5.4020e+03],
       [4.3800e+02, 7.7880e+03, 7.3000e+01, 1.6000e+01, 6.7730e+03],
       [4.2500e+02, 8.5810e+03, 7.1000e+01, 7.0000e+00, 7.9200e+03],
       [2.6800e+02, 1.3086e+04, 4.0000e+00, 1.4000e+01, 1.2592e+04],
       [3.1100e+02, 1.6766e+04, 4.0000e+01, 4.0000e+00, 1.6256e+04],
       [3.2200e+02, 1.9660e+04, 1.5000e+01, 1.2000e+01, 1.9027e+04],
       [8.2400e+02, 2.0398e+04, 3.2300e+02, 1.2100e+02, 1.9798e+04],
       [1.0150e+03, 2.2609e+04, 4.2000e+02, 3.0100e+02, 2.1853e+04],
       [1.0060e+03, 2.3937e+04, 1.9100e+02, 2.2800e+02, 2.3412e+04],
       [9.1400e+02, 2.5173e+04, 4.7000e+01, 5.6400e+02, 2.4230e+04],
       [9.9400e+02, 2.2348e+04, 2.7300e+02, 4.3900e+02, 2.1844e+04]])
    index = range(len(data))
    columns = ['新增确诊', '新增无症状', '无症状者转归', '隔离管控确诊', '隔离管控无症状']
    shanghai = pd.DataFrame(data=data,index=index,columns=columns)
    return shanghai

####***************************     3.2 Population      ****************************###
def load_population():
    """ Population data of U.S.(1970-2010)

    Yields:
    -------
    df : a pandas DataFrame object that contains 22 samples with the columns of 
      '年份','人口'

    Use :
        For change model practice

    Reference:
        Unknown

    """ 
    df = pd.DataFrame()
    df["年份"] = [int(i) for i in  range(1790,2010,10)]
    df["人口"] = [3.9,5.3,7.2,9.6,12.9,17.1,23.2,31.4,38.6,50.2,62.9,76,92,106.5,123.2,131.7,150.7,179.3,204,226.5,251.4,281.4]
    return df


###########################################################################################
###############################     4 Prediction         ###############################
###########################################################################################

####***************************     4.1 Restaurant     ****************************###
def load_restaurant():
    """ restaurant sales data

    Yields:
    -------
    restaurant : a pandas DataFrame object that contains 37 samples with the columns of 
       'day','sales'

    Use :
        For prediction model practice

    Reference:
        Unknown

    """ 
    data = np.array([
       [   1, 3023],
       [   2, 3039],
       [   3, 3056],
       [   4, 3138],
       [   5, 3188],
       [   6, 3224],
       [   7, 3226],
       [   8, 3029],
       [   9, 2859],
       [  10, 2870],
       [  11, 2910],
       [  12, 3012],
       [  13, 3142],
       [  14, 3252],
       [  15, 3342],
       [  16, 3365],
       [  17, 3339],
       [  18, 3345],
       [  19, 3421],
       [  20, 3443],
       [  21, 3428],
       [  22, 3554],
       [  23, 3615],
       [  24, 3646],
       [  25, 3614],
       [  26, 3574],
       [  27, 3635],
       [  28, 3738],
       [  29, 3707],
       [  30, 3827],
       [  31, 4039],
       [  32, 4210],
       [  33, 4493],
       [  34, 4560],
       [  35, 4637],
       [  36, 4755],
       [  37, 4817]])
    index = range(1,38)
    columns = ['day','sales']
    restaurant = pd.DataFrame(data=data,index=index,columns=columns)
    return restaurant


####***************************     4.2 Titanic     ****************************###
def load_titanic():
    """ Titanic data

    Yields:
    -------
    titanic : a pandas DataFrame object that contains 80 samples with the columns of 
       'Name', 'comp_rate', 'MinAgeRequirement', 'MinDiplomaRequirement',
       'MinExperienceRequirementYear', 'PhysicalorIntellectual', 'WeeklyHour',
       'WeeklyWageRate', 'Type', 'Experience', 'Remote''新增确诊', '新增无症状', '无症状者转归', '隔离管控确诊', '隔离管控无症状'

    Use :
        For change model practice

    Reference:
        Kaggle

    """ 
    data = np.array([[1, 0, 3, 'Braund, Mr. Owen Harris', 'male', 22.0, 1, 0,
        'A/5 21171', 7.25, np.nan, 'S'],
       [2, 1, 1, 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)',
        'female', 38.0, 1, 0, 'PC 17599', 71.2833, 'C85', 'C'],
       [3, 1, 3, 'Heikkinen, Miss. Laina', 'female', 26.0, 0, 0,
        'STON/O2. 3101282', 7.925, np.nan, 'S'],
       [4, 1, 1, 'Futrelle, Mrs. Jacques Heath (Lily May Peel)',
        'female', 35.0, 1, 0, '113803', 53.1, 'C123', 'S'],
       [5, 0, 3, 'Allen, Mr. William Henry', 'male', 35.0, 0, 0,
        '373450', 8.05, np.nan, 'S'],
       [6, 0, 3, 'Moran, Mr. James', 'male', np.nan, 0, 0, '330877', 8.4583,
        np.nan, 'Q'],
       [7, 0, 1, 'McCarthy, Mr. Timothy J', 'male', 54.0, 0, 0, '17463',
        51.8625, 'E46', 'S'],
       [8, 0, 3, 'Palsson, Master. Gosta Leonard', 'male', 2.0, 3, 1,
        '349909', 21.075, np.nan, 'S'],
       [9, 1, 3, 'Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)',
        'female', 27.0, 0, 2, '347742', 11.1333, np.nan, 'S'],
       [10, 1, 2, 'Nasser, Mrs. Nicholas (Adele Achem)', 'female', 14.0,
        1, 0, '237736', 30.0708, np.nan, 'C'],
       [11, 1, 3, 'Sandstrom, Miss. Marguerite Rut', 'female', 4.0, 1, 1,
        'PP 9549', 16.7, 'G6', 'S'],
       [12, 1, 1, 'Bonnell, Miss. Elizabeth', 'female', 58.0, 0, 0,
        '113783', 26.55, 'C103', 'S'],
       [13, 0, 3, 'Saundercock, Mr. William Henry', 'male', 20.0, 0, 0,
        'A/5. 2151', 8.05, np.nan, 'S'],
       [14, 0, 3, 'Andersson, Mr. Anders Johan', 'male', 39.0, 1, 5,
        '347082', 31.275, np.nan, 'S'],
       [15, 0, 3, 'Vestrom, Miss. Hulda Amanda Adolfina', 'female', 14.0,
        0, 0, '350406', 7.8542, np.nan, 'S'],
       [16, 1, 2, 'Hewlett, Mrs. (Mary D Kingcome) ', 'female', 55.0, 0,
        0, '248706', 16.0, np.nan, 'S'],
       [17, 0, 3, 'Rice, Master. Eugene', 'male', 2.0, 4, 1, '382652',
        29.125, np.nan, 'Q'],
       [18, 1, 2, 'Williams, Mr. Charles Eugene', 'male', np.nan, 0, 0,
        '244373', 13.0, np.nan, 'S'],
       [19, 0, 3,
        'Vander Planke, Mrs. Julius (Emelia Maria Vandemoortele)',
        'female', 31.0, 1, 0, '345763', 18.0, np.nan, 'S'],
       [20, 1, 3, 'Masselmani, Mrs. Fatima', 'female', np.nan, 0, 0, '2649',
        7.225, np.nan, 'C'],
       [21, 0, 2, 'Fynney, Mr. Joseph J', 'male', 35.0, 0, 0, '239865',
        26.0, np.nan, 'S'],
       [22, 1, 2, 'Beesley, Mr. Lawrence', 'male', 34.0, 0, 0, '248698',
        13.0, 'D56', 'S'],
       [23, 1, 3, 'McGowan, Miss. Anna "Annie"', 'female', 15.0, 0, 0,
        '330923', 8.0292, np.nan, 'Q'],
       [24, 1, 1, 'Sloper, Mr. William Thompson', 'male', 28.0, 0, 0,
        '113788', 35.5, 'A6', 'S'],
       [25, 0, 3, 'Palsson, Miss. Torborg Danira', 'female', 8.0, 3, 1,
        '349909', 21.075, np.nan, 'S'],
       [26, 1, 3,
        'Asplund, Mrs. Carl Oscar (Selma Augusta Emilia Johansson)',
        'female', 38.0, 1, 5, '347077', 31.3875, np.nan, 'S'],
       [27, 0, 3, 'Emir, Mr. Farred Chehab', 'male', np.nan, 0, 0, '2631',
        7.225, np.nan, 'C'],
       [28, 0, 1, 'Fortune, Mr. Charles Alexander', 'male', 19.0, 3, 2,
        '19950', 263.0, 'C23 C25 C27', 'S'],
       [29, 1, 3, 'O\'Dwyer, Miss. Ellen "Nellie"', 'female', np.nan, 0, 0,
        '330959', 7.8792, np.nan, 'Q'],
       [30, 0, 3, 'Todoroff, Mr. Lalio', 'male', np.nan, 0, 0, '349216',
        7.8958, np.nan, 'S'],
       [31, 0, 1, 'Uruchurtu, Don. Manuel E', 'male', 40.0, 0, 0,
        'PC 17601', 27.7208, np.nan, 'C'],
       [32, 1, 1, 'Spencer, Mrs. William Augustus (Marie Eugenie)',
        'female', np.nan, 1, 0, 'PC 17569', 146.5208, 'B78', 'C'],
       [33, 1, 3, 'Glynn, Miss. Mary Agatha', 'female', np.nan, 0, 0,
        '335677', 7.75, np.nan, 'Q'],
       [34, 0, 2, 'Wheadon, Mr. Edward H', 'male', 66.0, 0, 0,
        'C.A. 24579', 10.5, np.nan, 'S'],
       [35, 0, 1, 'Meyer, Mr. Edgar Joseph', 'male', 28.0, 1, 0,
        'PC 17604', 82.1708, np.nan, 'C'],
       [36, 0, 1, 'Holverson, Mr. Alexander Oskar', 'male', 42.0, 1, 0,
        '113789', 52.0, np.nan, 'S'],
       [37, 1, 3, 'Mamee, Mr. Hanna', 'male', np.nan, 0, 0, '2677', 7.2292,
        np.nan, 'C'],
       [38, 0, 3, 'Cann, Mr. Ernest Charles', 'male', 21.0, 0, 0,
        'A./5. 2152', 8.05, np.nan, 'S'],
       [39, 0, 3, 'Vander Planke, Miss. Augusta Maria', 'female', 18.0,
        2, 0, '345764', 18.0, np.nan, 'S'],
       [40, 1, 3, 'Nicola-Yarred, Miss. Jamila', 'female', 14.0, 1, 0,
        '2651', 11.2417, np.nan, 'C'],
       [41, 0, 3, 'Ahlin, Mrs. Johan (Johanna Persdotter Larsson)',
        'female', 40.0, 1, 0, '7546', 9.475, np.nan, 'S'],
       [42, 0, 2,
        'Turpin, Mrs. William John Robert (Dorothy Ann Wonnacott)',
        'female', 27.0, 1, 0, '11668', 21.0, np.nan, 'S'],
       [43, 0, 3, 'Kraeff, Mr. Theodor', 'male', np.nan, 0, 0, '349253',
        7.8958, np.nan, 'C'],
       [44, 1, 2, 'Laroche, Miss. Simonne Marie Anne Andree', 'female',
        3.0, 1, 2, 'SC/Paris 2123', 41.5792, np.nan, 'C'],
       [45, 1, 3, 'Devaney, Miss. Margaret Delia', 'female', 19.0, 0, 0,
        '330958', 7.8792, np.nan, 'Q'],
       [46, 0, 3, 'Rogers, Mr. William John', 'male', np.nan, 0, 0,
        'S.C./A.4. 23567', 8.05, np.nan, 'S'],
       [47, 0, 3, 'Lennon, Mr. Denis', 'male', np.nan, 1, 0, '370371', 15.5,
        np.nan, 'Q'],
       [48, 1, 3, "O'Driscoll, Miss. Bridget", 'female', np.nan, 0, 0,
        '14311', 7.75, np.nan, 'Q'],
       [49, 0, 3, 'Samaan, Mr. Youssef', 'male', np.nan, 2, 0, '2662',
        21.6792, np.nan, 'C'],
       [50, 0, 3, 'Arnold-Franchi, Mrs. Josef (Josefine Franchi)',
        'female', 18.0, 1, 0, '349237', 17.8, np.nan, 'S'],
       [51, 0, 3, 'Panula, Master. Juha Niilo', 'male', 7.0, 4, 1,
        '3101295', 39.6875, np.nan, 'S'],
       [52, 0, 3, 'Nosworthy, Mr. Richard Cater', 'male', 21.0, 0, 0,
        'A/4. 39886', 7.8, np.nan, 'S'],
       [53, 1, 1, 'Harper, Mrs. Henry Sleeper (Myna Haxtun)', 'female',
        49.0, 1, 0, 'PC 17572', 76.7292, 'D33', 'C'],
       [54, 1, 2, 'Faunthorpe, Mrs. Lizzie (Elizabeth Anne Wilkinson)',
        'female', 29.0, 1, 0, '2926', 26.0, np.nan, 'S'],
       [55, 0, 1, 'Ostby, Mr. Engelhart Cornelius', 'male', 65.0, 0, 1,
        '113509', 61.9792, 'B30', 'C'],
       [56, 1, 1, 'Woolner, Mr. Hugh', 'male', np.nan, 0, 0, '19947', 35.5,
        'C52', 'S'],
       [57, 1, 2, 'Rugg, Miss. Emily', 'female', 21.0, 0, 0,
        'C.A. 31026', 10.5, np.nan, 'S'],
       [58, 0, 3, 'Novel, Mr. Mansouer', 'male', 28.5, 0, 0, '2697',
        7.2292, np.nan, 'C'],
       [59, 1, 2, 'West, Miss. Constance Mirium', 'female', 5.0, 1, 2,
        'C.A. 34651', 27.75, np.nan, 'S'],
       [60, 0, 3, 'Goodwin, Master. William Frederick', 'male', 11.0, 5,
        2, 'CA 2144', 46.9, np.nan, 'S'],
       [61, 0, 3, 'Sirayanian, Mr. Orsen', 'male', 22.0, 0, 0, '2669',
        7.2292, np.nan, 'C'],
       [62, 1, 1, 'Icard, Miss. Amelie', 'female', 38.0, 0, 0, '113572',
        80.0, 'B28', np.nan],
       [63, 0, 1, 'Harris, Mr. Henry Birkhardt', 'male', 45.0, 1, 0,
        '36973', 83.475, 'C83', 'S'],
       [64, 0, 3, 'Skoog, Master. Harald', 'male', 4.0, 3, 2, '347088',
        27.9, np.nan, 'S'],
       [65, 0, 1, 'Stewart, Mr. Albert A', 'male', np.nan, 0, 0, 'PC 17605',
        27.7208, np.nan, 'C'],
       [66, 1, 3, 'Moubarek, Master. Gerios', 'male', np.nan, 1, 1, '2661',
        15.2458, np.nan, 'C'],
       [67, 1, 2, 'Nye, Mrs. (Elizabeth Ramell)', 'female', 29.0, 0, 0,
        'C.A. 29395', 10.5, 'F33', 'S'],
       [68, 0, 3, 'Crease, Mr. Ernest James', 'male', 19.0, 0, 0,
        'S.P. 3464', 8.1583, np.nan, 'S'],
       [69, 1, 3, 'Andersson, Miss. Erna Alexandra', 'female', 17.0, 4,
        2, '3101281', 7.925, np.nan, 'S'],
       [70, 0, 3, 'Kink, Mr. Vincenz', 'male', 26.0, 2, 0, '315151',
        8.6625, np.nan, 'S'],
       [71, 0, 2, 'Jenkin, Mr. Stephen Curnow', 'male', 32.0, 0, 0,
        'C.A. 33111', 10.5, np.nan, 'S'],
       [72, 0, 3, 'Goodwin, Miss. Lillian Amy', 'female', 16.0, 5, 2,
        'CA 2144', 46.9, np.nan, 'S'],
       [73, 0, 2, 'Hood, Mr. Ambrose Jr', 'male', 21.0, 0, 0,
        'S.O.C. 14879', 73.5, np.nan, 'S'],
       [74, 0, 3, 'Chronopoulos, Mr. Apostolos', 'male', 26.0, 1, 0,
        '2680', 14.4542, np.nan, 'C'],
       [75, 1, 3, 'Bing, Mr. Lee', 'male', 32.0, 0, 0, '1601', 56.4958,
        np.nan, 'S'],
       [76, 0, 3, 'Moen, Mr. Sigurd Hansen', 'male', 25.0, 0, 0,
        '348123', 7.65, 'F G73', 'S'],
       [77, 0, 3, 'Staneff, Mr. Ivan', 'male', np.nan, 0, 0, '349208',
        7.8958, np.nan, 'S'],
       [78, 0, 3, 'Moutal, Mr. Rahamin Haim', 'male', np.nan, 0, 0,
        '374746', 8.05, np.nan, 'S'],
       [79, 1, 2, 'Caldwell, Master. Alden Gates', 'male', 0.83, 0, 2,
        '248738', 29.0, np.nan, 'S'],
       [80, 1, 3, 'Dowdell, Miss. Elizabeth', 'female', 30.0, 0, 0,
        '364516', 12.475, np.nan, 'S']])
    columns = ['Name', 'comp_rate', 'MinAgeRequirement', 'MinDiplomaRequirement',
       'MinExperienceRequirementYear', 'PhysicalorIntellectual', 'WeeklyHour',
       'WeeklyWageRate', 'Type', 'Experience', 'Remote']
    titanic = pd.DataFrame(data=data,columns=columns)
    return titanic

def fetch_mead():
    """ Lake Mead's monthly elevation data

    Yields:
    -------
    mead : a pandas DataFrame object that contains  samples with the columns of 
       'Name', 'comp_rate', 'MinAgeRequirement', 'MinDiplomaRequirement',
       'MinExperienceRequirementYear', 'PhysicalorIntellectual', 'WeeklyHour',
       'WeeklyWageRate', 'Type', 'Experience', 'Remote''新增确诊', '新增无症状', '无症状者转归', '隔离管控确诊', '隔离管控无症状'

    Use :
        For change model practice

    Reference:
        https://www.comap.com/highschool/contests/himcm/2021_Problems/2021_HiMCM_LakeMead_MonthlyElevationData.xlsx

    """ 
    url = 'https://www.comap.com/highschool/contests/himcm/2021_Problems/2021_HiMCM_LakeMead_MonthlyElevationData.xlsx'
    mead = pd.read_excel(url)
    return mead


###########################################################################################
###############################     5 Explaination        ###############################
###########################################################################################

####***************************     5.1 Adult_us       ****************************###

def load_adult():
    """ Adult data

    Yields:
    -------
    adult : a pandas DataFrame object that contains 80 samples with the columns of 
       'sex', 'age', 'educ', 'hours', 'income_more_50K''Name'

    Use :
        For explaination model practice

    Reference:
        Unknown

    """ 
    data = np.array([[' Male', 39, 13, 40, 0],
       [' Male', 50, 13, 13, 0],
       [' Male', 38, 9, 40, 0],
       [' Male', 53, 7, 40, 0],
       [' Female', 28, 13, 40, 0],
       [' Female', 37, 14, 40, 0],
       [' Female', 49, 5, 16, 0],
       [' Male', 52, 9, 45, 1],
       [' Female', 31, 14, 50, 1],
       [' Male', 42, 13, 40, 1],
       [' Male', 37, 10, 80, 1],
       [' Male', 30, 13, 40, 1],
       [' Female', 23, 13, 30, 0],
       [' Male', 32, 12, 50, 0],
       [' Male', 40, 11, 40, 1],
       [' Male', 34, 4, 45, 0],
       [' Male', 25, 9, 35, 0],
       [' Male', 32, 9, 40, 0],
       [' Male', 38, 7, 50, 0],
       [' Female', 43, 14, 45, 1],
       [' Male', 40, 16, 60, 1],
       [' Female', 54, 9, 20, 0],
       [' Male', 35, 5, 40, 0],
       [' Male', 43, 7, 40, 0],
       [' Female', 59, 9, 40, 0],
       [' Male', 56, 13, 40, 1],
       [' Male', 19, 9, 40, 0],
       [' Male', 54, 10, 60, 1],
       [' Male', 39, 9, 80, 0],
       [' Male', 49, 9, 40, 0],
       [' Male', 23, 12, 52, 0],
       [' Male', 20, 10, 44, 0],
       [' Male', 45, 13, 40, 0],
       [' Male', 30, 10, 40, 0],
       [' Male', 22, 10, 15, 0],
       [' Male', 48, 7, 40, 0],
       [' Male', 21, 10, 40, 0],
       [' Female', 19, 9, 25, 0],
       [' Male', 31, 10, 38, 1],
       [' Male', 48, 12, 40, 0],
       [' Male', 31, 5, 43, 0],
       [' Male', 53, 13, 40, 0],
       [' Male', 24, 13, 50, 0],
       [' Female', 49, 9, 40, 0],
       [' Male', 25, 9, 35, 0],
       [' Male', 57, 13, 40, 1],
       [' Male', 53, 9, 38, 0],
       [' Female', 44, 14, 40, 0],
       [' Male', 41, 11, 40, 0],
       [' Male', 29, 11, 43, 0],
       [' Female', 25, 10, 40, 0],
       [' Female', 18, 9, 30, 0],
       [' Female', 47, 15, 60, 1],
       [' Male', 50, 13, 55, 1],
       [' Male', 47, 9, 60, 0],
       [' Male', 43, 10, 40, 1],
       [' Male', 46, 3, 40, 0],
       [' Male', 35, 11, 40, 0],
       [' Male', 41, 9, 48, 0],
       [' Male', 30, 9, 40, 0],
       [' Male', 30, 13, 40, 0],
       [' Male', 32, 4, 40, 0],
       [' Male', 48, 9, 40, 0],
       [' Male', 42, 16, 45, 1],
       [' Male', 29, 10, 58, 0],
       [' Male', 36, 9, 40, 0],
       [' Female', 28, 10, 40, 0],
       [' Female', 53, 9, 40, 1],
       [' Male', 49, 10, 50, 1],
       [' Male', 25, 10, 40, 0],
       [' Male', 19, 10, 32, 0],
       [' Female', 31, 13, 40, 0],
       [' Male', 29, 13, 70, 1],
       [' Male', 23, 10, 40, 0],
       [' Male', 79, 10, 20, 0],
       [' Male', 27, 9, 40, 0],
       [' Male', 40, 12, 40, 0],
       [' Male', 67, 6, 2, 0],
       [' Female', 18, 7, 22, 0],
       [' Male', 31, 4, 40, 0],
       [' Male', 18, 9, 30, 0],
       [' Male', 52, 13, 40, 0],
       [' Female', 46, 9, 40, 0],
       [' Male', 59, 9, 48, 0],
       [' Female', 44, 9, 40, 1],
       [' Female', 53, 9, 35, 0],
       [' Male', 49, 9, 40, 1],
       [' Male', 33, 14, 50, 0],
       [' Male', 30, 5, 40, 0],
       [' Female', 43, 16, 50, 1],
       [' Male', 57, 11, 40, 0],
       [' Female', 37, 10, 40, 0],
       [' Female', 28, 10, 25, 0],
       [' Female', 30, 9, 35, 0],
       [' Male', 34, 13, 40, 1],
       [' Male', 29, 10, 50, 0],
       [' Male', 48, 16, 60, 1],
       [' Male', 37, 10, 48, 1],
       [' Female', 48, 12, 40, 0],
       [' Male', 32, 9, 40, 0]])
    columns = ['sex', 'age', 'educ', 'hours', 'income_more_50K']
    adult = pd.DataFrame(data=data,columns=columns)
    return adult

####***************************     5.2 Trialon       ****************************###
def fetch_trialon():
    """ Trialon data

    Yields:
    -------
    trialon : a pandas DataFrame object that contains 3217 samples with the columns of 
       'BIB NO.', 'AGE', 'GENDER', 'CATEGORY', 'SWIM', 'T1', 'BIKE', 'T2',
       'RUN', 'FINALTM'

    Use :
        For explaination model practice

    Reference:
        https://www.comap.com/highschool/contests/himcm/2016_Files/HiMCM_TriDataSet.xlsx

    """ 
    url = 'https://www.comap.com/highschool/contests/himcm/2016_Files/HiMCM_TriDataSet.xlsx'
    trialon = pd.read_excel(url)
    return trialon


###########################################################################################
###############################     6 Simulation       ###############################
###########################################################################################

####***************************     6.1 Li Mei's activities       ****************************###
def load_activity():
    """ Li Mei's daily activities  data

    Yields:
    -------
    activity : a pandas DataFrame object constructed by a markov transfer matrix

    Use :
        For simulation model practice

    Reference:
        ThomsonRen  github https://github.com/ThomsonRen/mathmodels
    """
    data = np.array([[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]])
    activity = pd.DataFrame(data,index=["Sleep","Icecream","Run"],columns=["Sleep","Icecream","Run"])
    return activity

####***************************     6.2 Parties to join in       ****************************###
def load_party():
    """ People' choices to different parties 

    Yields:
    -------
    party : a pandas DataFrame object constructed by a markov transfer matrix

    Use :
        For simulation model practice

    Reference:
        ThomsonRen  github https://github.com/ThomsonRen/mathmodels
    """
    data = np.array([[0.5, 0.4, 0.1],
       [0.7, 0.2, 0.1],
       [0.2, 0.4, 0.4]])
    party = pd.DataFrame(data,index=['工党', '保守党', '自由党'],columns=['工党', '保守党', '自由党'])
    return party

####***************************     6.3 Education      ****************************###
def load_education():
    """

    Some sociological findings point out that the educational level of children depends on the educational level of their parents. 
    The process is to divide people into three categories: $E$,
    Such people have a junior high school education or below; $S$class, this kind of person has a high school education; $C $class,
    Such people are highly educated. When the father or mother (the more educated) is one of these three types, the probability that the children will fall into one of these three types is given below
    
    Yields:
    -------

    edu : a pandas DataFrame object constructed by a markov transfer matrix

    Use :
        For simulation model practice

    Reference:
        ThomsonRen  github https://github.com/ThomsonRen/mathmodels
    """
    data = np.array([[0.7, 0.2, 0.1],
       [0.4, 0.4, 0.2],
       [0.1, 0.2, 0.7]])
    edu = pd.DataFrame(data,index=['工党', '保守党', '自由党'],columns=['工党', '保守党', '自由党'])
    return edu