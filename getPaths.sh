#!/bin/sh

cat dataset/user_folder/metadata/Samples_Informations.csv | tr "," "\t" | sed 1d | cut -f1,17,18 > dataset/user_folder/metadata/Samples_Informations_3cols.tsv.tmp
sed 's/\"//g' dataset/user_folder/metadata/Samples_Informations_3cols.tsv.tmp > dataset/user_folder/metadata/Samples_Informations_3cols.tsv
rm dataset/user_folder/metadata/Samples_Informations_3cols.tsv.tmp
