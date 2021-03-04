#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
import argparse
import sys
parser=argparse.ArgumentParser(
    description=''' ''')

__file__ = "add_metadata.py"
__author__ = 'Sandra Godinho Silva (sandragodinhosilva@gmail.com)'
__version__ = '0.1'
__date__ = 'March 2nd, 2021'

parser.add_argument('inputDirectory', 
		help='Full path to the input directory where all files are')

parser.add_argument('metadata')

# Execute parse_args()
args = parser.parse_args()

inputDirectory = sys.argv[0]
metadata = sys.argv[1]
###############################################################################
import os
import pandas as pd

# From the script location, find results directory
script_location = sys.path[0]
out_dir = os.path.dirname(os.path.dirname(script_location))
out_dir = os.path.join(out_dir, "results/Annotation_results")
curdir = out_dir
os.chdir(curdir)

print("Input directory: " + curdir)
entries = list()
for (dirpath, dirnames, filenames) in os.walk(curdir):
    entries += [os.path.join(dirpath, file) for file in filenames]

# list tblout files
anno_files =[]
for filename in entries:
    if "counts" in filename or "PA" in filename:
        anno_files.append(filename)

metadata = pd.read_csv(os.path.join(script_location, "data/metadata.csv"),
                       names =["Genome","Metadata_field"], index_col=None)

for file in anno_files:
    filename = os.path.basename(file)
    name = filename.replace(".csv", "") + "_metadata.csv"
    df = pd.read_csv(file)
    df = df.set_index("index").T
    merge = pd.merge(df,metadata, how="left", left_index=True,right_on="Genome")
    print(merge.head(3))
    merge.to_csv(name, index=False)



