#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Goal: join selected annotations
#### Usage: python orf_annotation.py /path/to/directory_wt_all_files/ [databases_in_use]
#### Note: full path needed
###############################################################################

import argparse
import sys

parser = argparse.ArgumentParser(
    description="""Join KO, Pfam, COG, Merops, CAZymes annotations in one table."""
)

__file__ = "orf_annotation.py"
__author__ = "Sandra Godinho Silva (sandragodinhosilva@gmail.com)"
__version__ = "1"
__date__ = "September 9th, 2022"

parser.add_argument(
    "inputDirectory", help="Full path to the input directory where all files are"
)

parser.add_argument(
    "databases_in_use",
    metavar="N",
    type=str,
    nargs="+",
    help="Databases from which we want to have annotation",
)

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
# script_location = "/home/sandra/melange/scripts" #comment when not debugging
base_dir = os.path.dirname(script_location)

database_path = os.path.join(base_dir, "databases")
os.chdir(database_path)


def LoadPfamMap():
    pfam_map = pd.read_csv("Pfam-A.clans.tsv", sep="\t")
    pfam_map.columns = ["PFAM_ACC", "CLAN", "CLAN_Name", "PFAM_Name", "PFAM_desc"]
    pfam_map["ID"] = pfam_map["PFAM_ACC"].str.split(".", expand=True).loc[:, 0]
    pfam_map = pfam_map.drop_duplicates(subset="ID")
    return pfam_map


def LoadCogMap():
    cog_map = pd.read_csv("cog_mapping.tsv", sep="\t")
    cog_map = cog_map.rename(columns={"COG": "ID"})
    return cog_map


def LoadKoMap():
    ko_map = pd.read_csv("ko_mapping.tsv", sep="   ", engine="python", header=None)
    ko_map[["ID", "Desc"]] = ko_map[2].str.split(" ", 1, expand=True)
    ko_map["Desc"] = ko_map["Desc"].str.strip()
    ko_map[["KO_id", "Desc"]] = ko_map["Desc"].str.split(";", 1, expand=True)
    ko_map = ko_map[["ID", "KO_id", "Desc"]].dropna(axis=0)
    ko_map = ko_map.drop_duplicates(subset="ID")
    return ko_map


def LoadMeropsMap():
    merops_map = pd.read_csv("merops_ids.csv")
    merops_map = merops_map[["ID", "name", "desc"]]
    return merops_map


def CreateGeneralMap():
    general_map = pd.DataFrame(
        np.concatenate(
            [
                pfam_map[["ID", "PFAM_Name", "PFAM_desc"]].values,
                cog_map[["ID", "func", "name"]].values,
                ko_map.values,
                merops_map[["ID", "name", "desc"]].values,
            ]
        ),
        columns=["ID", "Name", "Desc"],
    )
    return general_map


pfam_map = LoadPfamMap()
cog_map = LoadCogMap()
ko_map = LoadKoMap()
merops_map = LoadMeropsMap()
general_map = CreateGeneralMap()

###############################################################################
print("Starting... ")

annotation_dir = sys.argv[1]
# annotation_dir = os.path.join(base_dir, "results/Annotation") #comment when not debugging
os.chdir(annotation_dir)

print("Input directory: " + annotation_dir)

databases_in_use = sys.argv[2:]
# databases_in_use = ["kegg","pfam","cog", "cazymes", "merops" ] #comment when not debugging


print("Databases in use: " + str(databases_in_use))

###############################################################################
# Step 2: Create output directory and list files

output_dir = os.path.join(base_dir, "results/Annotation_results")
output_dir_genome = os.path.join(output_dir, "Orfs_per_genome")

try:
    os.mkdir(output_dir)
except:
    pass
print("Output folder: " + output_dir)

try:
    os.mkdir(output_dir_genome)
except:
    pass
# print("Individual genome files: " + output_dir_genome)

