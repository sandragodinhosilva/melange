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

__file__ = "orf_annotation.py"
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
# MAPPINGS:
    
script_location = sys.path[0]
database_path = os.path.join(script_location, "databases")
os.chdir(database_path)
    
curdir = os.getcwd()
print("Script location: " + curdir)
    
def LoadPfamMap():
    pfam_map = pd.read_csv("Pfam-A.clans.tsv", sep="\t")
    pfam_map.columns = ['PFAM_ACC', 'CLAN','CLAN_Name','PFAM_Name', 'PFAM_desc']
    #pfam_map = pfam_map.rename(columns={"PFAM_ACC": "ID"})
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

for file in tblout_files:
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
###############################################################################
#Step 2: Create output directory and list files

#path_parent = os.path.dirname(inputDirectory)
os.chdir(sys.path[0])
curdir = os.getcwd()

output_dir = os.path.join(curdir,"FAW_results")
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
cazyme_pattern = "overview.txt"
cazyme_pattern2 = "_overview.txt"

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
    d_count_cazyme={}
    d_resumed = {} # for count table with one anno per orf
    d_stats_all = {} # for statistics
    return d_count, d_count_kegg, d_count_pfam, d_count_cog, d_count_cazyme, d_resumed, d_stats_all

def FilesToUse():
    d_files = {} #for summarize all annotations files per genome
    extensionsToCheck = (ko_pattern, pfam_pattern, cog_pattern, cazyme_pattern, cazyme_pattern2)
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
                    d_count_cazyme[name] = []
                else:
                    d_files[name] = []
                    d_files[name].append(filename)
                    d_count[name]= []
    return d_files, d_count

d_count, d_count_kegg, d_count_pfam, d_count_cog, d_count_cazyme, d_resumed, d_stats_all = CreateDictionaries()
d_files, d_count = FilesToUse()

print("Parsing input files: Kegg, Pfam, COG and Cazyme annotations")
###############################################################################  
#Step3: fill dictionaries for each annotation
for k, files in d_files.items():
    d_kegg = {}
    d_stats ={}
    name = k
    output = name + "_all_features.csv"
    output_resumed = name + "_1anno_per_orf.csv"
    #print(name)
    for file in files:
        if file.endswith(ko_pattern):
            kegg = file
        elif file.endswith(pfam_pattern):
            pfam = file
        elif file.endswith(cog_pattern):
            cog= file
        elif file.endswith(cazyme_pattern):
            cazyme = file
        elif file.endswith(cazyme_pattern2):
            cazyme = file
    ###############     KEGG     #############
    with open(os.path.join(curdir,kegg)) as f:
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
    with open(os.path.join(curdir,pfam)) as f:
        c=0
        lines = f.readlines()
        for line in lines[1:]:
            c+=1
            line = line.rstrip() # This removes the whitespace at the end of the line
            tabs = line.split("\t") # And now we can create a list by splitting each line into pieces based on where the tabs are.         
            query = tabs[0] # The first item in the line is the query protein. We can assign the variable "query" to it. 
            d_kegg[query].append(tabs[1])
            d_count[name].append(tabs[1])
            d_count_pfam[name].append(tabs[1]) # for the individual file count
        d_stats["pfam"]=c
    ###############    Cazymes     ###########
    with open(os.path.join(curdir,cazyme)) as f:
        c=0
        lines = f.readlines()
        for line in lines[1:]:

            line = line.rstrip() # This removes the whitespace at the end of the line
            if line.endswith("3"): #select orfs with at least
                c += 1
                tabs = line.split("\t") # And now we can create a list by splitting each line into pieces based on where the tabs are.             
                query = tabs[0]
                l2=[]
                for tab in tabs[1:4]:
                    tab = re.sub("[\(\[].*?[\)\]]", "", tab)
                l2.append(tab)
                cnt = Counter(l2)
                common = cnt.most_common(3)
                if len(common)==1:
                    result = common[0][0]
                elif len(common) == 2:
                    result = common[0][0]
                elif len(common) == 3:
                    result = l2[0] #if there isn't one most common result, select HHMER
                d_count[name].append(result)
                d_count_cazyme[name].append(result) # for the individual file count
                if result.startswith("G"): # to avoid that PLUs enter in the Pfam column
                    pass
                else:
                    result = "G"+result
                try:
                    d_kegg[query].append(result)
                except:
                    pass
                        #print(name + " does not have cazyme annotation")
            elif line.endswith("2"):#select orfs with at least 2 hits
                c += 1
                tabs = line.split("\t") # And now we can create a list by splitting each line into pieces based on where the tabs are.             
                query = tabs[0]
                l2=[]
                for tab in tabs[1:4]:
                    tab = re.sub("[\(\[].*?[\)\]]", "", tab)
                    if tab != "-":
                        l2.append(tab)
                try:
                    result = l2[0] #if there is two hits try to select HHMER
                except:
                    result = l2[1] # or Hotpet
                d_count[name].append(result)
                d_count_cazyme[name].append(result) # for the individual file count
                if result.startswith("G"): # to avoid that PLUs enter in the Pfam column
                    pass
                else:
                    result = "G"+result
                try:
                    d_kegg[query].append(result)
                except:
                    pass
        d_stats["cazymes"]=c
    ###############     COG     #############        
    with open(os.path.join(curdir,cog)) as f:
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

    d_stats_all[name] = d_stats
    
    s=pd.Series(d_kegg).explode()
    s=s[s!='']
    df=pd.crosstab(index=s.index,columns=s.str[0],values=s,aggfunc='first')
    
    df = df.rename(columns={"K":"KO", "G": "CAZyme", "P":"Pfam", "C": "COG"})
    df.to_csv(os.path.join(output_dir_genome,output))
    try:
        df["CAZyme"] = df["CAZyme"].str.replace("GPL", "PL") # transform masked PLUs into original format
        pfam_ = df["Pfam"]
        ko_ = df["KO"]
        cog_ =df["COG"]
        cazymes_ = df["CAZyme"]
        df0 = cazymes_.combine_first(pfam_) #combine first to set order
        df1 = df0.combine_first(ko_)
        df2 = df1.combine_first(cog_)
        d_resumed[name]=df2
        
    except:
        print("Note: " + name + " doesn't have cazyme annotation.")
        pfam_ = df["Pfam"]
        ko_ = df["KO"]
        cog_ =df["COG"]
        df1 = pfam_.combine_first(ko_)
        df2 = df1.combine_first(cog_)
        d_resumed[name]=df2
    df2.columns=["Orf", "Annotation"]
    df2.to_csv(os.path.join(output_dir_genome,output_resumed))

