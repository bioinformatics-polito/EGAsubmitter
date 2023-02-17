#!/bin/sh

printf "Name of the project (folder): "
read project

printf "Please, select the type (number) of your files:\n
0 for BAM
1 for Complete Genomics
2 for CRAM
3 for Fasta
4 for One Fastq file (Single)
5 for Two Fastq files (Paired)
6 for PacBio HDF5
7 for SFF
8 for SRF

File type value: "

read fileType

export FILETYPE=$fileType PROJECT_NAME=$project

snakemake -s local/share/snakerule/Snakefile_submission -j1
