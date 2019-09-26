'''
Akond Rahman 
Sep 25, 2019 
Get RDD Dataset
'''
from datetime import timedelta
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


def getHashesForDate(proj_, day_list, full_df ):
    hash_list = []
    proj_df =  full_df[full_df['REPO']==proj_]
    for day_ in day_list:
        hash_ = proj_df[proj_df['DATE']==day_]['HASH'].tolist()[0]
        hash_list.append(hash_)
    return hash_list 



def getBeforeAfterCIDate(travis_dict, df_, days_cutoff=60):
    proj_hash_dict = {}
    for proj_name, ci_start_date in travis_dict.iteritems():
        proj_dates = df_[df_['REPO']==proj_name]['DATE'].tolist()
        before_ci_dates = [x_ for x_ in proj_dates if x_ <= ci_start_date ] 
        after_ci_dates  = [x_ for x_ in proj_dates if x_ > ci_start_date ] 
        # print ci_start_date
        days_before_ci, days_after_ci= len(before_ci_dates), len(after_ci_dates)
        if (days_before_ci >= days_cutoff) and (days_after_ci >= days_cutoff) :
            sorted_days_before  = sorted(before_ci_dates, reverse=True)
            sorted_days_before  = sorted(sorted_days_before)
            sorted_days_after   = sorted(after_ci_dates)

            before_topk_days    = sorted_days_before[0:days_cutoff] 
            after_topk_days     = sorted_days_after[0:days_cutoff] 
            # print 'Before:', before_topk_days
            # print 'After:',  after_topk_days 
            before_topk_hashes  = getHashesForDate(proj_name, before_topk_days, df_)
            after_topk_hashes   = getHashesForDate(proj_name, after_topk_days, df_)
            # print 'Before:', before_topk_hashes
            # print 'After:',  after_topk_hashes
            # print '='*25
            if proj_name not in proj_hash_dict:
                proj_hash_dict[proj_name] = (before_topk_hashes, after_topk_hashes) 

    print '*'*50
    print 'Day cutoff :', days_cutoff
    print 'Projects existing:', len(proj_hash_dict)
    return proj_hash_dict 

def getValuesForHash(repo_, hash_, comm_df, bug_df_, secu_df_):
    repo_df    = comm_df[comm_df['REPO']==repo_]
    commit_add = repo_df[repo_df['HASH']==hash_]['ADD_LOC'].tolist()[0]
    commit_del = repo_df[repo_df['HASH']==hash_]['DEL_LOC'].tolist()[0]
    commit_tot = repo_df[repo_df['HASH']==hash_]['TOT_LOC'].tolist()[0]    

    commit_bug = bug_df_[bug_df_['HASH']==hash_]['FINAL_RATING'].tolist()[0]    
    commit_sec = secu_df_[secu_df_['HASH']==hash_]['SECU_FLAG'].tolist()[0]    

    return commit_add, commit_del, commit_tot, commit_bug, commit_sec 

def getDevCountForProj(dev_df_, proj_name_):
    return len( np.unique( dev_df_[dev_df_['REPO']==proj_name_]['DEV_IDENTIFIER'].tolist() ) )

def getCommCountForProj(comm_df_, proj_name_):
    return len( np.unique( comm_df_[comm_df_['REPO']==proj_name_]['HASH'].tolist() ) )    

def getDiffDays( e_date, s_date ):
    diff = e_date - s_date
    return  diff.days    

def getCIAdoptionDays(hash_before_list, proj_sec_df, proj_):
    before_date_list = []
    commit_hash_dates =  proj_sec_df[proj_sec_df['REPO']==proj_]['DATE'].tolist() 
    proj_start_date   =  min(commit_hash_dates) 

    for hash_ in hash_before_list:
        before_date_list.append( proj_sec_df[proj_sec_df['HASH']==hash_]['DATE'].tolist()[0] )
    ci_start_date   =  max(before_date_list)  
    diff_days = getDiffDays(ci_start_date, proj_start_date) 

    # print proj_, proj_start_date, ci_start_date, diff_days 
    return diff_days 



def generateDataset(dic_, commit_df, bug_df, secu_df, dev_df, cutoff_days, csv_out_file):
    for k_, v_ in dic_.iteritems(): 
        time_after_intervention, intervention_flag  = 0, 0 
        proj_name = k_ 
        before_hash_list, after_hash_list = v_ 
        age_at_travis           = getCIAdoptionDays(before_hash_list, secu_df, proj_name)
        if age_at_travis > cutoff_days:
            tot_comm_count = len( np.unique( secu_df[secu_df['REPO']==proj_name]['HASH'].tolist() ) )
            dev_count, commit_count = getDevCountForProj(dev_df, proj_name), getCommCountForProj(commit_df, proj_name)
            for hash_val in before_hash_list:
                commi_add, commi_del, commi_tot, commi_bug, commi_sec  = getValuesForHash(proj_name, hash_val, commit_df, bug_df, secu_df) 

            for hash_val in after_hash_list:
                time_after_intervention += 1 
                intervention_flag = 1 
                commi_add, commi_del, commi_tot, commi_bug, commi_sec  = getValuesForHash(proj_name, hash_val, commit_df, bug_df, secu_df) 


if __name__=='__main__':
   days_ = 60 
   travis_ci_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/TRAVIS_START_TIME_DATE.csv'
   travis_ci_df_  = pd.read_csv(travis_ci_file) 

   travis_ci_df_['TRAVIS_MODI_DATE'] = travis_ci_df_['TRAVIS_MODI_TIME'].apply(getDate)
   #print travis_ci_df_.head() 

   proj_travis_date_dict = getTravisStartDate(travis_ci_df_) 

   proj_secu_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/UNIQUE_SECU_COMM.csv' 
   proj_secu_df_  = pd.read_csv(proj_secu_file)  
   proj_secu_df_['DATE'] = proj_secu_df_['TIME'].apply(getDate)
   #print proj_secu_df_
   all_proj_before_after_hash_dict = getBeforeAfterCIDate(proj_travis_date_dict, proj_secu_df_, days_)  

   comm_size_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/COMMIT_SIZE_FINAL.csv' 
   comm_size_df_  = pd.read_csv(comm_size_file)     

   buggy_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/UNIQUE_BUG_COMM.csv' 
   buggy_df_  = pd.read_csv(buggy_file)     

   dev_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/UNIQUE_DEVS.csv' 
   dev_df_  = pd.read_csv(dev_file)     

   rdd_out_file =  '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/RDD_DATASET.csv'
   generateDataset(all_proj_before_after_hash_dict, comm_size_df_, buggy_df_, proj_secu_df_, dev_df_ , days_,  rdd_out_file) 

