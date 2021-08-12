# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 22:34:59 2021

@author: Barbf
"""

from netCDF4 import Dataset
import sys, os
import pandas as pd
import numpy as np
import random as rnd
import warnings
import yaml
from collections import OrderedDict, defaultdict
warnings.filterwarnings("ignore")
import datetime as dt
import shutil

data_folder = "C:/Users/Barbf/Downloads/cmanwx"

in_csv_folder = 'C:/Users/Barbf/Downloads/csv'

C_years = [str(yr) for yr in range(2011,2021 + 1)]
C_months = [str(m).zfill(2) for m in range(1,12 + 1)]



def main():
        
    (_,dirs,files) = next(os.walk(in_csv_folder))
    
    for fname in files:
        try:
            yearmonth1 = fname[fname.index("_20")+1:]
        except ValueError:
            continue
        try:
            yearmonth = yearmonth1[ : yearmonth1.index('_D')]
            yr = yearmonth[:4]
            mo = yearmonth[4:]
            year_int = int(yr)
            
            if 2011 <= year_int <= 2021:
            
                shutil.copy2(in_csv_folder+'/'+fname,
                         data_folder+'/'+yr+'/'+mo+'/'+'csv'+'/'+fname)
                print(fname)
                #return             
            
        except ValueError:
            continue
        
 
       




def doYear(year):
    
    yearFolder = data_folder+'/'+year
    
    os.makedirs(yearFolder, exist_ok=True)
    
    #(_,yeardirs,yearfiles) = next(os.walk(yearFolder))
    
    
    for month in C_months:
        monthFolder = yearFolder+'/'+month
        os.makedirs(monthFolder+'/csv', exist_ok=True)




#for yr in C_years:
#    doYear(yr)


if __name__ == "__main__":
    # run main function:
    main()