ko_pattern = "_kegg.txt"
pfam_pattern = "_pfam_out.txt"
cog_pattern = "protein-id_cog.txt"
merops_pattern = "_merops_out.txt"
cazymes_pattern = "_cazymes_3tools.txt"

entries = list()
for (dirpath, dirnames, filenames) in os.walk(annotation_dir):
    entries += [os.path.join(dirpath, file) for file in filenames]

extensions_to_check = []


# for the individual file counts:
if "kegg" in databases_in_use:
    extensions_to_check.append(ko_pattern)
    d_count_kegg = {}
if "pfam" in databases_in_use:
    extensions_to_check.append(pfam_pattern)
    d_count_pfam = {}
if "cog" in databases_in_use:
    extensions_to_check.append(cog_pattern)
    d_count_cog = {}
if "cazymes" in databases_in_use:
    extensions_to_check.append(cazymes_pattern)
    d_count_cazymes = {}
if "merops" in databases_in_use:
    extensions_to_check.append(merops_pattern)
    d_count_merops = {}
d_resumed = {}  # for count table with one anno per orf
d_stats_all = {}  # for statistics


# Create empty dictionaries:


def FilesToUse():
    d_count = {}  # for count table
    d_files = {}  # for summarize all annotations files per genome
    for filename in entries:
        if filename.endswith(".faa"):
            name = os.path.basename(filename)
            name = os.path.splitext(name)[0]
            if name in d_files:
                d_files[name].append(filename)
            else:
                d_files[name] = []
                d_files[name].append(filename)
        if filename.endswith(tuple(extensions_to_check)):
            name = os.path.basename(filename)
            big_regex = re.compile("|".join(map(re.escape, tuple(extensions_to_check))))
            name = big_regex.sub("", name)
            if "(1)" not in name:
                if name in d_files:
                    d_files[name].append(filename)
                    if "kegg" in databases_in_use:
                        d_count_kegg[name] = []
                    if "pfam" in databases_in_use:
                        d_count_pfam[name] = []
                    if "cog" in databases_in_use:
                        d_count_cog[name] = []
                    if "cazymes" in databases_in_use:
                        d_count_cazymes[name] = []
                    if "merops" in databases_in_use:
                        d_count_merops[name] = []
                else:
                    d_files[name] = []
                    d_files[name].append(filename)
                    d_count[name] = []
    return d_files, d_count


d_files, d_count = FilesToUse()
print(d_files)

