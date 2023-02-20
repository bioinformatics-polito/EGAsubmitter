#!/bin/sh
# This is a script created for testing purposes, it creates all the required json with metadata that needs to be submitted to the EGA API via curl but do not submit them.
# Since we require IDs returned by the EGA API to link all objects together and proceed with Experiment/Run/Dataset submission this will proceed up to creating Submission.json.

# Variables needed to have colors in echo output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "${RED}WARNING${NC}: you are using a dummy/dry run script that will only create json with metadata to test EGAsubmitter,  \n use metadataSubmission.sh to work on real datasets."

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

snakemake -s local/share/snakerule/Snakefile_submission -j1 sub

echo "Checking if all the yaml have converted to json..."
n=$(ls dataset/user_folder/metadata/json/ | wc -l)
if [ "$n" -ne "5" ]
then
  echo "${RED}Something failed in the test, we did not generate all yaml!${NC}"
  echo "Yaml test: ${RED}failed${NC}"
else
  echo "Yaml test: ${GREEN}passed${NC}"
fi

echo "Checking if all the samples have their json..."
n=$(ls dataset/user_folder/metadata/samples/*json | wc -l)
if [ "$n" -ne "5" ]
then
  echo "${RED}Something failed in the test, we did not generate all samples json!${NC}"
  echo "Yaml test: ${RED}failed${NC}"
else
  echo "Yaml test: ${GREEN}passed${NC}"
fi

echo "Checking if all the files listing all samples are complete..."
n=$(sort dataset/user_folder/metadata/samples/SamplesInformation.csv | uniq | wc -l)
if [ "$n" -ne "6" ]
then
  echo "${RED}Something failed in the test, we did not generate a correct list of samples to go on with EGA submission!${NC}"
  echo "Samples list test: ${RED}failed${NC}"
else
  echo "Samples test: ${GREEN}passed${NC}"
fi