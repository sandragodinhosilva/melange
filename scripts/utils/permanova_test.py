from skbio.stats.distance import permanova, DistanceMatrix
from sklearn.metrics import pairwise_distances
from statsmodels.stats.multitest import multipletests
import numpy as np
import pandas as pd

def get_permanova_ranked_list(x, y, feature_list, label_set):
    x = x.transpose().values
    
    values = []
    for f in range(len(feature_list)):
        sub_x = x[:,f]
        dist = pairwise_distances(sub_x.reshape(-1,1), sub_x.reshape(-1,1), metric="cityblock")
        dist = DistanceMatrix(data=dist)
        perm = permanova(dist, y)
        values.append(perm.loc["p-value"])
    
    fdr_values = multipletests(values, method="fdr_bh")[1]
    permanova_df = pd.DataFrame(index=feature_list, data={"p-value":np.array(values).reshape(-1), "Adj p-value": np.array(fdr_values).reshape(-1)})
    return permanova_df
