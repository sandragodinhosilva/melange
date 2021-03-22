import sys
import os
import warnings
from os.path import abspath
import configparser as cp

import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold

import models.rf as rf

from utils.melange_io import get_config, save_params, load_params, get_stat_dict
from utils.permanova_test import get_permanova_ranked_list

if __name__ == "__main__":

    #####################################################################
    # Input Config File definitions
    #####################################################################

    config = get_config()
    #dataset = config.get('Evaluation', 'DataSet')
    script_location = sys.path[0]
    input_dir = os.path.dirname(script_location)
    dataset = os.path.join(input_dir, "FeatureSelection/abundance.csv")
    labels = os.path.join(input_dir, "FeatureSelection/labels.tsv")
    
    num_runs = 1 #int(config.get('Evaluation', 'NumberRuns'))
    num_test = 2 #int(config.get('Evaluation', 'NumberTestSplits'))
    train_rf = True #config.get('RF', 'Train')

    #########################################################################
    # Set models to use
    #########################################################################
    to_train = []

    if train_rf == True:
        to_train.append("RF")

    #########################################################################
    # Set up DataFrames to store results
    #########################################################################

    cross_validation_list = ["Run_" + str(x) + "_CV_" + str(y) for x in range(num_runs) for y in range(num_test)]

    auc_df = pd.DataFrame(index=to_train, columns=cross_validation_list)
    mcc_df = pd.DataFrame(index=to_train, columns=cross_validation_list)
    precision_df = pd.DataFrame(index=to_train, columns=cross_validation_list)
    recall_df = pd.DataFrame(index=to_train, columns=cross_validation_list)
    f1_df = pd.DataFrame(index=to_train, columns=cross_validation_list)

    #########################################################################
    # Create results dir
    #########################################################################
    result_path = "../results/"
    #result_path = "../results/" + dataset
    print("Saving results to %s" % (result_path))
    try:
        os.mkdir("../results/")
    except OSError:
        pass

    param_tune = True
    #########################################################################
    # Read in data and generate tree maps
    #########################################################################
    print("\nStarting MeLanGE on %s..." % (dataset))

    abundance = pd.read_csv(dataset, index_col=0, header=None)
    labels = pd.read_csv(labels, index_col=0, header=None)
    
    labels_data, label_set = pd.factorize(labels.index.values)    
    num_class = len(np.unique(labels_data))
    full_features = abundance.index
    #permanova_df = get_permanova_ranked_list(abundance, labels_data, full_features, label_set)
        
    col_sums = abundance.sum(axis=0)
    abundance = abundance.divide(col_sums, axis=1)
    num_pos = (abundance != 0).astype(int).sum(axis=1)
        
    #abundance = abundance.drop(num_pos.loc[num_pos.values < float(filt_thresh_count) * abundance.values.shape[1]].index)
    #abundance = abundance.loc[abundance.mean(1) > float(filt_thresh_mean)]        
    features = abundance.index.values


    labels.to_csv(result_path + "/labels.txt", header=None)
    print("There are %d classes...%s" % (num_class, ", ".join(label_set)))
        
    #permanova_df.to_csv(result_path + "/PERMANOVA_rankings.csv")
        
    np.savetxt(result_path + "/label_set.txt", label_set, fmt="%s")
    #abundance.to_csv(result_path + "/abundance.tsv", sep="\t")

    #abundance = abundance.transpose().values        
    labels = labels_data

    #########################################################################
    # Set up seeds for different runs
    #########################################################################
    rf_scores = pd.DataFrame(index=features)
        
    seeds = np.random.randint(1000, size=num_runs)
    run = 0

    for seed in seeds:

    #####################################################################
    # Set up CV partitioning
    #####################################################################

        print("Starting cross-valudation")
        skf = StratifiedKFold(n_splits=num_test, shuffle=True, random_state=seed)
        fold = 0

    #####################################################################
    # Begin k-fold CV
    #####################################################################
        for train_index, test_index in skf.split(abundance, labels):

        #################################################################
        # Select and format training and testing sets
        #################################################################
                train_x, test_x = abundance[train_index,:], abundance[test_index,:]

