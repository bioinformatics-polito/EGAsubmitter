#!/bin/sh

printf "Name of the project (BAM folder): "
read project

export PROJECT_NAME=$project

snakemake -s local/share/snakerule/Snakefile_BAMsubmission
