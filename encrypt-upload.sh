#!/bin/sh

printf "Name of the project (folder): "
read project

printf "How many cores do you want to use?: "
read cores

printf "\n"

export PROJECT_NAME=$project
rm -f dataset/encrypting-uploading/logs/done/filesCrypted.done
rm -f dataset/encrypting-uploading/logs/done/paths.done
rm -f dataset/user_folder/metadata/All_files-names.txt
snakemake -s local/share/snakerule/Snakefile_encrypting-uploading --cores $cores
