'''
Akond Rahman 
Sep 04, 2019 : Wednesday  
Script to mine first date and time for .travis.yml 
'''

import pandas as pd 
import cPickle as pickle
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


secu_kws = [ 'race', 'racy', 'buffer', 'overflow', 'stack', 'integer', 'signedness', 'widthness', 'underflow',
             'improper', 'unauthenticated', 'gain access', 'permission', 'cross site', 'CSS', 'XSS', 'denial service', 
             'DOS', 'crash', 'deadlock', 'SQL', 'SQLI', 'injection', 'format', 'string', 'printf', 'scanf', 
             'cross site', 'request forgery', 'CSRF', 'XSRF', 'forged', 
             'security', 'vulnerability', 'vulnerable', 'hole', 'exploit', 'attack', 'bypass', 'backdoor', 
             'threat', 'expose', 'breach', 'violate', 'fatal', 'blacklist', 'overrun', 'insecure'
           ]

prem_bug_kw_list      = ['error', 'bug', 'fix', 'issue', 'mistake', 'incorrect', 'fault', 'defect', 'flaw', 'solve' ]

def checkIfTravisDiff(repo_, hash_):
    fl = False 
    cdCommand   = "cd " + repo_ + " ; "
   
    diffCommand = "git diff " + hash_ + "~" + " " + hash_
    command2Run = cdCommand + diffCommand
    try:
      diff_output = subprocess.check_output(["bash", "-c", command2Run])
    except subprocess.CalledProcessError as e_:
      diff_output = "NOT_FOUND" 

    splitted_lines = diff_output.split('\n')
    add_files      = [x_.split(' ')[-1] for x_ in splitted_lines if '---' in x_ ]
    del_files      = [x_.split(' ')[-1] for x_ in splitted_lines if '+++' in x_ ]
    # print mod_files
    add_travis_files   = [x_ for x_ in add_files if 'travis' in x_] 
    del_travis_files   = [x_ for x_ in del_files if 'travis' in x_] 
    # print add_travis_files, del_travis_files
    if len(add_travis_files) > 0  or len(del_travis_files):
        fl = True 
    
    return fl 

def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def extractTravisCommits(repo, branchName):
  str_dump =  ''
  full_list = []
  repo_dir_absolute_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_repos/' + repo + '/'
  print 'Started>' + repo_dir_absolute_path + '<' 
  repo_  = Repo(repo_dir_absolute_path)
  all_commits = list(repo_.iter_commits(branchName))

  for commit_ in all_commits: 
    commit_hash = commit_.hexsha
    timestamp_commit = commit_.committed_datetime
    str_time_commit  = timestamp_commit.strftime('%Y-%m-%dT%H-%M-%S') ## date with time 
    travisFlag       = checkIfTravisDiff(repo_dir_absolute_path, commit_hash) 

    if travisFlag:
       tup_ = (repo, commit_hash, str_time_commit) 
       full_list.append(tup_) 
  print 'Finished>' + repo_dir_absolute_path + '<'
  return full_list


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

def dumpBugStatus(projects, csv_file):
    sec_kws_lower = [x_.lower() for x_ in secu_kws]
    bug_kws_lower = [x_.lower() for x_ in prem_bug_kw_list ]

    full_list = []
    for proj_ in projects:
        sec_cnt, bug_cnt = 0, 0 
        bug_flag, secu_flag = 'NEUTRAL', 'NEUTRAL'
        branchName = getBranchName(proj_)     
        repo_dir_absolute_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_repos/' + proj_ + '/'
        print 'Started>' + repo_dir_absolute_path + '<' 
        repo_  = Repo(repo_dir_absolute_path)
        all_commits = list(repo_.iter_commits(branchName))   
        for commit_ in all_commits: 
            commit_hash = commit_.hexsha
            
            msg_commit =  commit_.message         
            msg_commit = msg_commit.replace('\n', ' ')
            msg_commit = msg_commit.replace(',',  ';')    
            msg_commit = msg_commit.replace('\t', ' ')
            msg_commit = msg_commit.replace('&',  ';')  
            msg_commit = msg_commit.replace('#',  ' ')
            msg_commit = msg_commit.replace('=',  ' ')      
            msg_commit = msg_commit.lower()    
            for sec_kw in sec_kws_lower:
              if sec_kw in msg_commit:
                  secu_flag  = 'INSECURE'
                  sec_cnt += 1  
            for bug_kw in bug_kws_lower:
              if bug_kw in msg_commit:
                  bug_flag  = 'BUGGY'
                  bug_cnt += 1         
            tup_ = (proj_, commit_hash, secu_flag, bug_flag)     
            full_list.append(tup_)
        print 'Bugs:{}, Security bugs:{}, All:{}'.format( bug_cnt, sec_cnt, len(all_commits) ) 
        print '='*50                            

    bug_status_df = pd.DataFrame(full_list) 
    bug_status_df.to_csv(csv_file, header=['REPO','HASH','SECU_FLAG', 'BUG_FLAG'], index=False, encoding='utf-8')

def checkIfPrior(curr, other):

  d_curr  = datetime.datetime.strptime(curr,  '%Y-%m-%dT%H-%M-%S').date()
  d_other = datetime.datetime.strptime(other, '%Y-%m-%dT%H-%M-%S').date()
  # print d_curr, d_other
  return d_curr > d_other

def getEligibleProjects(fileNameParam):
  repo_list = []
  with open(fileNameParam, 'rU') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
      repo_list.append(row[-1])
  return repo_list


if __name__=='__main__':

    t1 = time.time()
    print 'Started at:', giveTimeStamp()
    print '*'*100

    travis_out_csv_fil  = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/ALL_SECU_COMM.csv'
    bug_status_csv_fil  = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/ALL_BUG_STATUS.csv'

    fileName      = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/LOCKED_FINAL_JULIA_REPOS.csv'
    elgibleRepos  =  getEligibleProjects(fileName)

    secu_dict, diff_dict = {}, {}    
    full_list = []

    # for proj_ in elgibleRepos:
    #     branchName = getBranchName(proj_) 
    #     commit_travis_list = extractTravisCommits(proj_, branchName)
    #     secu_dict[proj_]   = commit_travis_list
    #     full_list          = full_list + commit_travis_list
    
    # all_proj_df = pd.DataFrame(full_list) 
    # all_proj_df.to_csv(travis_out_csv_fil, header=['REPO','HASH','TRAVIS_MODI_TIME'], index=False, encoding='utf-8') 

    dumpBugStatus(elgibleRepos, bug_status_csv_fil)

    print '*'*100
    print 'Ended at:', giveTimeStamp()
    print '*'*100
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print "Duration: {} minutes".format(time_diff)
    print '*'*100  

        
