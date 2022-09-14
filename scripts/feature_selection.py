#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Goal: join selected annotations                  
#### Usage: python orf_annotation.py /path/to/directory_wt_all_files/ [databases_in_use]
#### Note: full path needed                                    
###############################################################################
import os
import re
import argparse
import sys

parser=argparse.ArgumentParser(
    description='''Join KO, Pfam, COG, Merops, CAZymes annotations in one table.''')

__file__ = "orf_annotation.py"
__author__ = 'Sandra Godinho Silva (sandragodinhosilva@gmail.com)'
__version__ = '0.1'
__date__ = 'September 13th, 2022'

parser.add_argument('inputDirectory', 
		help='Full path to the input directory where all files are')

#parser.add_argument('databases_in_use', metavar='N', type=str, nargs='+',
#                    help='Databases from which we want to have annotation')

# Execute parse_args()
#args = parser.parse_args()
###############################################################################
# import standard Python modules

import pandas as pd
import numpy as np
###############################################################################
#import pygraphviz
import os
import traceback


import sys
import weka.core.jvm as jvm
import weka.core.packages as packages
from weka.core.classes import complete_classname

jvm.start(packages=True)

pkg = "DMNBtext"

# install package if necessary
if not packages.is_installed(pkg):
    print("Installing %s..." % pkg)
    packages.install_package(pkg)
    print("Installed %s, please re-run script!" % pkg)
    jvm.stop()
    sys.exit(0)

# testing classname completion
print(complete_classname(".J48"))
print(complete_classname(".DMNBtext"))





import python-weka-wrapper3
import weka.core.jvm as jvm
from weka.core.classes import Random
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.classifiers import Classifier, Evaluation
from weka.filters import Filter
from weka.core.converters import Loader

jvm.start()
###############################################################################
from itertools import *
import pandas as pd
import os
###############################################################################
# From the script location, find databases directory
script_location = sys.path[0]
#script_location = "/home/sandra/MeLanGE/scripts"
#out_dir = os.path.dirname(os.path.dirname(script_location))
out_dir = os.path.dirname(script_location)

###############################################################################
### Load the dataset
from weka.core.converters import Loader

def LoadDataset(file, i):
    print("Loading dataset")
    loader = Loader(classname="weka.core.converters.CSVLoader")
    data_file = file
    data = loader.load_file(data_file)

    print('Num instances: ', data.num_instances)
    print('Num attributes: ', data.num_attributes)
  
    name_dataset = str(file).split(".")[0]
    print(name_dataset)

    #name dataset
    df_evolution["Dataset"].iloc[i]=name_dataset
    df_evolution["Initial number instances"].iloc[i]=data.num_instances
    df_evolution["Initial number attributes"].iloc[i]=data.num_attributes

    return data, name_dataset
### Preprocessing
from weka.filters import Filter

def FirstPreprocessing(data, i, att_class):
    print("")
    print("Attribute to use as class: " + str(att_class))
    print("Preprocess number 1")

    df_evolution["Class"].iloc[i]=att_class 
    
    l = ["genome","index", "Family", "Bin_Id", "Unnamed: 0", "Genus", "orfs","Genome_ID", "Genomes", "Genome", "Assembly", "Assembly accession", "Origin"]

    for x in l:
    #Remove attribute by name
        remove = Filter(classname="weka.filters.unsupervised.attribute.RemoveByName", options=["-E",str(x)])
        remove.inputformat(data)     # let the filter know about the type of data to filter
        data = remove.filter(data)  # filter the data

    last_column = data.num_attributes
    
    print('Sample instances: ', data.num_instances)
    print('Sample attributes: ', data.num_attributes)
    
    df_evolution["After pre-processing nr instances"].iloc[i]=data.num_instances
    df_evolution["After pre-processing nr attributes"].iloc[i]=data.num_attributes
  
    return data
### Choose class: Genus
def SelectClass(data):
    print("")
    print("Defining last attribute as class")
    last_column = data.num_attributes
    #We choose to classify on the nominal atrribute Genus. We first split our dataset to train and test, with a 80% to the train split.
    #print('Classifying on: ', data.instance(last_column - 1)
    data.class_index = last_column - 1
    return data
