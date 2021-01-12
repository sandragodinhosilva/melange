#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Script to shorten contig headers                 
#### Usage: python fasta_cleaner.py /path/to/directory_wt_all_files/ 
#### Note: provide full path!                                          
###############################################################################

import argparse
import fileinput
import os, sys
import re

parser=argparse.ArgumentParser(
    description='''Script to rename contig headers, starting in contig1, 
    		including ncbi accession number.''')

__file__ = "contig_namer.py"
__author__ = 'Sandra Godinho Silva (sandragodinhosilva@gmail.com)'
__version__ = '0.2'
__date__ = '05-12-2020'

parser.add_argument('inputDirectory', 
	help='Full path to the input directory where all files are')

args = parser.parse_args()
###############################################################################
inputDirectory = sys.argv[1]

curdir = inputDirectory
os.chdir(curdir)

entries = os.listdir(curdir)

d={}
fass=[]

for filename in entries:
    if ".fa" in filename:
        fass.append(filename)

for filename in fass:
    with open(filename, 'r') as f:
        count=0
        for line in f:
            if line.strip().startswith(">"):
                count+=1
                k=len(str(count))
        d[filename]=k

for filename in entries:
    if ".fa" in filename:
        i=1
        k = d[filename]
        filepath = os.path.join(curdir, filename)
        with fileinput.FileInput(filepath, inplace=True) as file: 
            name = filename
            x=name.split('_')
            x[0:2] = ['_'.join(x[0:2])]
            final=str(x[0])
            final=re.sub('\.fa$', '', final)
            for line in file:        
                if line.strip().startswith(">"):
                    if i <10:
                        kf= k-1
                        title=">{}_contig".format(final)+ kf*"0" +"{}\n".format(i)
                        line = title
                        i+=1
                    elif i <100:
                        kf= k-2
                        title=">{}_contig".format(final)+ kf*"0" +"{}\n".format(i)
                        line = title
                        i+=1
                    elif  i < 1000:
                        kf= k-3
                        title=">{}_contig".format(final)+ kf*"0" +"{}\n".format(i)
                        line = title
                        i+=1
                    elif i >= 1000 & i < 10000:
                        kf=k-4
                        title=">{}_contig".format(final)+ kf*"0" +"{}\n".format(i)
                        line = title
                        i+=1
                sys.stdout.write(line)
                fileinput.close()

###############################################################################
        