print("Parsing input files: ")
###############################################################################
# Step3: fill dictionaries for each annotation
def fill_dic():
    for k, files in d_files.items():
        d_total = {}
        d_stats = {}
        name = k
        output = name + "_all_features.csv"
        ###############     PATTERNS     #############
        for file in files:
            if file.endswith(".faa"):
                genes = file
            if file.endswith(ko_pattern):
                kegg = file
            if file.endswith(pfam_pattern):
                pfam = file
            if file.endswith(cog_pattern):
                cog = file
            if file.endswith(cazymes_pattern):
                cazymes = file
            if file.endswith(merops_pattern):
                merops = file

        with open(os.path.join(genes), "r") as f:
            c = 0
            orf_list = []
            for ln in f:
                if ln.startswith(">"):
                    c += 1
                    orf = ln[1:].split()[0]
                    orf_list.append(orf)
                    d_total[orf] = []
            d_stats["orfs"] = c
        ###############     KEGG     #############
        with open(os.path.join(kegg)) as f:
            c = 0
            lines = f.readlines()
            for line in lines:
                line = (
                    line.rstrip()
                )  # This removes the whitespace at the end of the line
                tabs = line.split(
                    "\t"
                )  # And now we can create a list by splitting each line into pieces based on where the tabs are.
                query = tabs[
                    0
                ]  # The first item in the line is the query protein. We can assign the variable "query" to it.
                try:
                    d_total[query].append(tabs[1])
                    d_count[name].append(tabs[1])
                    d_count_kegg[name].append(tabs[1])  # for the individual file count
                    c += 1
                except:
                    pass
            d_stats["ko"] = c

        ###############     Pfam     ############
        if "pfam" in databases_in_use:
            with open(os.path.join(pfam)) as f:
                c = 0  # for nr of orfs annotated with this database
                l_pfam = dict()
                lines = f.readlines()
                for line in lines[1:]:
                    c += 1
                    line = (
                        line.rstrip()
                    )  # This removes the whitespace at the end of the line
                    tabs = line.split(
                        "\t"
                    )  # And now we can create a list by splitting each line into pieces based on where the tabs are.
                    query = tabs[
                        0
                    ]  # The first item in the line is the query protein. We can assign the variable "query" to it.
                    l_pfam[query] = l_pfam.get(query, []) + [tabs[1]]
                    d_count[name].append(tabs[1])
                    d_count_pfam[name].append(tabs[1])  # for the individual file count
                d_stats["pfam"] = c

        ###############     COG     #############
        if "cog" in databases_in_use:
            with open(os.path.join(cog)) as f:
                c = 0  # for nr of orfs annotated with this database
                lines = f.readlines()
                for line in lines:
                    if line.startswith("Query"):
                        pass
                    else:
                        c += 1
                        line = (
                            line.rstrip()
                        )  # This removes the whitespace at the end of the line
                        tabs = line.split(
                            "\t"
                        )  # And now we can create a list by splitting each line into pieces based on where the tabs are.
                        query = tabs[
                            0
                        ]  # The first item in the line is the query protein. We can assign the variable "query" to it.
                        d_total[query].append(tabs[1])
                        d_count[name].append(tabs[1])
                        d_count_cog[name].append(
                            tabs[1]
                        )  # for the individual file count
                d_stats["cog"] = c

        ###############     merops     ############
        if "merops" in databases_in_use:
            with open(os.path.join(merops)) as f:
                c = 0  # for nr of orfs annotated with this database
                lines = f.readlines()
                for line in lines[1:]:
                    c += 1
                    line = (
                        line.rstrip()
                    )  # This removes the whitespace at the end of the line
                    tabs = line.split(
                        "\t"
                    )  # And now we can create a list by splitting each line into pieces based on where the tabs are.
                    query = tabs[
                        0
                    ]  # The first item in the line is the query protein. We can assign the variable "query" to it.
                    d_total[query].append(tabs[1])
                    d_count[name].append(tabs[1])
                    d_count_merops[name].append(
                        tabs[1]
                    )  # for the individual file count
                d_stats["merops"] = c

        ###############     CAZymes    ############
        if "cazymes" in databases_in_use:
            with open(os.path.join(cazymes)) as f:
                c = 0
                lines = f.readlines()
                for line in lines[1:]:
                    c += 1
                    line = (
                        line.rstrip()
                    )  # This removes the whitespace at the end of the line
                    tabs = line.split(
                        "\t"
                    )  # And now we can create a list by splitting each line into pieces based on where the tabs are.
                    query = tabs[
                        0
                    ]  # The first item in the line is the query protein. We can assign the variable "query" to it.
                    try:
                        d_total[query].append(tabs[1])
                    except:
                        d_total[query] = []
                        d_total[query].append(tabs[1])
                    d_count[name].append(tabs[1])
                    d_count_cazymes[name].append(
                        tabs[1]
                    )  # for the individual file count
                d_stats["cazymes"] = c

        ###############     FINAL     #############
        for k, i in l_pfam.items():
            i = "+".join(i)
            l_pfam[k] = i

        df_pfam = pd.DataFrame.from_dict(l_pfam, orient="index")
        df_pfam = df_pfam.rename(columns={0: "PFAM"})

        d_stats_all[name] = d_stats

        s = pd.Series(d_total).explode()
        s = s[s != ""]
        df = pd.crosstab(index=s.index, columns=s.str[0], values=s, aggfunc="first")
        print(df)
        df = df.rename(columns={"K": "KO", "C": "COG", "M": "MEROPS", "G": "CAZymes"})
        merge = pd.merge(df, df_pfam, how="left", left_index=True, right_index=True)
        merge.to_csv(os.path.join(output_dir_genome, output))

    return df


