'''
Akond Rahman 
Aug 28, 2019 : Wednesday  
Script to mine commits from scientific software repos 
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

def getDevsOfRepo(repo_path_param):
    commit_dict       = {}
    author_dict       = {}

    cdCommand         = "cd " + repo_path_param + " ; "
    commitCountCmd    = " git log --pretty=format:'%H_%an' "
    command2Run = cdCommand + commitCountCmd

    commit_count_output = subprocess.check_output(['bash','-c', command2Run])
    author_count_output = commit_count_output.split('\n')
    for commit_auth in author_count_output:
       commit_ = commit_auth.split('_')[0]
       
       author_ = commit_auth.split('_')[1]
       author_ = author_.replace(' ', '')
       # only one author for one commit 
       if commit_ not in commit_dict:
           commit_dict[commit_] = author_ 
       # one author can be involved with multiple commits 
       if author_ not in author_dict:
           author_dict[author_] = [commit_] 
       else:            
           author_dict[author_] = author_dict[author_] + [commit_] 
    return commit_dict, author_dict   

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

def getModFilesInDiff(diff_str):
    splitted_lines = diff_str.split('\n')
    mod_files = [x_.split('a')[-1] for x_ in splitted_lines if '---' in x_ ]
    return mod_files

def getDiff(repo_, hash_):
    mod_files_list = []
   
    cdCommand   = "cd " + repo_ + " ; "
   
    diffCommand = "git diff " + hash_ + "~" + " " + hash_
    command2Run = cdCommand + diffCommand
    try:
      diff_output = subprocess.check_output(["bash", "-c", command2Run])
      mod_files_list =  getModFilesInDiff(diff_output)
    except subprocess.CalledProcessError as e_:
      diff_output = "NOT_FOUND" 
    return diff_output, mod_files_list

def getDiffLOC(diff_text):
    add_cnt, del_cnt = 0, 0 
    diff_text_list = diff_text.split('\n') 
    diff_text_list = [x_ for x_ in diff_text_list if (('---' not in x_) and ('+++' not in x_)) ]
    add_text_list  = [x_ for x_ in diff_text_list if x_.startswith('+')]
    del_text_list  = [x_ for x_ in diff_text_list if x_.startswith('-')]

    # print add_text_list, del_text_list 
    add_cnt, del_cnt = len(add_text_list), len(del_text_list)
    return add_cnt, del_cnt 

def getDiffMetrics(diff_param):
    loc_add, loc_del = getDiffLOC(diff_param) 
    loc_tot          = loc_add + loc_del 
    return loc_add, loc_del, loc_tot 

def preProcess(txt_, replace_char): 

    txt_ = txt_.replace('\n', replace_char)
    txt_ = txt_.replace('\r', replace_char)
    txt_ = txt_.replace(',',  replace_char)    
    txt_ = txt_.replace('\t', replace_char)
    txt_ = txt_.replace('&',  replace_char)  
    txt_ = txt_.replace('#',  replace_char)
    txt_ = txt_.replace('=',  replace_char)  
    txt_ = txt_.replace('-',  replace_char)  
    txt_ = txt_.lower()

    return txt_ 

def extractCommits(repo, branchName):
  str_dump = ''
  full_list, diff_list  = [], []
  repo_dir_absolute_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_repos/' + repo + '/'
  print 'Started>' + repo_dir_absolute_path + '<' 
  repo_  = Repo(repo_dir_absolute_path)
  all_commits = list(repo_.iter_commits(branchName))
  commit_dict, author_dict = getDevsOfRepo(repo_dir_absolute_path) 
  sec_cnt = 0 
  dev_name = 'UNKNOWN'
  for commit_ in all_commits: 
    secu_flag  = 'NEUTRAL'
    merge_flag = 'NEUTRAL' 
    msg_commit =  commit_.message 

    msg_commit = preProcess(msg_commit, ' ')  
    msg_commit = msg_commit.lower()

    commit_hash = commit_.hexsha

    timestamp_commit = commit_.committed_datetime
    str_time_commit  = timestamp_commit.strftime('%Y-%m-%dT%H-%M-%S') ## date with time 

    sec_kws_lower = [x_.lower() for x_ in secu_kws]
    commit_dff, mod_files_list   = getDiff(repo_dir_absolute_path, commit_hash) 
    add_loc, del_loc, tot_loc = getDiffMetrics(commit_dff)
    dev_name = commit_dict[commit_hash]     

    for sec_kw in sec_kws_lower:
      if sec_kw in msg_commit:
          secu_flag  = 'INSECURE'
          sec_cnt += 1 
          str_dump = str_dump + sec_kw + '\n' + '*'*25  + msg_commit + '\n' + '*'*25 + '\n' + repo_dir_absolute_path + '\n' + '*'*25 + '\n' + commit_hash + '\n' + '*'*25 + '\n' 
    if 'merge' == msg_commit.split(' ')[0]:
      merge_flag = 'MERGE' 
    
    
    for mod_file in mod_files_list:
        mod_file = unicode(mod_file, errors='ignore')
        mod_file = preProcess(mod_file, '')  
        # tup_ = (repo, commit_hash, str_time_commit, add_loc, del_loc, tot_loc, author_exp, author_recent_exp, mod_file, secu_flag) 
        tup_ = (repo, commit_hash, str_time_commit, dev_name, msg_commit , mod_file, merge_flag, secu_flag) 
        full_list.append(tup_) 
    # diff_list.append( (commit_hash, commit_dff) )
  print 'Finished>' + repo_dir_absolute_path + '<insecure commit count------>' + str(sec_cnt)  
  return full_list , diff_list



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
    str_dump = ''
    sec_kws_lower = [x_.lower() for x_ in secu_kws]
    bug_kws_lower = [x_.lower() for x_ in prem_bug_kw_list ]

    full_list = []
    for proj_ in projects:
        sec_cnt, bug_cnt = 0, 0 
        secu_flag = 'NEUTRAL'
        branchName = getBranchName(proj_)     
        repo_dir_absolute_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_repos/' + proj_ + '/'
        print 'Started>' + repo_dir_absolute_path + '<' 
        repo_  = Repo(repo_dir_absolute_path)
        all_commits = list(repo_.iter_commits(branchName))   
        for commit_ in all_commits: 
            commit_hash = commit_.hexsha
            
            msg_commit = commit_.message         
            msg_commit = preProcess(msg_commit, ' ')
            
            commit_dff, mod_files_list   = getDiff(repo_dir_absolute_path, commit_hash) 
            for sec_kw in sec_kws_lower:
              if sec_kw in msg_commit:
                  secu_flag  = 'INSECURE'
                  sec_cnt += 1  
            for bug_kw in bug_kws_lower:
              if bug_kw in msg_commit:
                  bug_flag  = 'BUGGY'
                  bug_cnt += 1         
                  # str_dump = str_dump + bug_kw + '\n' + '*'*25  + msg_commit + '\n' + '*'*25 + '\n' + repo_dir_absolute_path + '\n' + '*'*25 + '\n' + commit_hash + '\n' + '*'*25 + '\n' 
            for mod_file in mod_files_list:
                mod_file = unicode(mod_file, errors='ignore')
                tup_ = (proj_, commit_hash, mod_file, secu_flag, msg_commit, bug_flag)     
                full_list.append(tup_)
        print 'Bugs:{}, Security bugs:{}, All:{}'.format( bug_cnt, sec_cnt, len(all_commits) ) 
        print '='*50                            
        print str_dump
        print '='*50   

    bug_status_df = pd.DataFrame(full_list) 
    bug_status_df.drop_duplicates(subset ="HASH", keep = False, inplace = True) 
    bug_status_df.to_csv(csv_file, header=['REPO','HASH', 'MOD_FIL', 'SECU_FLAG', 'COMMIT_MESSAGE' , 'BUG_FLAG'], index=False, encoding='utf-8')


def getUniqueEntries(inp_fil, out_fil):
  df_        = pd.read_csv(inp_fil) 
  df_.drop_duplicates(subset ="HASH", keep = False, inplace = True) 
  df_.to_csv(out_fil, header=['REPO','HASH','TIME', 'DEV', 'COMMIT_MESSAGE', 'MOD_FILE', 'MERGE_FLAG', 'SECU_FLAG'], index=False, encoding='utf-8')   

if __name__=='__main__':

    t1 = time.time()
    print 'Started at:', giveTimeStamp()
    print '*'*100

    # secu_out_csv_fil  = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/ALL_SECU_COMM.csv'
    bug_status_csv    = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/ALL_BUG_STATUS.csv'

    fileName     = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_repos/LOCKED_FINAL_JULIA_REPOS.csv'
    elgibleRepos = getEligibleProjects(fileName)

    secu_dict, diff_dict = {}, {}    
    full_list = []

    # for proj_ in elgibleRepos:
    #     branchName = getBranchName(proj_) 
    #     commit_secu_list, commit_diff_list = extractCommits(proj_, branchName)
    #     secu_dict[proj_] = commit_secu_list
    #     diff_dict[proj_] = commit_diff_list 
    #     full_list = full_list + commit_secu_list
    
    # all_proj_df = pd.DataFrame(full_list) 
    # # all_proj_df.to_csv(secu_out_csv_fil, header=['REPO','HASH','TIME', 'ADD_LOC', 'DEL_LOC', 'TOT_LOC', 'DEV_EXP', 'DEV_RECENT', 'MODIFIED_FILE', 'SECU_FLAG'], index=False, encoding='utf-8') 
    # all_proj_df.to_csv(secu_out_csv_fil, header=['REPO','HASH','TIME', 'DEV', 'COMMIT_MESSAGE', 'MOD_FILE', 'MERGE_FLAG', 'SECU_FLAG'], index=False, encoding='utf-8') 

    dumpBugStatus(elgibleRepos, bug_status_csv)

    # getUniqueEntries(secu_out_csv_fil, 'UNIQUE_SECU_COMM.csv')

    print '*'*100
    print 'Ended at:', giveTimeStamp()
    print '*'*100
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print "Duration: {} minutes".format(time_diff)
    print '*'*100  