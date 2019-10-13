'''
'''
import pandas as pd 
import os 
import numpy as np 
import time
import datetime
from sklearn.feature_extraction.text import  TfidfVectorizer
import cPickle as pickle 
from sklearn import decomposition
from sklearn.decomposition import TruncatedSVD
import sklearn_models

def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def parseFileName(file_list):
    final_str = ''
    for file_ in file_list:
            file_ = file_.replace('_', '')
            if ('.' in file_ ):
                val = file_.split('.')[0]
                if (val.isdigit() == False ):
                   final_str = final_str + ' ' + val 
            elif '/' in file_:
                final_str = final_str + ' ' + file_ 
    return final_str
    
def performPCA(allFeatures, pca_comp=1000, explained_var=True):
    pca_xform_comp_dict = {1:1, 4:3, 5:4, 10:4, 20:5, 30:5, 40:5, 50:5}
    selected_features = None
    pcaObj = decomposition.PCA(n_components=pca_comp)

    if explained_var:
        pcaObj.fit(allFeatures)
        variance_of_features = pcaObj.explained_variance_
        variance_ratio_of_features = pcaObj.explained_variance_ratio_
        totalvarExplained = float(0)        
        for index_ in xrange(len(variance_ratio_of_features)):
            var_exp_ = variance_ratio_of_features[index_]
            totalvarExplained = totalvarExplained + var_exp_
            print "Prin. comp#{}, explained variance:{}, total explained variance:{}".format(index_+1, var_exp_, totalvarExplained)
    else: 
        pcaObj.n_components = pca_xform_comp_dict[pca_comp]
        selected_features   = pcaObj.fit_transform(allFeatures)
        print "Dimension of PCA feature set size:", np.shape(selected_features)
        print "-"*50
    return selected_features


def prepareForTFIDF(df_):
    cnt_ = 0 
    hashes = np.unique(df_['HASH'].tolist()) 
    print "{} hashes to go through".format(len(hashes))
    mod_file_list, all_labels = [], []
    for commit_hash in hashes:
        tx = time.time()
        per_commit_df = df_[df_['HASH']==commit_hash]
        per_commit_mod_files = per_commit_df['MODIFIED_FILE'].tolist()
        per_commit_final_files = parseFileName(per_commit_mod_files)  
        mod_file_list.append(per_commit_final_files) 
        ty = time.time()
        time_diff = round( (ty - tx ) / 60, 5) 
        cnt_ += 1 
        secu_label = list(np.unique( per_commit_df['SECU_FLAG'].tolist() ))[0]
        if secu_label=='INSCURE':
            label = 1
        else: 
            label = 0 
        all_labels.append( label ) 
        if (cnt_%10000) == 0 :
           print cnt_ 
           print "Duration: {} minutes for one hash".format(time_diff)
    return mod_file_list , all_labels  

def printMatrix(feature_names, result, cnt):
    tfidfScores  = zip(feature_names, np.asarray(result.sum(axis=0)).ravel())
    sortedScores = sorted(tfidfScores, key=lambda x_: x_[1], reverse=True)
    for feature in sortedScores:
        print "{0:25} Score: {1} NormScore: {2}".format(feature[0], feature[1], float(feature[1])/float(cnt))  #:25 means 25 spaces after the first string 


def filterTFIDF(result, topK = 5):
    tfidfDict = {} 
    r_, c_ = result.shape 
    result_mat = result.todense()
    for r_col in xrange(r_):
        tfidf_vals = result[r_col, :] ## this is per row values 
        tfidf_val_array = list(tfidf_vals.toarray()[0])

        tfidf_np_array        = np.array(tfidf_val_array) 
        top_k_indices         = np.argsort(tfidf_np_array)[-topK:]
        top_k_tfidf_scores    = tfidf_np_array[top_k_indices]

        if r_col not in tfidfDict: 
            tfidfDict[r_col] = (list(top_k_tfidf_scores), list(top_k_indices)) 
        if (r_col%999==0):
           print r_col, top_k_tfidf_scores, top_k_indices 
           print '_'*25
    return tfidfDict 

def performTFIDF(mod_files_list, pkl_file_name): 
    # mod_files_list is a list of  strings, each string corresponds to files modified in a  commit  
    commitCnt           = len(mod_files_list) 
    tfidfVectorizer     = TfidfVectorizer(min_df=1)
    transformedFeatures = tfidfVectorizer.fit_transform(mod_files_list)
    pickle.dump( transformedFeatures, open( pkl_file_name , 'wb')) 
    featureNames        = tfidfVectorizer.get_feature_names()
    tfidf_features      = pickle.load(open(pkl_file_name, 'rb')) 
    xformed_features    = tfidf_features.toarray() 
    # performPCA(xformed_features, featureNames) 

    
    # printMatrix(featureNames, transformedFeatures, commitCnt) 