### Feature selection
def LoaderSubsetEval(data, i, name_dataset, class_):
    file = "AfterFS/" + name_dataset + "_" + class_ +"_after_SubsetEval.csv"
    if file in os.listdir():
        print("Loading output from SubsetEval to save time: " + str(file))
        from weka.core.converters import Loader
        loader = Loader(classname="weka.core.converters.CSVLoader")
        data_file = file
        data = loader.load_file(data_file)

        print('Sample size: ', data.num_instances)
        print('Sample size: ', data.num_attributes)

        last_column = data.num_attributes
        data.class_index = last_column - 1
        print('Classifying on: ', data.attribute(last_column - 1))

        df_evolution["After CfsSubsetEval nr instances"].iloc[i]=data.num_instances
        df_evolution["After CfsSubsetEval nr attributes"].iloc[i]=data.num_attributes
  
    else: 
        data = AttributeSelectionSubsetEval(data, i, name_dataset, class_)

    return data
def AttributeSelectionSubsetEval(data, i, name_dataset, class_):
    """
    evaluator: CfsSubsetEval
    Evaluates the worth of a subset of attributes by considering the individual predictive ability of each feature along with the degree of redundancy between them.
    Subsets of features that are highly correlated with the class while having low intercorrelation are preferred.

    search: BestFirst
    """  
    print("")
    print("Attribute Selection by CfsSubsetEval")
    from weka.filters import Filter
    remove = Filter(classname="weka.filters.supervised.attribute.AttributeSelection", options=["-E","weka.attributeSelection.CfsSubsetEval -P 1 -E 1", 
                                                                                             "-S", "weka.attributeSelection.BestFirst -D 1 -N 5"])
    remove.inputformat(data)
    filtered = remove.filter(data)
    print('Sample size: ', filtered.num_instances)
    print('Sample size: ', filtered.num_attributes)
    data = filtered

    output= "AfterFS/" + name_dataset + "_" + class_ +"_after_SubsetEval.csv"
    # Save filtered dataset into csv file - backup
    from weka.core.converters import Saver
    saver = Saver(classname="weka.core.converters.CSVSaver")
    saver.save_file(data, output)

    df_evolution["After CfsSubsetEval nr instances"].iloc[i]=data.num_instances
    df_evolution["After CfsSubsetEval nr attributes"].iloc[i]=data.num_attributes

    last_column = data.num_attributes
    #We choose to classify on the nominal atrribute Genus. We first split our dataset to train and test, with a 80% to the train split.
    print('Classifying on: ', data.attribute(last_column - 1))
    data.class_index = last_column - 1

    return data
def GetOptimal(i):
    print("Getting parameters from Feature_selection_correct.csv")
    optimal = {}
    optimal["Optimal threshold"] = int(right["Optimal threshold"].iloc[i])
    optimal["Optimal nr features"] = int(right["Optimal nr features"].iloc[i])
    print("Threshold: " + str(optimal["Optimal threshold"]))
    print("Nr features: " + str(optimal["Optimal nr features"]))
    return optimal
def AttributeSelectionInfoGain(data, threshold):
    """
    evaluator: InfoGainAttributeEval
    Evaluates the worth of an attribute by measuring the information gain with respect to the class.
    InfoGain(Class,Attribute) = H(Class) - H(Class | Attribute).
  
    search: Ranker
    """
    print("Attribute Selection by InfoGain. Threshold: " +str(threshold))
    from weka.filters import Filter
    remove = Filter(classname="weka.filters.supervised.attribute.AttributeSelection",\
                         options=["-S", "weka.attributeSelection.Ranker -T {} -N -1".format(str(threshold)), #T: threshold 
                                  "-E", "weka.attributeSelection.InfoGainAttributeEval"])
    remove.inputformat(data)
    filtered = remove.filter(data)
    
    print('Sample size: ', filtered.num_instances)
    print('Sample size: ', filtered.num_attributes)
    n_att = filtered.num_attributes
  
    return filtered, n_att
