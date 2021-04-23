#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Goal: join KO, Pfam, COG annotations                  
#### Usage: python orf_annotation.py /path/to/directory_wt_all_files/ 
#### Note: provide full path!                                          
###############################################################################

import argparse
import sys
parser=argparse.ArgumentParser(
    description='''Join KO, Pfam, COG annotations in one table.''')

__file__ = "orf_annotation.py"
__author__ = 'Sandra Godinho Silva (sandragodinhosilva@gmail.com)'
__version__ = '0.9'
__date__ = 'December 3rd, 2020'

parser.add_argument('inputDirectory', 
		help='Full path to the input directory where all files are')

# parser.add_argument('outputDirectory')

# parser.add_argument('databaseDirectory')

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
# MAPPINGS:

# From the script location, find databases directory
script_location = sys.path[0]
#script_location = "/home/sandra/MeLanGE2/scripts"
#out_dir = os.path.dirname(os.path.dirname(script_location))
out_dir = os.path.dirname(script_location)

database_path = os.path.join(out_dir, "databases")
os.chdir(database_path)
    
def LoadPfamMap():
    pfam_map = pd.read_csv("Pfam-A.clans.tsv", sep="\t")
    pfam_map.columns = ['PFAM_ACC', 'CLAN','CLAN_Name','PFAM_Name', 'PFAM_desc']
    pfam_map["ID"] = pfam_map["PFAM_ACC"].str.split(".", expand=True).loc[:,0]
    pfam_map = pfam_map.drop_duplicates(subset="ID")
    return pfam_map
def LoadCogMap():
    cog_map = pd.read_csv("cog_mapping.tsv", sep="\t")
    cog_map = cog_map.rename(columns={"COG":"ID"})
    return cog_map
def LoadKoMap():
    ko_map = pd.read_csv("ko_mapping.tsv", sep="   ", engine='python', header=None)
    ko_map[["ID","Desc"]] = ko_map[2].str.split(" ", 1, expand=True)
    ko_map["Desc"] = ko_map["Desc"].str.strip()
    ko_map[["KO_id", "Desc"]] = ko_map["Desc"].str.split(";", 1, expand=True)
    ko_map = ko_map[["ID", "KO_id", "Desc"]].dropna(axis=0)
    ko_map = ko_map.drop_duplicates(subset="ID")
    return ko_map
def CreateGeneralMap():
    general_map = pd.DataFrame(np.concatenate([pfam_map[["ID", 'PFAM_Name', 'PFAM_desc']].values, cog_map[["ID", "func", "name"]].values, ko_map.values]), columns=["ID", "Name", "Desc"])
    return general_map
    
pfam_map= LoadPfamMap()
cog_map = LoadCogMap()
ko_map = LoadKoMap()
general_map = CreateGeneralMap()

###############################################################################
print("Starting... ")

inputDirectory = sys.argv[0]
curdir = os.path.join(out_dir, "results")
os.chdir(curdir)

print("Input directory: " + curdir)

curdir = os.getcwd()
###############################################################################
#Step 2: Create output directory and list files
curdir = os.getcwd()
output_dir = os.path.join(curdir,"Annotation_results")
output_dir_genome = os.path.join(output_dir,"Orfs_per_genome")

try:
    os.mkdir(output_dir)
except:
    pass
print("Output folder: " + output_dir)

try:
    os.mkdir(output_dir_genome)
except:
    pass
print("Individual genome files: " + output_dir_genome)

l = os.listdir()

#To change this default, substitute:
ko_pattern = ".ko.out"
pfam_pattern = "_tblout_pfam.txt"
cog_pattern = "protein-id_cog.txt"

entries = list()
for (dirpath, dirnames, filenames) in os.walk(curdir):
    entries += [os.path.join(dirpath, file) for file in filenames]

def CreateDictionaries():
    # Create empty dictionaries:
    d_count={} # for count table
    # for the individual file counts:
    d_count_kegg={}
    d_count_pfam={}
    d_count_cog={}
    d_resumed = {} # for count table with one anno per orf
    d_stats_all = {} # for statistics
    return d_count, d_count_kegg, d_count_pfam, d_count_cog, d_resumed, d_stats_all

