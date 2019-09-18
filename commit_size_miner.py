'''
Akond Rahman and Kaitlyn Cottrel 
Sep 18, 2019 
This file gets commit sizes 
'''
import pandas as pan
import numpy as np 
import subprocess

def getDiff(repo_, hash_):
    mod_files_list = []
   
    cdCommand   = "cd " + repo_ + " ; "
   
    diffCommand = "git diff " + hash_ + "~" + " " + hash_
    command2Run = cdCommand + diffCommand
    try:
      diff_output = subprocess.check_output(["bash", "-c", command2Run])
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



def getCommitSize(df_param):
    ls = []
    hashes = np.unique( df_param['HASH'].tolist() ) 
    for hash_ in hashes: 
        hash_df   = df_param[df_param['HASH']==hash_] 
        repo_name = np.unique(  hash_df['REPO'].tolist() )[0]
        repo_full_path = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/project_repos/' + repo_name
        diff_str , files_modified = getDiff(repo_full_path, hash_)  
        add_loc, del_loc, tot_loc  = getDiffMetrics(diff_str ) 
        # print hash_, repo_name, repo_full_path, add_loc, del_loc, tot_loc
        tup_ = (hash_, repo_name, add_loc, del_loc, tot_loc)
        ls.append(tup_) 
    output_df = pan.DataFrame(ls)
    output_df.to_csv('/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/COMMIT_SIZE_FINAL.csv', header=['HASH','REPO','ADD_LOC', 'DEL_LOC', 'TOT_LOC'], index=False)     


if __name__=='__main__':
   dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/research/Insure/Datasets/UNIQUE_SECU_BUG_MSG.csv' 
   df_ = pan.read_csv(dataset_file) 
   #print df_.head()

   getCommitSize(df_) 

