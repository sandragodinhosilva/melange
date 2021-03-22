#####################################################################################
# Setings
#####################################################################################

[Evaluation]

# NumberTestSplits	Number of partitions (k) in k-fold cross-validation [integer]
# NumberRuns		Number of iterations to run cross-validation [integer]
# Normalization	Normalization type [Standard or MinMax]
# Dataset		Dataset located in ../data

NumberTestSplits = 5
NumberRuns = 1
Normalization = Standard
DataSet = PRISM_3


#####################################################################################
# Random Forest settings
#####################################################################################

[RF]

# Train		Turn Random Forest models on or off [boolean]
# NumberTrees		Number of trees per forest [integer]
# ValidationModels	Number of partitions (k) to use in cross-validation for selecting number of features [integer]

Train = True
NumberTrees = 500
ValidationModels = 5
