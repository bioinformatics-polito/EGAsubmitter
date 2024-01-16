#!/bin/sh

printf "EGA submission ID: "
read id

export SUBMISSION_ID=$id

snakemake -s local/share/snakerule/Snakefile_get-EGA_IDs
