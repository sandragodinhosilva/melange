---
layout: default
title: Melange description
nav_order: 1
---

# Melange Description

## The problem

 With the advent of high-throughput DNA sequencing technologies, the amount of genomic data available far exceeds the amount of data that is thoroughly analysed. This can be partly explained by the difficulties of sorting and comparing large amounts of data, which is usually computationally intensive and often intractable. However, such large comparative genomics studies can be essential to determine important genomic or functional traits of different groups of organisms based on phylogeny, taxonomy, ecosystem origin, etc.

## Our solution

We present **Melange**, an innovative tool for genomic annotation that overcomes existing limitations of flexibile solutions to simultaneously annotate large groups of prokaryotic sequences, enabling large-scale comparative studies of prokaryote genomes or metagenomes. Melange allows functional annotation using multiple schemes, including Pfam, COG, KEGG Orthology, CAZymes, and MEROPS. It handles unassembled (meta)genomic sequencing data in fastq format, (meta)genome assemblies, and predicted amino acid sequences. Melange automatically downloads and configures all necessary tools and databases, and executes all processes with a single command. It is implemented in Python and Snakemake, ensuring reproducibility and transparency in the annotation process. Melange is highly scalable and can annotate from one to thousands of genomes, running on various Linux systems, from personal computers to high-performance clusters. The results are presented in a tabular format that is easy to analyze and compare, facilitating diverse and personalized comparative studies. Melange is a valuable resource for functional genomics studies, providing a user-friendly and efficient solution for annotating and analyzing large groups of genomes.

## Performance

Melange is designed to facilitate the process of annotating large groups of genomes with different databases. Even though computational requirements are taken into consideration, this tool is not designed to outperform existing annotation tools directly. Instead, Melange is focused on facilitating the whole process, from installing all necessary dependencies to the automatic distribution (and parallelization if the system allows) of the tasks. It places an emphasis on ease of use and customization, as also on the diversification of the outputs provided at the end. 

* * *