### Classifier - Random Forest
def Classifier(data, nfeatures):
    #set Train and Test data
    from weka.filters import Filter
    remove = Filter(classname="weka.filters.supervised.instance.Resample",\
                         options=["-B", "0.0", "-S", "1", "-Z", "80", "-no-replacement"])
    remove.inputformat(data)
    train = remove.filter(data)
    print('Train size: ', train.num_instances)
    print('Train size: ', train.num_attributes)
    remove = Filter(classname="weka.filters.supervised.instance.Resample",\
                         options=["-B", "0.0", "-S", "1", "-Z", "80", "-no-replacement", "-V"])
    remove.inputformat(data)
    test = remove.filter(data)
    print('Test size: ', test.num_instances)
    print('Test size: ', test.num_attributes)
    
    from weka.classifiers import Classifier, Evaluation, PredictionOutput
    #Train the classifier
    cls = Classifier(classname="weka.classifiers.trees.RandomForest", options=["-P","100","-attribute-importance","-K",str(nfeatures)])
    cls.build_classifier(train)

    # Evaluating the classifier
    # cross-validation
    evlCV = Evaluation(train)
    try:
        evlCV.crossvalidate_model(cls, train, 10, Random(1))#, output=pred_output)
    except:
        evlCV.crossvalidate_model(cls, train, 2, Random(1))#, output=pred_output)
    print(evlCV.summary(title="cross-validation"))
    #print(pout.buffer_content())

    # evaluate the built model on the test set
    evlTest = Evaluation(test)
    evlTest.test_model(cls, test)
    print(evlTest.summary(title="test"))

    return evlTest, evlCV

### Select better threshold and number of features
def SelectionOptimalParam(data, i, class_):
    """
    -K <number of attributes> \
    # Number of attributes to randomly investigate. (default 0) 
    """
    print("")
    print("Selecting best parameters")
  
    threshold_list = [0.0, 0.10, 0.20, 0.30, 0.40,0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.96, 0.97, 0.98, 0.99]
    nr_features_list = [1, 3, 5, 7, 9, 11, 13]

    threshold_eval = {}
    feature_eval = {}
    feature_eval_backupf_measure = {}
    d = {}
    d2 = {}
    d3_f = {}
    optimal = {}

    for t in threshold_list:
        print("")
        print("Threshold: " + str(t))
        data_AS, n_att = AttributeSelectionInfoGain(data, t)
        feature_eval = {}
        d2[t] = []
        d2[t].append(n_att)
        d3_f[t] = []
        d3_f[t].append(n_att)
        
    for f in nr_features_list:
        print("Number of features: " + str(f))
        evl, evlCV = Classifier(data_AS, f)
        last_column = data_AS.num_attributes
        feature_eval[f] = evl.percent_correct 
        feature_eval_backupf_measure[f] = evlCV.weighted_f_measure
        print("Accuracy: " + str(evl.percent_correct))
        print("Weighted recall: " + str(evl.weighted_recall))
        print("F-measure: " + str(evlCV.weighted_f_measure))
        d2[t].append(feature_eval[f]) #accuracy of test
        d3_f[t].append(feature_eval_backupf_measure[f]) #f-measure of cross-validation
    #best_feature_nr = str(max(feature_eval, key=feature_eval.get)) # accuracy as metric
    best_feature_nr = str(max(feature_eval_backupf_measure, key=feature_eval_backupf_measure.get)) #f-masure as metric
    d[t] = best_feature_nr
    threshold_eval[t] = str(feature_eval[int(best_feature_nr)])
    #print("Number features with better results for threshold " + str(t) + ": " + best_feature_nr +" with " + str(threshold_eval[t]) + " F-measure.")
    #print("-----------------------")

    print("Conclusions: ")
    
    better_threshold = str(max(threshold_eval, key=threshold_eval.get))
    optimal["Optimal threshold"] = better_threshold
    optimal["Optimal nr features"] = d[float(better_threshold)]
    
    print("Threshold with better results: " + better_threshold + " with " + str(threshold_eval[float(better_threshold)]) +" F-measure " + "for " + d[float(better_threshold)] + " number of features.")
  
    df_evolution["Optimal threshold"].iloc[i]=better_threshold
    df_evolution["Optimal nr features"].iloc[i]=d[float(better_threshold)]

    return d2, d3_f, optimal

