'''
Akond Rahman
Oct 10, 2019 
Data for SWAN 2018 CI Analysis 
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

def getValuesForHash(repo_, hash_, comm_df, bug_df_, secu_df_):
    bug_cnt, sec_cnt, mer_cnt  = 0 , 0 , 0
    repo_df    = comm_df[comm_df['REPO']==repo_]
    commit_add = repo_df[repo_df['HASH']==hash_]['ADD_LOC'].tolist()[0]
    commit_del = repo_df[repo_df['HASH']==hash_]['DEL_LOC'].tolist()[0]
    commit_tot = repo_df[repo_df['HASH']==hash_]['TOT_LOC'].tolist()[0]    

    commit_bug = bug_df_[bug_df_['HASH']==hash_]['FINAL_RATING'].tolist()[0]    
    if commit_bug=='BUGGY':
        bug_cnt = 1 
    commit_sec = secu_df_[secu_df_['HASH']==hash_]['SECU_FLAG'].tolist()[0]    
    if commit_sec=='INSECURE':
        sec_cnt = 1     
    commit_merge = bug_df_[bug_df_['HASH']==hash_]['MERGE_FLAG'].tolist()[0]    
    if commit_merge=='MERGED':
        mer_cnt = 1 

    return commit_add, commit_del, commit_tot, bug_cnt, sec_cnt , mer_cnt

def getBeforeAfterCIDate(travis_dict, df_, days_cutoff=60):
    proj_hash_dict = {}
    for proj_name, ci_start_date in travis_dict.items():
        proj_dates = df_[df_['REPO']==proj_name]['DATE'].tolist()
        before_ci_dates = [x_ for x_ in proj_dates if x_ <= ci_start_date ] 
        after_ci_dates  = [x_ for x_ in proj_dates if x_ > ci_start_date ] 
        days_before_ci, days_after_ci= len(before_ci_dates), len(after_ci_dates)
        if (days_before_ci >= days_cutoff) and (days_after_ci >= days_cutoff) :
            before_hashes  = getHashesForDate(proj_name, before_ci_dates,  df_)
            after_hashes   = getHashesForDate(proj_name, after_ci_dates, df_)       
            proj_hash_dict[proj_name] = (before_hashes, after_hashes) 
    return proj_hash_dict    

def generateBoxplotData(proj_dict, comm_df, bug_df, secu_df, csv_out_file): 
    all_data_list = []
    for k_, v_ in proj_dict.items():
        before_hashes, after_hashes = v_ 
        for hash_ in before_hashes:
            commi_add, commi_del, commi_tot, commi_bug, commi_sec, commi_merge = getValuesForHash(k_, hash_, comm_df, bug_df, secu_df) 
            data_tuple = (k_ , commi_add, commi_del, commi_tot, commi_bug, commi_sec,  commi_merge, 'BEFORE')
            all_data_list.append(data_tuple)
    
        for hash_ in after_hashes:
            commi_add, commi_del, commi_tot, commi_bug, commi_sec, commi_merge = getValuesForHash(k_, hash_, comm_df, bug_df, secu_df) 
            data_tuple = (k_ , commi_add, commi_del, commi_tot, commi_bug, commi_sec,  commi_merge, 'AFTER')
            all_data_list.append(data_tuple)

    full_df = pd.DataFrame(all_data_list) 
    # print full_df.head() 		
    full_df.to_csv(csv_out_file, header=['REPO', 'ADD_LOC', 'DEL_LOC', 'COMMIT_SIZE', 'BUG_COUNT', 'SEC_COUNT', 'MERGE_COUNT', 'CI_FLAG' ], index=False, encoding='utf-8')

def getDuration(date_list):
    min_date = min(date_list)
    max_date = max(date_list) 
    dura_days = abs((max_date - min_date).days)
    return dura_days 


def getProjectDuration(df_, out_fil):
    proj_names = np.unique( df_['REPO'].tolist() ) 
    full_list = []
    for project in proj_names:
        proj_df = df_[df_['REPO']==project] 
        proj_dates = proj_df[proj_df['REPO']==project]['DATE'].tolist() 
        dura_days = getDuration(proj_dates) 
        data_tuple = (project, dura_days)
        full_list.append(data_tuple) 
    data_df = pd.DataFrame(full_list) 
    data_df.to_csv(out_fil, header=['PROJECT', 'DURATION_DAYS'] , index=False, encoding='utf-8')


def getHotSoSResults():
    all_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/ALL_SECU_COMM.csv'
    rdd_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/FULL_RDD_DATASET_FINAL_30DAYS.csv'
    all_df   = pd.read_csv(all_file) 
    rdd_df   = pd.read_csv(rdd_file) 

    rdd_repos   = np.unique( rdd_df['REPO'].tolist()  )
    rdd_all_commits, rdd_all_neutral, rdd_all_insecure = [], [], [] 
    dump_list = []
    for repo_ in rdd_repos:
        repo_df = all_df[all_df['REPO']==repo_]
        repo_rdd_commits  = np.unique( repo_df['HASH'].tolist()  )
        repo_rdd_insecure = np.unique( repo_df[repo_df['SECU_FLAG']=='INSECURE']['HASH'].tolist()  )
        repo_rdd_neutral  = np.unique( repo_df[repo_df['SECU_FLAG']=='NEUTRAL']['HASH'].tolist()  ) 
        for x_ in repo_rdd_commits:
            rdd_all_commits.append(x_) 
        for x_ in repo_rdd_insecure:
            rdd_all_insecure.append(x_) 
        for x_ in repo_rdd_neutral:
            rdd_all_neutral.append(x_) 
        for hash_ in repo_rdd_commits:
            hash_df   = repo_df[repo_df['HASH']==hash_]
            secu_flag = hash_df['SECU_FLAG'].tolist()[0]
            tuple_    = (repo_, hash_, secu_flag) 
            dump_list.append(tuple_)
    df_ = pd.DataFrame(dump_list)
    df_.to_csv('HOTSOS2020_SCI_SOFT_SECU.csv', header=['REPO', 'HASH' , 'LABEL'] , index=False, encoding='utf-8')    

    print('='*100)
    print('REPO_COUNT:{}, SECU_PER_REPO:{}'.format(len(rdd_repos), float(len(rdd_all_insecure))/float( len(rdd_repos) ) ))
    print('='*100)
    print('COMMIT_COUNT:{}, INSECURE:{}, PROPORTION:{}'.format(len(rdd_all_commits), len(rdd_all_insecure) , float(len(rdd_all_insecure))/float( len(rdd_all_commits) ) ))
    print('='*100)    
    print('COMMIT_COUNT:{}, REPO_COUNT:{}, COMMIT_PER_REPO:{}'.format(len(rdd_all_commits), len(rdd_repos), float(len(rdd_all_commits))/float( len(rdd_repos) ) ))
    print('='*100)    


if __name__=='__main__':
   days_ = 30 
   travis_ci_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/TRAVIS_START_TIME_DATE.csv'
   travis_ci_df_  = pd.read_csv(travis_ci_file, encoding = 'utf-8') 

   travis_ci_df_['TRAVIS_MODI_DATE'] = travis_ci_df_['TRAVIS_MODI_TIME'].apply(getDate)
   #print travis_ci_df_.head() 

   proj_travis_date_dict = getTravisStartDate(travis_ci_df_) 

   proj_secu_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/UNIQUE_SECU_COMM_ELYAS.csv'    
   proj_secu_df_  = pd.read_csv(proj_secu_file, encoding = 'utf-8')  
   proj_secu_df_['DATE'] = proj_secu_df_['TIME'].apply(getDate)
   #print proj_secu_df_
   #all_proj_before_after_hash_dict = getBeforeAfterCIDate(proj_travis_date_dict, proj_secu_df_, days_)  

   comm_size_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/COMMIT_SIZE_FINAL.csv' 
   comm_size_df_  = pd.read_csv(comm_size_file, encoding = 'utf-8')     

   buggy_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/UNIQUE_BUG_COMM.csv' 
   buggy_df_  = pd.read_csv(buggy_file, encoding = 'utf-8')     

   output_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/FULL_MEDIAN_DATASET.csv' 
   #generateBoxplotData(all_proj_before_after_hash_dict, comm_size_df_, buggy_df_, proj_secu_df_, output_file)  

   proj_dura_output_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/PROJ_DURA_DATASET.csv'
   #getProjectDuration(proj_secu_df_, proj_dura_output_file) 


   '''
   HotSoS 2020 Work 
   '''
   getHotSoSResults() 

