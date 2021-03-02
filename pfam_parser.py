#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Goal: join KO, Pfam, COG and CAZyme annotations                  
#### Usage: python orf_annotation.py /path/to/directory_wt_all_files/ 
#### Note: provide full path!                                          
###############################################################################

import argparse
import sys
parser=argparse.ArgumentParser(
    description='''Join KO, Pfam, COG and CAZyme annotations in one table.''')

__file__ = "pfam_parser.py"
__author__ = 'Sandra Godinho Silva (sandragodinhosilva@gmail.com)'
__version__ = '0.8'
__date__ = 'December 3rd, 2020'

parser.add_argument('inputDirectory', 
		help='Full path to the input directory where all files are')

# Execute parse_args()
args = parser.parse_args()
###############################################################################
# import standard Python modules
import os
import pandas as pd
import re
from collections import Counter
import numpy as np
###############################################################################
print("Starting... ")

script_location = sys.path[0]
inputDirectory = sys.argv[0]
curdir = os.path.join(script_location, "results")
os.chdir(curdir)

print("Input directory: " + curdir)

curdir = os.getcwd()

###############################################################################
#Step 1: parse Pfam files

entries = list()
for (dirpath, dirnames, filenames) in os.walk(curdir):
    entries += [os.path.join(dirpath, file) for file in filenames]

# list tblout files
tblout_files =[]
for filename in entries:
    if "_tblout.txt" in filename:
        tblout_files.append(filename)

d = {}
record_genomes_used = []

## Function is parallelized to increase running time
import multiprocessing as mp

def tblout_annotation(file):        
    path_parent = os.path.dirname(file)
    filename = os.path.basename(file)
    name = filename.replace("_tblout.txt", "")
    record_genomes_used.append(name)
    out = os.path.join(path_parent, name + "_tblout_pfam.txt")
    
    if out not in entries:
        protein2hit_dict = {}
        protein2bit_dict = {}
        dic = {}
        with open(file, 'r') as f:
            i=0
            lines = f.readlines()
            for line in lines:
                line = line.rstrip() # This removes the whitespace at the end of the line
                if line.startswith("#"): # We only want to analyze lines with HMMER matches, so we can pass on all the lines that start with a #
                    pass
                else:
                    newline = re.sub("\s+", "\t", line) # Now we can replace the whitespace in the lines with tabs, which are easier to work with. 
                    tabs = newline.split("\t") # And now we can create a list by splitting each line into pieces based on where the tabs are. 
                    hit = tabs[3]             
                    i +=1
                    query = tabs[0] # The first item in the line is the query protein. We can assign the variable "query" to it. 
                    bit_score = tabs[5] # The fifth item is the bit score. We can assign the variable "bit_score" to it. 
                    dic[i]= query
                    protein2bit_dict[i] = float(bit_score)
                    protein2hit_dict[i] = hit
                with open(out, "w") as outputfile: 
                    outputfile.write("Query\tHit\tScore\n")
                    for proteins in protein2hit_dict:
                        outputfile.write(dic[proteins] + "\t" + protein2hit_dict[proteins] + "\t" + str(protein2bit_dict[proteins]) +"\n")
                outputfile.close()
                l = []
                for proteins in protein2hit_dict:
                    l.append(protein2hit_dict[proteins])
                    d[name] = l
        print("File " + str(out) + " was created.")
        f.close()
    else:
       pass
       
N= mp.cpu_count()

with mp.Pool(processes = N) as p:
    results = p.map(tblout_annotation, [file for file in tblout_files])