def PlotOptimalParam(d2, att_class):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    df = pd.DataFrame.from_dict(d2, orient='index', columns=["Nr_attributes",'1','3','5', '7', '9', '11', '13'])

    df2 = df.drop(columns=["Nr_attributes"])
    df2= df2.T.max()

    df3 = df["Nr_attributes"]
    d3 = df3.T

    #https://matplotlib.org/gallery/api/two_scales.html

    fig, ax1 = plt.subplots(figsize=(8,5))
    title=  "Feature Selection - Evaluation on test dataset from " + name_dataset+ "_" + att_class
    ax1.set_title(title)
    ax1.set_xlabel("InfoGain Threshold")

    color = 'tab:red'
    ax1.plot(df2, color=color)
    ax1.set_ylabel('Accuracy', color=color)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.plot(df3, color=color)
    ax2.set_ylabel("Number of attributes", color=color)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y')

    fig.tight_layout() 
    output_file = name_dataset + "_" + att_class + "_accuracy_best_metrics.png"
    #plt.savefig(output_file, bbox_inches = 'tight')  # osandragodinhosilva@gmail.comtherwise the right y-label is slightly clipped
    plt.show()
def PlotOptimalParamFMeasure(d3_f, att_class):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    df = pd.DataFrame.from_dict(d3_f, orient='index', columns=["Nr_attributes",'1','3', '5', '7', '9', '11', '13'])
  
  #df.to_csv("COG_selector_function_output.csv")
  #df =pd.read_csv("COG_selector_function_output.csv")
  #df.set_index("Unnamed: 0",inplace=True)

    df2 = df.drop(columns=["Nr_attributes"])
    df2= df2.T.max()

    df3 = df["Nr_attributes"]
    d3 = df3.T

  #https://matplotlib.org/gallery/api/two_scales.html

    fig, ax1 = plt.subplots(figsize=(8,5))
    title=  "Feature Selection - Cross-validation on train dataset from " + name_dataset + "_" + att_class
    ax1.set_title(title)
    ax1.set_xlabel("InfoGain Threshold")

    color = 'tab:red'
    ax1.plot(df2, color=color)
    ax1.set_ylabel('F-measure', color=color)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.plot(df3, color=color)
    ax2.set_ylabel("Number of attributes", color=color)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y')

    fig.tight_layout() 
    output_file = name_dataset + "_" + att_class + "_f_measure_best_metrics.png"
    #plt.savefig(output_file, bbox_inches = 'tight')  # otherwise the right y-label is slightly clipped
    plt.show()
    