df = fill_dic()
print("All input files were correctly parsed.")

###############################################################################
# Step4: Create Statistics table
d_stats_all = pd.DataFrame.from_dict(d_stats_all).T
print(d_stats_all)
# df_stats = d_stats_all[["orfs", "pfam", "ko","cog",  "merops", "cazymes"]]

# df_stats["Orfs_anno_pfam%"] = df_stats["pfam"] / df_stats["orfs"] *100
if "kegg" in databases_in_use:
    d_stats_all["Orfs_anno_ko%"] = d_stats_all["ko"] / d_stats_all["orfs"] * 100

if "cog" in databases_in_use:
    d_stats_all["Orfs_anno_cog%"] = d_stats_all["cog"] / d_stats_all["orfs"] * 100

if "merops" in databases_in_use:
    d_stats_all["Orfs_anno_merops%"] = d_stats_all["merops"] / d_stats_all["orfs"] * 100

if "cazymes" in databases_in_use:
    d_stats_all["Orfs_anno_cazymes%"] = (
        d_stats_all["cazymes"] / d_stats_all["orfs"] * 100
    )

d_stats_all.to_csv(os.path.join(output_dir, "Statistics.csv"))
print("Table Statistics.csv was created.")

###############################################################################
# Step5: Create tables


def GetCounter(dataset, d, df_stats=d_stats_all, x="NA"):
    """Create counts, Presence/Absence (PA) and relative abundance tables for the
    input dictionary (d).
    """
    print(str(dataset) + " dataset is being parsed: ")
    df_counter = (
        pd.DataFrame({k: Counter(v) for k, v in d.items()}).fillna(0).astype(int)
    )
    df_counter = df_counter.reindex(
        sorted(df_counter.columns), axis=1
    )  # columns by alphabeticall order

    df_counter_PA = df_counter.copy()  # for presence/absence
    df_counter_abund = df_counter.copy()
    df_counter = df_counter.reset_index()
    print("Count table:")
    print(df_counter.head())

    # Presence/absence dataframe
    df_counter_PA[df_counter_PA > 0] = 1  # transform into Presence/absence matrix
    df_counter_PA = df_counter_PA.reset_index()
    print("Presence/absence table:")
    print(df_counter_PA.head())

    # Relative abundance
    df_counter_abund = df_counter_abund.T  # .reset_index()
    df_counter_abund["sum"] = df_counter_abund.sum(axis=1)
    numeric_cols = df_counter_abund.select_dtypes(exclude=["object"]).columns.to_list()
    numeric_cols.remove("sum")
    df_counter_abund[numeric_cols] = (
        df_counter_abund[numeric_cols]
        .div(df_counter_abund["sum"], axis=0)
        .multiply(100)
    )
    df_counter_abund = df_counter_abund.drop(columns="sum")
    df_counter_abund = df_counter_abund.T.reset_index()
    print("Relative abundance table:")
    print(df_counter_abund.head())

    return df_counter, df_counter_PA, df_counter_abund


###############################################################################
## Kegg
if "kegg" in databases_in_use:
    df_counter_kegg, df_counter_kegg_PA, df_counter_kegg_abund = GetCounter(
        "Kegg", d_count_kegg
    )

    df_counter_kegg.to_csv(os.path.join(output_dir, "Kegg_counts.csv"), index=False)
    df_counter_kegg_PA.to_csv(os.path.join(output_dir, "Kegg_PA.csv"), index=False)
    df_counter_kegg_abund.to_csv(
        os.path.join(output_dir, "Kegg_abund.csv"), index=False
    )

    # Create mappting files
    kegg = df_counter_kegg[["index"]]
    kegg_dic = pd.merge(kegg, ko_map, how="left", left_on="index", right_on="ID")
    kegg_dic.drop(columns=["ID"]).to_csv(
        os.path.join(output_dir, "Kegg_description.csv"), index=False
    )

