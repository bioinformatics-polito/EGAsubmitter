#!/bin/sh


printf "Name of the project (folder): "
read project

stty -echo

printf "How many cores do you want to use?: "
read cores

stty -echo

printf "\n"


PROJECT_NAME=$project snakemake -s local/share/snakerule/Snakefile_encrypting-uploading --cores $cores