def giveOnlyLabels(df_):
    cnt_ = 0 
    hashes = np.unique(df_['HASH'].tolist()) 
    print "{} hashes to go through".format(len(hashes))
    all_labels = []
    for commit_hash in hashes:
        cnt_ += 1 
        per_commit_df = df_[df_['HASH']==commit_hash]
        secu_label = list(np.unique( per_commit_df['SECU_FLAG'].tolist() ))[0]
        if secu_label=='INSCURE':
            label = 1
        else: 
            label = 0 
        all_labels.append( label ) 
        if cnt_%1000 == 0:
            print 'Processed:', cnt_
    return  all_labels  

if __name__=='__main__':
    t1 = time.time()
    print 'Started at:', giveTimeStamp()
    print '*'*100

    csc4220data  = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/teaching/ProjectMaterials/LOCKED_FINAL_CSC4220_5220_DATASET.csv'
    full_dataset = pd.read_csv(csc4220data) 
    # print 'Before filtering:', full_dataset.shape
    # print '*'*50 
    # dataset_with_valid_files = full_dataset[full_dataset['MODIFIED_FILE'].str.contains('/|.', na=False)]
    # dataset_with_valid_files = dataset_with_valid_files[~dataset_with_valid_files['MODIFIED_FILE'].str.contains('---', na=False)]
    # dataset_with_valid_files = dataset_with_valid_files[~dataset_with_valid_files['MODIFIED_FILE'].str.contains('-', na=False)]
    # dataset_with_valid_files = dataset_with_valid_files[~dataset_with_valid_files['MODIFIED_FILE'].str.isdigit()]
    # # #print dataset_with_valid_files.head()
    # print 'After filtering:', dataset_with_valid_files.shape   

    dataframe_for_prediction = full_dataset.drop_duplicates(['HASH'], keep='last')
    dataframe_for_prediction = dataframe_for_prediction.drop(['HASH', 'MODIFIED_FILE', 'REPO', 'TIME', 'DEV_EXP', 'DEV_RECENT', 'SECU_FLAG'], axis=1)
    print dataframe_for_prediction.head()
    numpy_dataframe_pred = dataframe_for_prediction.as_matrix()
    print numpy_dataframe_pred 
    print type(numpy_dataframe_pred)


    # get the giant TFIDF pickle 
    # tfidf_list_full , labels_full = prepareForTFIDF(dataset_with_valid_files)   
    # print '*'*50 
    # performTFIDF(tfidf_list_full, 'FULL_TFIDF.PKL')  
    # print '*'*100
    # ###get full TFIDF matrix 
    # full_tfidf_matrix = pickle.load(open('FULL_TFIDF.PKL', 'rb'))
    # ###filter IFIDF , take top K tokens based on TFIDF scores : 1, 5, 10, 20, 30, 50
    top_k = 1
    # ###
    # filteredTFIDFDict= filterTFIDF(full_tfidf_matrix, top_k) 
    # pickle.dump(filteredTFIDFDict, open('FILTERED_TFIDF.PKL', 'wb')) 
    # pkl_dict_file = 'TOP'+ str(top_k) +'_FILTERED_TFIDF.PKL'
    # filtered_tfidf_dict = pickle.load(open(pkl_dict_file, 'rb')) 
    # pca_list = []
    # for k_, v_ in filtered_tfidf_dict.iteritems():
    #     tfidf_scores = v_[0] 
    #     tfidf_scores = [round(z_, 2) for z_ in tfidf_scores ]
    #     pca_list.append(tfidf_scores) # get TFIDF scores 
    # pca_array = np.array(pca_list) 
    # pca_mod_features =  performPCA(pca_array, top_k, False)   
    pca_mod_features = performPCA(numpy_dataframe_pred, 4, False )
    label_list = full_dataset.drop_duplicates(['HASH'], keep='last')['SECU_FLAG'].tolist() 
    dep_var_list = []
    for flag in label_list:
        if flag == 'INSECURE':
            dep_var_list.append(1)
        else: 
            dep_var_list.append(0)
    dep_var_list = np.array(dep_var_list) 
    print 'Labels:', len(dep_var_list)
    print 'Starting model building ...'
    iterDumpDir_       = '/Users/akond/Documents/AkondOneDrive/OneDrive/JobPrep-TNTU2019/teaching/ProjectMaterials/output/'
    sklearn_models.performIterativeModeling(pca_mod_features, dep_var_list, 10, 10, iterDumpDir_)


    print 'Ended at:', giveTimeStamp()
    print '*'*100
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print "Duration: {} minutes".format(time_diff)
    print '*'*100     
