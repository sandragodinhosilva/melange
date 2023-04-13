#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Goal: 
#### Usage: 
#### Note: 
###############################################################################

import sys

__file__ = "benchmark_parser.py"
__author__ = "Sandra Godinho Silva (sandragodinhosilva@gmail.com)"
__version__ = "1"
__date__ = "November 8th, 2022"



import argparse
import sys

parser = argparse.ArgumentParser(
    description="""Benchmark"""
)

__file__ = "benchmarker_parser.py"
__author__ = "Sandra Godinho Silva (sandragodinhosilva@gmail.com)"
__version__ = "2"
__date__ = "April 13th, 2023"

parser.add_argument(
    "outputDirectory", help="Path to the output annotation directory"
)

# Execute parse_args()
args = parser.parse_args()

###############################################################################
# import standard Python modules
import os
import pandas as pd

###############################################################################
print("Starting... ")

# From the script location, find benchmarks directory
# From the script location, find benchmarks directory
script_location = sys.path[0]
base_dir = os.path.dirname(script_location)
base_base_dir = os.path.dirname(base_dir)
benchmarks_path = os.path.join(base_base_dir, "benchmarks")

print("Benchmark directory: " + str(benchmarks_path))
print(" ")

# Output directory 
output_dir = os.path.abspath(sys.argv[1])

print("Output directory: " + output_dir)
print(" ")

###############################################################################
os.chdir(benchmarks_path)

files = os.listdir() 
file_list = list() 

for file in os.listdir():
    if file.endswith(".txt"):
        name = os.path.basename(file)
        name = os.path.splitext(name)[0]
        tool = name.split("_")[0]
        genome = name.split("_",1)[1].replace(".benchmark", "")
        if file.endswith(".txt"):
            df=pd.read_csv(file,sep="\t")
#           df['filename'] = file
            df['tool'] = tool
            df['genome'] = genome
            file_list.append(df) 
    all_files = pd.concat(file_list, axis=0, ignore_index=True) 
 

all_files.to_csv(os.path.join(output_dir, "benchmark_results.csv"), index=False)
    
#all_files.to_csv(os.path.join(output_dir, "benchmark_results.csv"))
print("Table benchmark_results.csv was created.")
    
###############################################################################
# END