def FilesToUse():
    d_files = {} #for summarize all annotations files per genome
    extensionsToCheck = (ko_pattern, pfam_pattern, cog_pattern)
    for filename in entries:
        if filename.endswith(extensionsToCheck):
            name = os.path.basename(filename)
            big_regex = re.compile('|'.join(map(re.escape, extensionsToCheck)))
            name = big_regex.sub("", name)
            if "(1)" not in name:
                if name in d_files:
                    d_files[name].append(filename)
                    # for the individual file counts:
                    d_count_kegg[name] = []
                    d_count_pfam[name] = []
                    d_count_cog[name] = []
                else:
                    d_files[name] = []
                    d_files[name].append(filename)
                    d_count[name]= []
    return d_files, d_count

d_count, d_count_kegg, d_count_pfam, d_count_cog, d_resumed, d_stats_all = CreateDictionaries()
d_files, d_count = FilesToUse()

print("Parsing input files: Kegg, Pfam, COG annotations")
###############################################################################  
#Step3: fill dictionaries for each annotation

def fill_dic():
    for k, files in d_files.items():
        d_kegg = {}
        d_stats ={}
        name = k
        output = name + "_all_features.csv"
        ###############     PATTERNS     #############        
        for file in files:
            if file.endswith(ko_pattern):
                kegg = file
            elif file.endswith(pfam_pattern):
                pfam = file
            elif file.endswith(cog_pattern):
                cog= file
        ###############     KEGG     #############
        with open(os.path.join(kegg)) as f:
            c=0
            c_ko =0
            lines = f.readlines()
            for line in lines:
                c+=1
                line = line.rstrip() # This removes the whitespace at the end of the line
                tabs = line.split("\t") # And now we can create a list by splitting each line into pieces based on where the tabs are.         
                query = tabs[0] # The first item in the line is the query protein. We can assign the variable "query" to it. 
                d_kegg[query] = []
                if len(tabs) == 1:
                    d_kegg[query].append("")
                else:
                    d_kegg[query].append(tabs[1])
                    d_count[name].append(tabs[1])
                    d_count_kegg[name].append(tabs[1]) # for the individual file count
                    c_ko +=1
            d_stats["orfs"]=c
            d_stats["ko"] = c_ko
        ###############     Pfam     ############
        with open(os.path.join(pfam)) as f:
            c=0
            l_pfam = dict() 
            lines = f.readlines()
            for line in lines[1:]:
                c+=1
                line = line.rstrip() # This removes the whitespace at the end of the line
                tabs = line.split("\t") # And now we can create a list by splitting each line into pieces based on where the tabs are.         
                query = tabs[0] # The first item in the line is the query protein. We can assign the variable "query" to it. 

                l_pfam[query] = l_pfam.get(query, []) + [tabs[1]]
                d_count[name].append(tabs[1])
                d_count_pfam[name].append(tabs[1]) # for the individual file count

            d_stats["pfam"]=c
        ###############     COG     #############        
        with open(os.path.join(cog)) as f:
            c=0
            lines = f.readlines()
            for line in lines:
                if line.startswith("Query"):
                    pass
                else:
                    c+=1
                    line = line.rstrip() # This removes the whitespace at the end of the line
                    tabs = line.split("\t") # And now we can create a list by splitting each line into pieces based on where the tabs are.         
                    query = tabs[0] # The first item in the line is the query protein. We can assign the variable "query" to it. 
                    d_kegg[query].append(tabs[1])
                    d_count[name].append(tabs[1])
                    d_count_cog[name].append(tabs[1]) # for the individual file count
            d_stats["cog"]=c
        
        ###############     FINAL     ############# 
        
        for k,i in l_pfam.items():
            i = '+'.join(i)
            l_pfam[k]=i
                
        df_pfam = pd.DataFrame.from_dict(l_pfam, orient='index')
        df_pfam = df_pfam.rename(columns={0:"Pfam"})
        
        
        d_stats_all[name] = d_stats

        s=pd.Series(d_kegg).explode()
        s=s[s!='']
        df=pd.crosstab(index=s.index,columns=s.str[0],values=s,aggfunc='first')
        
        df = df.rename(columns={"K":"KO", "C": "COG"})
        merge = pd.merge(df, df_pfam, how="left", left_index=True, right_index=True)        
        merge.to_csv(os.path.join(output_dir_genome,output))

    return df

df = fill_dic()
print("All input files were correctly parsed.")
###############################################################################
#Step4: Create Statistics table
d_stats_all = pd.DataFrame.from_dict(d_stats_all).T
df_stats = d_stats_all[["orfs", "pfam", "ko","cog"]]

#df_stats["Orfs_anno_pfam%"] = df_stats["pfam"] / df_stats["orfs"] *100
df_stats["Orfs_anno_ko%"] = df_stats["ko"] / df_stats["orfs"] *100
df_stats["Orfs_anno_cog%"] = df_stats["cog"] / df_stats["orfs"] *100

