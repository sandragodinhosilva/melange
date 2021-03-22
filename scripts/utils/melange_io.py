import os
from sklearn.metrics import roc_auc_score, matthews_corrcoef, precision_score, recall_score, f1_score
import configparser as cp
import numpy as np
import json
import re

def get_config():
    config = cp.ConfigParser()
    config.read('config.py')
    return config

def save_params(param_dict, path):
    with open(path + "/model_paramters.json", 'w') as f:
        json_out = json.dumps(param_dict, sort_keys=True, indent=4)
        json_out2 = re.sub(r'": \[\s+', '": [', json_out)
        json_out3 = re.sub(r',\s+', ', ', json_out2)
        json_out4 = re.sub(r'\s+\]', ']', json_out3)
        json_out5 = re.sub(r'\s\}, ', '},\n    ', json_out4)
        json_out6 = re.sub(r'\{\}, ', '{},\n    ', json_out5)
        json_out7 = re.sub(r'\], ', '],\n        ', json_out6)
        json_out8 = re.sub(', "', ',\n        "' , json_out7)
        f.write(json_out8)

def load_params(path):
    with open(path + "/model_paramters.json", 'r') as f:
        param_str = f.read()
    param_dict = json.loads(param_str)
    return(param_dict)

    


def get_stat_dict(y, probs, pred):

    config = get_config()
    y = np.array(y)
    y_oh = np.eye(len(np.unique(y)))[np.array(y).reshape(-1)]
    probs = np.array(probs)

    num_class = probs.shape[1]
    stat_dict = {}
         
    if num_class == 2:
        stat_dict["AUC"] = roc_auc_score(y, probs[:,1], average='weighted')
    else:

        stat_dict["AUC"] = roc_auc_score(y_oh, probs, average='weighted')        
    stat_dict["MCC"] = matthews_corrcoef(y, pred.reshape(-1))
    stat_dict["Precision"] = precision_score(y, pred, average='weighted')
    stat_dict["Recall"] = recall_score(y, pred, average='weighted')
    stat_dict["F1"] = f1_score(y, pred, average='weighted')
    
    
    return stat_dict
