#!/bin/sh


printf "Name of the project (folder): "
read project

stty -echo

printf "How many cores do you want to use?: "
read cores

stty -echo

printf "\n"


EGA_USER=EGA_USER EGA_PWD=EGA_PWD PROJECT_NAME=$project snakemake -s local/share/snakerule/Snakefile_encrypting-uploading --cores $cores
