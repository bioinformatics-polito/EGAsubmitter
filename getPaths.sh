#!/bin/sh

cat dataset/user_folder/metadata/Samples_Informations.csv | tr "," "\t" | cut -f1,17,18 > dataset/user_folder/metadata/Samples_Informations_3cols.tsv