###############################################################################
## Pfams
if "pfam" in databases_in_use:
    df_counter_pfam, df_counter_pfam_PA, df_counter_pfam_abund = GetCounter(
        "Pfam", d_count_pfam, x="pfam"
    )

    df_counter_pfam.to_csv(os.path.join(output_dir, "Pfam_counts.csv"), index=False)
    df_counter_pfam_PA.to_csv(os.path.join(output_dir, "Pfam_PA.csv"), index=False)
    df_counter_pfam_abund.to_csv(
        os.path.join(output_dir, "Pfam_abund.csv"), index=False
    )

    # Create mappting files
    pfam = df_counter_pfam[["index"]]
    pfam2 = pfam["index"].str.split(".", expand=True)  # .loc[:,0]
    pfam2["index2"] = pfam2.loc[:, 0]
    pfam2 = pfam2.drop(columns=[0, 1])
    pfam_dic = pd.merge(
        pfam2, pfam_map, how="left", left_on="index2", right_on="PFAM_ACC"
    )
    pfam_dic.drop(columns=["index2", "ID"]).to_csv(
        os.path.join(output_dir, "Pfam_description.csv"), index=False
    )

###############################################################################
## COG
if "cog" in databases_in_use:
    df_counter_cog, df_counter_cog_PA, df_counter_cog_abund = GetCounter(
        "Cog", d_count_cog
    )

    df_counter_cog.to_csv(os.path.join(output_dir, "Cog_counts.csv"), index=False)
    df_counter_cog_PA.to_csv(os.path.join(output_dir, "Cog_PA.csv"), index=False)
    df_counter_cog_abund.to_csv(os.path.join(output_dir, "Cog_abund.csv"), index=False)

    # Create mappting files
    cog = df_counter_cog[["index"]]
    cog_dic = pd.merge(cog, cog_map, how="left", left_on="index", right_on="ID")
    cog_dic.drop(columns=["ID"]).to_csv(
        os.path.join(output_dir, "Cog_description.csv"), index=False
    )

###############################################################################
## MEROPS
if "merops" in databases_in_use:
    df_counter_merops, df_counter_merops_PA, df_counter_merops_abund = GetCounter(
        "Merops", d_count_merops
    )

    df_counter_merops.to_csv(os.path.join(output_dir, "Merops_counts.csv"), index=False)
    df_counter_merops_PA.to_csv(os.path.join(output_dir, "Merops_PA.csv"), index=False)
    df_counter_merops_abund.to_csv(
        os.path.join(output_dir, "Merops_abund.csv"), index=False
    )

    # Create mappting files
    merops = df_counter_merops[["index"]]
    merops_dic = pd.merge(
        merops, merops_map, how="left", left_on="index", right_on="ID"
    )
    merops_dic.drop(columns=["ID"]).to_csv(
        os.path.join(output_dir, "Merops_description.csv"), index=False
    )

###############################################################################
## CAZYMES
if "cazymes" in databases_in_use:
    df_counter_cazymes, df_counter_cazymes_PA, df_counter_cazymes_abund = GetCounter(
        "Cazymes", d_count_cazymes
    )

    df_counter_cazymes.to_csv(
        os.path.join(output_dir, "Cazymes_counts.csv"), index=False
    )
    df_counter_cazymes_PA.to_csv(
        os.path.join(output_dir, "Cazymes_PA.csv"), index=False
    )
    df_counter_cazymes_abund.to_csv(
        os.path.join(output_dir, "Cazymes_abund.csv"), index=False
    )

###############################################################################
# END