print("All input files were correctly parsed.")
###############################################################################
#Step4: Create Statistics table
df_stats = pd.DataFrame.from_dict(d_stats_all).T
df_stats = df_stats[["orfs", "pfam", "ko","cog", "cazymes"]]

#df_stats["Orfs_anno_pfam%"] = df_stats["pfam"] / df_stats["orfs"] *100
df_stats["Orfs_anno_ko%"] = df_stats["ko"] / df_stats["orfs"] *100
df_stats["Orfs_anno_cog%"] = df_stats["cog"] / df_stats["orfs"] *100
df_stats["Orfs_anno_cazymes%"] = df_stats["cazymes"] / df_stats["orfs"] *100

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
## CAZymes
df_counter_cazyme, df_counter_cazyme_PA, df_counter_cazyme_abund = GetCounter("Cazyme", d_count_cazyme)

df_counter_cazyme.to_csv(os.path.join(output_dir,"Cazyme_counts.csv"), index=False)
df_counter_cazyme_PA.to_csv(os.path.join(output_dir,"Cazyme_PA.csv"), index=False)
df_counter_cazyme_abund.to_csv(os.path.join(output_dir,"Cazyme_abund.csv"), index=False)

###############################################################################
#every orf only has one annotation:
df_counter_all, df_counter_all_PA, df_counter_all_abund = GetCounter("All orfs - one annotation per orf", d_count)

df_counter_all.to_csv(os.path.join(output_dir,"all_counts.csv"), index=False)
df_counter_all_PA.to_csv(os.path.join(output_dir,"all_PA.csv"), index=False)
df_counter_all_abund.to_csv(os.path.join(output_dir,"all_abund.csv"), index=False)

###############################################################################
#every orf only has one annotation:
df_counter_all, df_counter_all_PA, df_counter_all_abund = GetCounter("All orfs", d_resumed)

df_counter_all.to_csv(os.path.join(output_dir,"all_1_per_orf_counts.csv"), index=False)
df_counter_all_PA.to_csv(os.path.join(output_dir,"all_1_per_orf_PA.csv"), index=False)
df_counter_all_abund.to_csv(os.path.join(output_dir,"all_1_per_orf_abund.csv"), index=False)
###############################################################################
print("Success! You may find your outputs at " + str(output_dir))
#END


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
