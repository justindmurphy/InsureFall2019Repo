'''
Akond Rahman 
Sep 25, 2019 
Get RDD Dataset
'''
import pandas as pd 
from datetime import datetime
import time 
import numpy as np 

# def getTravisStartTime(proj_df):

def getDate(single_val): 
    date_str = single_val.split('T')[0]
    date_    = datetime.strptime(date_str, '%Y-%m-%d')
    # print type(date_)   , detetime object 
    return date_ 

def getTravisStartDate(df_pa):
    travis_dict = {}
    projects = np.unique(df_pa['REPO'].tolist()) 
    for proj_ in projects:
        travis_mod_days = df_pa[df_pa['REPO']==proj_]['TRAVIS_MODI_DATE'].tolist() 
        start_date      = min(travis_mod_days) 
        if proj_ not in travis_mod_days:
            travis_dict[proj_] =  start_date
    return travis_dict 


def getBeforeAfterCIDate(travis_dict, df_):
    for proj_name, ci_start_date in travis_dict.iteritems():
        proj_dates = df_[df_['REPO']==proj_name]['DATE'].tolist()
        before_ci_dates = [x_ for x_ in proj_dates if x_ < ci_start_date ] 
        after_ci_dates  = [x_ for x_ in proj_dates if x_ >= ci_start_date ] 
        print ci_start_date
        print 'Before:', before_ci_dates
        print 'After:', after_ci_dates
        print '='*50

if __name__=='__main__':
   travis_ci_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/TRAVIS_START_TIME_DATE.csv'
   travis_ci_df_  = pd.read_csv(travis_ci_file) 

   travis_ci_df_['TRAVIS_MODI_DATE'] = travis_ci_df_['TRAVIS_MODI_TIME'].apply(getDate)
   #print travis_ci_df_.head() 

   proj_travis_date_dict = getTravisStartDate(travis_ci_df_) 

   proj_secu_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/UNIQUE_SECU_COMM.csv' 
   proj_secu_df_  = pd.read_csv(proj_secu_file)  
   proj_secu_df_['DATE'] = proj_secu_df_['TIME'].apply(getDate)
   #print proj_secu_df_
   getBeforeAfterCIDate(proj_travis_date_dict, proj_secu_df_) 