df_stats.to_csv(os.path.join(output_dir, "Statistics.csv"))
print("Table Statistics.csv was created.")

###############################################################################
#Step5: Create tables

#dataset="Pfam"
#d= d_count_pfam
#x="pfam"
def GetCounter(dataset, d, df_stats=df_stats, x="NA"):
    """ Create counts, Presence/Absence (PA) and relative abundance tables for the 
    input dictionary (d).
    """
    print(str(dataset) + " dataset is being parsed: ")
    df_counter = pd.DataFrame({k:Counter(v) for k, v in d.items()}).fillna(0).astype(int)
    df_counter = df_counter.reindex(sorted(df_counter.columns), axis=1) #columns by alphabeticall order

    df_counter_PA = df_counter.copy() # for presence/absence
    df_counter_abund = df_counter.copy()
    df_counter = df_counter.reset_index()
    print("Count table:")
    print(df_counter.head())

    # Presence/absence dataframe
    df_counter_PA[df_counter_PA > 0] = 1 #transform into Presence/absence matrix
    df_counter_PA = df_counter_PA.reset_index()
    print("Presence/absence table:")
    print(df_counter_PA.head())
    
    # Relative abundance
    df_counter_abund = df_counter_abund.T#.reset_index()
    df_counter_abund["sum"] = df_counter_abund.sum(axis=1)
    numeric_cols = df_counter_abund.select_dtypes(exclude=["object"]).columns.to_list()
    numeric_cols.remove("sum")
    df_counter_abund[numeric_cols] = df_counter_abund[numeric_cols].div(df_counter_abund["sum"], axis=0).multiply(100)
    df_counter_abund = df_counter_abund.drop(columns="sum")
    df_counter_abund = df_counter_abund.T.reset_index()
    print("Relative abundance table:")
    print(df_counter_abund.head())
    
    return df_counter, df_counter_PA, df_counter_abund

###############################################################################
## KO
df_counter_kegg, df_counter_kegg_PA, df_counter_kegg_abund = GetCounter("Kegg", d_count_kegg)

df_counter_kegg.to_csv(os.path.join(output_dir,"Kegg_counts.csv"),index=False)
df_counter_kegg_PA.to_csv(os.path.join(output_dir,"Kegg_PA.csv"),index=False)
df_counter_kegg_abund.to_csv(os.path.join(output_dir,"Kegg_abund.csv"),index=False)

###############################################################################
## Pfams
df_counter_pfam, df_counter_pfam_PA,df_counter_pfam_abund = GetCounter("Pfam", d_count_pfam, x="pfam")

df_counter_pfam.to_csv(os.path.join(output_dir,"Pfam_counts.csv"), index=False)
df_counter_pfam_PA.to_csv(os.path.join(output_dir,"Pfam_PA.csv"), index=False)
df_counter_pfam_abund.to_csv(os.path.join(output_dir,"Pfam_abund.csv"), index=False)

###############################################################################
## COG
df_counter_cog, df_counter_cog_PA, df_counter_cog_abund = GetCounter("Cog", d_count_cog)

df_counter_cog.to_csv(os.path.join(output_dir,"Cog_counts.csv"), index=False)
df_counter_cog_PA.to_csv(os.path.join(output_dir,"Cog_PA.csv"), index=False)
df_counter_cog_abund.to_csv(os.path.join(output_dir,"Cog_abund.csv"), index=False)

###############################################################################
#Create mappting files

pfam = df_counter_pfam[["index"]]
pfam2 = pfam["index"].str.split(".", expand=True)#.loc[:,0]
pfam2["index2"] = pfam2.loc[:,0]
pfam2 = pfam2.drop(columns=[0,1])
pfam_dic = pd.merge(pfam2, pfam_map, how="left", left_on="index2", right_on="PFAM_ACC")
pfam_dic.drop(columns=["index2","ID"]).to_csv(os.path.join(output_dir,"Pfam_description.csv"), index=False)

cog = df_counter_cog[["index"]]
cog_dic = pd.merge(cog, cog_map, how="left", left_on="index", right_on="ID")
cog_dic.drop(columns=["ID"]).to_csv(os.path.join(output_dir,"Cog_description.csv"), index=False)

kegg = df_counter_kegg[["index"]]
kegg_dic = pd.merge(kegg, ko_map, how="left", left_on="index", right_on="ID")
kegg_dic.drop(columns=["ID"]).to_csv(os.path.join(output_dir,"Kegg_description.csv"), index=False)

#END