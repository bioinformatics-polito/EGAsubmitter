#!/bin/sh

printf "Name of the project (folder): "
read project

printf "How many cores do you want to use?: "
read cores

printf "\n"

export PROJECT_NAME=$project
snakemake -s local/share/snakerule/Snakefile_transferRecovery --cores $cores
