#!/bin/sh
# This is a script created for testing purposes, it encrypts everything without uploading resulting files to the EGA ftp server.

# Variables needed to have colors in echo output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

printf "Name of the project (folder): "
read project

printf "How many cores do you want to use?: "
read cores

printf "\n"

export PROJECT_NAME=$project
rm -f dataset/encrypting-uploading/logs/done/filesCrypted.done
rm -f dataset/encrypting-uploading/logs/done/paths.done
rm -f dataset/user_folder/metadata/All_files-names.txt
echo "${RED}WARNING${NC}: you are using a dummy/dry run script that will only encrypt files to test EGAsubmitter,  \n use encrypt-upload.sh to work on real datasets."
snakemake -s local/share/snakerule/Snakefile_encrypting-uploading --cores $cores all_crypted

echo "${RED}Checking if all the files have been crypted...${NC}"
n=$(sort dataset/user_folder/metadata/All_files-names.txt | uniq | wc -l)
# We check wheter the list of files contains 15 paths, since we have 5 example input files (1 encrypted files and two gpg each).
if [ "$n" -ne "15" ]
then
  echo "Something failed in the test, we did not generate a complete list of encrypted files!${NC}"
  echo "Encryption test: ${RED}failed${NC}"
else
  echo "Encryption test: ${GREEN}passed${NC}"
fi
