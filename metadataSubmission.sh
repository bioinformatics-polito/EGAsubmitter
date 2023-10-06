#!/bin/sh

printf "Name of the project (folder): "
read project

printf "Please, select the file type of your files:\n
- srf
- sff
- fastq
- Illumina_native
- Illumina_native_qseq
- SOLiD_native_csfasta
- PacBio_HDF5
- bam
- cram
- CompleteGenomics_native
- OxfordNanopore_native

File type value: "

read fileType

export FILETYPE=$fileType PROJECT_NAME=$project

snakemake -s local/share/snakerule/Snakefile_submission -j1
