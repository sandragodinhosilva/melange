# Third-party libraries
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from utils.melange_io import get_stat_dict


def train(train, test, config, seed=42):

    number_trees = int(config.get('RF', 'NumberTrees'))
    num_models = int(config.get('RF', 'ValidationModels'))

    x, y = train
    test_x, test_y = test
    
    clf = RandomForestClassifier(n_estimators=number_trees, n_jobs=-1)
    clf.fit(x, y)
    
    feature_importance = clf.feature_importances_

    test_probs = np.array([row for row in clf.predict_proba(test_x)])
    test_pred = np.argmax(test_probs, axis=-1)

    test_stat_dict = get_stat_dict(test_y, test_probs, test_pred)
    

    return clf, test_stat_dict, feature_importance
