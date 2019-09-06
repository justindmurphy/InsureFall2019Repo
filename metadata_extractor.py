import subprocess 
from git import Repo
from datetime import datetime
import os 
import csv 
import requests
import json
import pandas as pd 
import shutil 

def getOutputLines(file_name):
    file_lines = []
    with open(file_name, 'rU') as fil:
         file_str = fil.read()
         file_lines = file_str.split('\n')
    return file_lines


def getCreationDateField(str_list):
    val_to_ret = 0
    line = [ s_ for s_ in str_list if '"created_at":' in s_]
    if (len(line) > 0 ):
        if ':' in line[0]:
            val_to_ret =  line[0].split('"')[3].split('T')[0].strip()
    return str(val_to_ret)

def getMetaDataField(field_, str_list):
    val_to_ret = 0
    line = [ s_ for s_ in str_list if field_ in s_]
    if (len(line) > 0 ):
        if ':' in line[0]:
            val_to_ret =  line[0].split(':')[-1].split(',')[0].strip()
            if val_to_ret == 'false':
               val_to_ret = 0 
            if val_to_ret == 'true':
               val_to_ret = 1        
            # print 'asi mama:', val_to_ret
    return str(val_to_ret)

def getMetaData(json_dir_name):
    str_ = ''
    for root_, dirnames, filenames in os.walk(json_dir_name):
        for file_ in filenames:
            if (file_.endswith('json')):
               names = file_.split('$')
               if len(names) > 1: 
                 repo_name = names[0] + '/' + names[1]
                 dir_name = names[1]
                 full_p_file = os.path.join(root_, file_)
                 if (os.path.exists(full_p_file)):
                    the_lines=getOutputLines(full_p_file)
                    fork_data    = getMetaDataField('"fork":', the_lines)
                    watcher_data = getMetaDataField('"watchers":', the_lines)
                    stars_data   = getMetaDataField('"stargazers_count":', the_lines)
                    lang_data    = getMetaDataField('"language":', the_lines)
                    start_ts     = getCreationDateField( the_lines)
                    start_data   = start_ts.split('T')[0]
                    the_str      = repo_name + ',' + dir_name + ',' + fork_data + ',' + watcher_data + ',' + stars_data + ',' + start_data + ',' + lang_data  + '\n'
                    # print the_str
                    str_ = str_ + the_str
    str_ = 'repo,dir,fork,watcher,star,start_date,language' + '\n'  + str_
    return str_

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def cloneRepo(repo_name):
    cmd_ = "git clone " + repo_name
    try:
       subprocess.check_output(['bash','-c', cmd_])    
    except subprocess.CalledProcessError:
       print 'Skipping this repo ... trouble cloning repo', repo_name 


def getGitCommitCount(repo_name):
    proj_name  = repo_name.split('/')[-1]
    branchName = getBranchName(proj_name) 
    repo_  = Repo(repo_name)
    all_commits = list(repo_.iter_commits(branchName))
    return all_commits     

def getBranchName(proj_):
    branch_name = ''
    proj_branch = {'biemond@biemond-oradb':'puppet4_3_data', 'derekmolloy@exploringBB':'version2', 'exploringBB':'version2', 
                   'jippi@puppet-php':'php7.0', 'maxchk@puppet-varnish':'develop', 'threetreeslight@my-boxen':'mine', 
                   'puppet':'production', 'jevo':'Float64-optimization' 
                  } 
    if proj_ in proj_branch:
        branch_name = proj_branch[proj_]
    else:
        branch_name = 'master'
    return branch_name


def getGitCommitCount(repo_name):
    branchName = getBranchName(repo_name) 
    repo_  = Repo(repo_name)
    all_commits = list(repo_.iter_commits(branchName))
    return len(all_commits)

def days_between(d1_, d2_): 
    return abs((d2_ - d1_).days)

def getMunMeasure(file_name):
    str_map = ''
    df_ = pd.read_csv(file_name)
    repo_names = df_['repo'].tolist()
    valid  = 0 
    for repo_ in repo_names:
        start_date     = df_[df_['repo']==repo_]['start_date'].tolist()[0]
        clone_url      = 'https://github.com/' + repo_.replace('.json', '')
        print clone_url
        dirName        = clone_url.split('/')[-1]
        print dirName
        cloneRepo(clone_url)
        comm_cnt       = getGitCommitCount(dirName)
        start_datetime = datetime(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]), 12, 30)
        print start_datetime
        print comm_cnt
        ds_life_days   = days_between(start_datetime, datetime(2019, 9, 1, 12, 30))
        ds_life_months = round(float(ds_life_days)/float(30), 5)
        mun_metric     = float(comm_cnt) / float(ds_life_months)
        print mun_metric
        if mun_metric < 2.0 :
            print 'Deleting ', repo_
            try:
               if os.path.exists(dirName):
                  shutil.rmtree(dirName)
            except OSError:
               print 'Failed deleting, will try manually'
        else:
            valid += 1
            str_map = str_map + clone_url + ',' + dirName + '\n'
        print '*'*50
    print 'Total valid repos: {}. All of them are cloned.'.format(valid)
    print str_map




if __name__=='__main__':
   # dir_ = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_metadata/'
   # metadata_str = getMetaData(dir_)
   # dumpContentIntoFile(metadata_str, '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_metadata/JULIA_PROJS_METADATA.csv')

   filtered_list_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/filtered_projects.csv'
   getMunMeasure(filtered_list_file)