def ImplementFeatureSelection(data, optimal, i):
    from weka.classifiers import Classifier, Evaluation, PredictionOutput
    from weka.filters import Filter
    print("")
    print("Implementing best parameters: Feature Selection")
  #CfsSubsetEval
  # Implement Feature Selection
    data, n_att = AttributeSelectionInfoGain(data, optimal['Optimal threshold'])

  #set Train and Test data
    remove = Filter(classname="weka.filters.supervised.instance.Resample",\
                         options=["-B", "0.0", "-S", "1", "-Z", "80", "-no-replacement"])
    remove.inputformat(data)
    train = remove.filter(data)
    print('Train size: ', train.num_instances)
    print('Train size: ', train.num_attributes)
  
    remove = Filter(classname="weka.filters.supervised.instance.Resample",\
                         options=["-B", "0.0", "-S", "1", "-Z", "80", "-no-replacement", "-V"])
    remove.inputformat(data)
    test = remove.filter(data)
    print('Test size: ', test.num_instances)
    print('Test size: ', test.num_attributes)

  #Train the classifier
    cls = Classifier(classname="weka.classifiers.trees.RandomForest", options=["-P","100","-attribute-importance","-K",str(optimal["Optimal nr features"])])
    cls.build_classifier(train)
    pred_output = PredictionOutput(classname="weka.classifiers.evaluation.output.prediction.PlainText", options=["-distribution"])# outputfile])

  # Evaluating the classifier
  # cross-validation
    evlCV = Evaluation(train)
    try:
        evlCV.crossvalidate_model(cls, train, 10, Random(1), output=pred_output)
    except:
        evlCV.crossvalidate_model(cls, train, 2, Random(1), output=pred_output)
    print(evlCV.summary(title="cross-validation"))

  # evaluate the built model on the test set
    evlTest = Evaluation(test)
    evlTest.test_model(cls, test)
    print(evlTest.summary(title="test"))

  #Save in evolution dataframe
    df_evolution["After InfoGainAttributeEval nr instances"].iloc[i] = data.num_instances
    df_evolution["After InfoGainAttributeEval nr attributes"].iloc[i] = data.num_attributes

    df_evolution["Training cross-validation (f-measure)"].iloc[i] = evlCV.weighted_f_measure
    df_evolution["Training cross-validation (accuracy)"].iloc[i] =  evlCV.percent_correct

    df_evolution["Evaluation (f-measure)"].iloc[i] = evlTest.weighted_f_measure
    df_evolution["Evaluation (accuracy)"].iloc[i] = evlTest.percent_correct
  
  #Save attributes selected
    l_att = []
    for x in data.attributes():
        a = str(x).split(" ")[1]
        l_att.append(a)

    df_evolution["Selected attributes"].iloc[i]=  l_att
  #print("weightedPrecision: " + str(evaluation.weighted_precision))
  #print("weightedRecall: " + str(evaluation.weighted_recall))
  
    return data, evlTest, cls, pred_output

# pred_output - Predictions
# cls # Classifier output (if attribute importance is on, also this)

### Save Final dataset
def SaveFinaldf(data, name_dataset, att_class ):
    """
    Save filtered dataset into csv file 
    """
    from weka.core.converters import Saver

    output = "AfterFS/" + name_dataset + "_" + att_class + "_FS.csv"

    saver = Saver(classname="weka.core.converters.CSVSaver")
    saver.save_file(data, output)
    print("Save dataset after Filter Selection as " + str(output))

# Implementation

###############################################################################
print("Starting... ")

outDirectory = sys.argv[1]
curdir = outDirectory
os.chdir(curdir)

print("Input directory: " + curdir)

###############################################################################
#Step 2: Create output directory and list files

output_dir = os.path.join(out_dir,"results/Feature_selection")

try:
    os.mkdir(output_dir)
except:
    pass
print("Output folder: " + output_dir)
###############################################################################
entries = list()
for (dirpath, dirnames, filenames) in os.walk(curdir):
    entries += [os.path.join(dirpath, file) for file in filenames]
    
import sys
script_location = sys.path[0]
home = os.path.dirname(os.path.dirname(script_location))
home

metadata = pd.read_csv(os.path.join(home, snakemake.input["ind"]), header=None)
metadata.columns = ["Genome", "metadata"]
metadata = metadata.set_index("Genome")
metadata.head()    

new_directory = os.path.join(inputdir2, "AfterFS")
if "AfterFS" not in os.listdir():
    os.makedirs(new_directory)


for file in os.listdir():
    if "Statistics" not in file and "metadata" not in file and "Orfs_per_genome" not in file \
        and "evolution" not in file and "FS" not in file and "Feature_selection" not in file \
        and "description" not in file and "after_SubsetEval" not in file:
        print(file)
        name = file.split(".")[0]
        print(name)
        final = name + "_metadata.csv"
        if final not in file:
            df = pd.read_csv(file)
            df = df.set_index("index").T
            df = pd.merge(df, metadata, how="left", left_index=True, right_index=True)
            df = df.rename_axis("genome")
            df.to_csv(name + "_metadata.csv")