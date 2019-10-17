'''
Script to download emails 
Akond Rahman 
Oct 17, 2019 
'''

import pandas as pd 
import _pickle as pickle 
import time
import datetime
import os 
import csv 
import numpy as np
import sys
from git import Repo
import  subprocess
import time 
import  datetime 
from collections import Counter

def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def getEligibleProjects(fileNameParam):
  repo_list = []
  with open(fileNameParam, 'rU') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
      repo_list.append(row[-1])
  return repo_list

def getDevEmailForCommit(repo_path_param, hash_):

    cdCommand         = "cd " + repo_path_param + " ; "
    commitCountCmd    = " git log --format='%ae'" + hash_ + "^!"
    command2Run = cdCommand + commitCountCmd

    author_emails = str(subprocess.check_output(['bash','-c', command2Run]))
    author_emails = author_emails.split('\n')
    # print(type(author_emails)) 
    author_emails = [x_.replace(hash_, '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('^', '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('!', '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('\\n', ',') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = author_emails[0].split(',')
    author_emails = [x_ for x_ in author_emails if len(x_) > 3 ] 
    # print(author_emails) 
    author_emails = np.unique(author_emails) 
    return author_emails  

    

def getBranchName(proj_):
    branch_name = ''
    proj_branch = {'biemond@biemond-oradb':'puppet4_3_data', 'derekmolloy@exploringBB':'version2', 'exploringBB':'version2', 
                   'jippi@puppet-php':'php7.0', 'maxchk@puppet-varnish':'develop', 'threetreeslight@my-boxen':'mine', 
                   'puppet':'production', 'deepvariant':'r0.8', 'galaxy':'dev', 'mdanalysis':'develop', 'pyGeno':'bloody',
                   'miso-lims':'develop' , 'jevo':'Float64-optimization'
                  } 
    if proj_ in proj_branch:
        branch_name = proj_branch[proj_]
    else: 
        branch_name = 'master'
    return branch_name


def getDevEmails(projects, csv_file):
    full_list = []
    for proj_ in projects:
        branchName = getBranchName(proj_)     
        repo_dir_absolute_path = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/project_repos/' + proj_ + '/'
        
        print('Started>' + repo_dir_absolute_path + '<') 
        repo_  = Repo(repo_dir_absolute_path)
        all_commits = list(repo_.iter_commits(branchName))   
        for commit_ in all_commits:
            commit_hash = commit_.hexsha
            emails = getDevEmailForCommit(repo_dir_absolute_path, commit_hash)
            full_list = full_list + emails 
            
    emails = np.unique(emails) 
    bug_status_df = pd.DataFrame(full_list) 
    bug_status_df.to_csv(csv_file, header=['EMAIL'], index=False, encoding='utf-8')


if __name__=='__main__':
    t1 = time.time()
    print('Started at:', giveTimeStamp())
    print('*'*100)

    fileName     = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/project_repos/LOCKED_FINAL_JULIA_REPOS.csv'
    elgibleRepos = getEligibleProjects(fileName)

    dev_out_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Insure/Datasets/DEV_EMAILS.csv'
    getDevEmails(elgibleRepos, dev_out_file )

    print('*'*100)
    print('Ended at:', giveTimeStamp())
    print('*'*100)
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print('Duration: {} minutes'.format(time_diff))
    print('*'*100)  