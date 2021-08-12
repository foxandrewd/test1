"""
Created on: Thursday May 27, 2021
@author: Andrew Fox
"""

import os, yaml
import pandas as pd
import numpy as np
import random as rnd
import datetime as dt
import re
from pandas.api.types import is_numeric_dtype


base_folder = 'C:/Users/Barbf/Downloads/cmanwx'
output_folder = 'C:/Users/Barbf/OneDrive/Documents/andy/ANZ/proj8/data'
MAX_FILES_TO_RUN = 1

# Zero'th month doesn't exist:
C_MonthLength = [0,31,28,31,30,31,30,31,31,30,31,30,31]

RUN_YR_START = '1973'
RUN_YR_END   = '2020'

RUN_MONTH_START = '01'
RUN_MONTH_END = '12'

BASIS_YEAR = RUN_YR_END
BASIS_MONTH = RUN_MONTH_END
ALL_MONTHS = [str(m).zfill(2) for m in range(int(RUN_MONTH_START),int(RUN_MONTH_END)+1)]
ALL_YEARS = [ str(y) for y in range(int(RUN_YR_START), int(RUN_YR_END)+1) ] 


def main():
    _,_,files = next(os.walk('/'.join([base_folder, BASIS_YEAR, BASIS_MONTH, 'csv'])))
    for fname in files[:MAX_FILES_TO_RUN]:
        run_analysis(fname)

            
def run_analysis(fname):
    
    yr = BASIS_YEAR
    mon = BASIS_MONTH
    df = pd.read_csv( '/'.join([base_folder,yr, mon, 'csv', fname]), index_col=0)
    
    buoyname = fname_to_buoyname(fname)
    
    try: df.drop('c11_k.1', axis=1, inplace=True)
    except KeyError: pass
        
    df_next = pd.DataFrame(columns = df.columns)
    
    for year in ALL_YEARS:        
        for month in ALL_MONTHS:
            buoy_fnames = get_buoy_fnames(year, month)

            try:
                curr_fname = buoy_fnames[buoyname]
            except KeyError:
                continue
            try:
                df_x = pd.read_csv('/'.join([base_folder,year,month,'csv',curr_fname]), index_col=0)
            except:
                fname_adjusted = buoyname + '_' + year + month + '.csv.'
                try: df_x = pd.read_csv( '/'.join([base_folder,year,month,'csv',fname_adjusted]), index_col=0)
                except: continue

            try: df_x.drop('c11_k.1', axis=1, inplace=True)
            except KeyError: pass
            
            df_x['datetime.1'] = pd.to_datetime(df_x['datetime.1'])
            
            
            # Fix Kelvin temp's: make them into Celsius
            for col in df_x.columns:
                if 'temperature' in col and is_numeric_dtype(df_x[col].dtype):
                    #try:   # Try to convert Kelvin to Celsius:
                    df_x[col][df_x[col] >= 1e20] = np.nan
                    if df_x[col].mean() > 160:
                        df_x[col] = df_x[col] - 273.15
                    #except: pass
            
            wanted = (df_x['datetime.1'].dt.time > dt.time(12,49)) & \
                     (df_x['datetime.1'].dt.time < dt.time(12,51))
            df_wanted = df_x.loc[ wanted ]
                    
            df_next = df_next.append(df_wanted)
            
    df_final = df_next    # Capture the last df_next as the final dataframe
    
    # post-processing for-loop:
    for col in df_final:
        try: df_final[col] = df_final[col].astype('float64')
        except: pass
        
        if 'float' in str(df_final[col].dtype) and is_integer_column(df_final[col]):
            try: df_final[col] = df_final[col].fillna(-32767).astype('int64')
            except ValueError: pass
        
        if df_final[col].dtype in ('int64','float64'):
            df_final[col][df_final[col] >= 1e24] = np.nan
            df_final[col][df_final[col] <= -1e6] = np.nan
        if 'int' in str(df_final[col].dtype):
            df_final[col][df_final[col] == -32767] = np.nan
        
    #end post-processing for-loop    
    
    buoyname = fname_to_buoyname(fname)
    df_final.index.name = buoyname
    dates = list(df_final['datetime.1'])
    #'''
    print( 'mindate: ', min(dates) )
    print( 'maxdate: ', max(dates ))
    print( 'buoyname: ', buoyname )
    print()
    print(df_final.dtypes)
    #'''
    df_final.to_csv(output_folder+'/'+ buoyname + '.csv')


def get_buoy_fnames(year, month):
    look_in_dir = '/'.join([base_folder, year, month, 'csv'])
    _,_,files = next(os.walk( look_in_dir ))
    buoy_fnames = {}
    for fname in files:
        if '_adcp_' in fname: continue   # these '_adcp_' files have almost no data
        buoy = fname_to_buoyname(fname)
        if buoy not in buoy_fnames:
            buoy_fnames[buoy] = fname  # Keep buoy's 1st file, ignore it's 2nd, 3rd,..
        else: continue
        
    return buoy_fnames

def is_integer_column(col):
    for num in list(col):
        if not num.is_integer():   # Find a non-integer, should return False
            return False
    return True                    # All were integers so should return True

def fname_to_buoyname(fname):
    
    if fname.startswith('sim_'):    # Remove 'sim_' if at the start of fname
        fname = fname[4:]
    
    if fname.startswith('NDBC_'):
        newname = fname[5:]         # Remove 'NDBC_' from the start of the name
    else:
        newname = fname
    uscore = newname.index('_')
    buoyname = newname[:uscore]
    return buoyname
    

def make_index():
    pass


if __name__ == "__main__":
    main()