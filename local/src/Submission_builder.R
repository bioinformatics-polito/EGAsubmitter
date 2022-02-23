#!/usr/bin/env Rscript

set.seed(42)

library(tidyverse)
library(yaml)
library(jsonlite)



mainDir <- snakemake@params[['path']]
metadataDir <- paste0(mainDir,"/user_folder/metadata")
submissionDir <- paste0(mainDir,"/submission")
# samplesDir <- paste0(metadataDir,"/samples")
# samples <- list.files(path=samplesDir, pattern="*.json", full.names=TRUE)

### Read all the yaml to get the info we need
SubmissionSubsetTemplate <- fromJSON(snakemake@input[['json']])
SubmissionSubsetTemplate[["title"]] <- readLines(paste0(metadataDir,"/title"), n=1)
SubmissionSubsetTemplate[["description"]] <- readLines(paste0(metadataDir,"/description"), n=1)
### Take all the alias
# SubmissionSubsetTemplate[["submissionSubset"]][["analysisIds"]] <- list(readLines(paste0(metadataDir,"/Analysis_alias"), n=1))
# SubmissionSubsetTemplate[["submissionSubset"]][["dacIds"]] <- list(readLines(paste0(metadataDir,"/DAC_alias"), n=1))
# SubmissionSubsetTemplate[["submissionSubset"]][["datasetIds"]] <- list(readLines(paste0(metadataDir,"/Dataset_alias"), n=1))
# SubmissionSubsetTemplate[["submissionSubset"]][["experimentIds"]] <- list(readLines(paste0(metadataDir,"/Experiment_alias"), n=1))
# SubmissionSubsetTemplate[["submissionSubset"]][["policyIds"]] <- list(readLines(paste0(metadataDir,"/Policy_alias"), n=1))
# SubmissionSubsetTemplate[["submissionSubset"]][["runIds"]] <- list(readLines(paste0(metadataDir,"/Run_alias"), n=1))
# SubmissionSubsetTemplate[["submissionSubset"]][["studyIds"]] <- list(readLines(paste0(metadataDir,"/Study_alias"), n=1))

SubmissionSubsetTemplate[["submissionSubset"]][["analysisIds"]] <- list()
SubmissionSubsetTemplate[["submissionSubset"]][["dacIds"]] <- list()
SubmissionSubsetTemplate[["submissionSubset"]][["datasetIds"]] <- list()
SubmissionSubsetTemplate[["submissionSubset"]][["experimentIds"]] <- list()
SubmissionSubsetTemplate[["submissionSubset"]][["policyIds"]] <- list()
SubmissionSubsetTemplate[["submissionSubset"]][["runIds"]] <- list()
SubmissionSubsetTemplate[["submissionSubset"]][["studyIds"]] <- list()
SubmissionSubsetTemplate[["submissionSubset"]][["sampleIds"]] <- list()
# for ( i in seq(samples) ) {
#   id <- fromJSON(samples[i])
#   SubmissionSubsetTemplate[["submissionSubset"]][["sampleIds"]] <- append(SubmissionSubsetTemplate[["submissionSubset"]][["sampleIds"]], id$alias)
# }

# SubmissionSubsetTemplate[["submissionSubset"]][["sampleIds"]] <- SubmissionSubsetTemplate[["submissionSubset"]][["sampleIds"]][-1]
SubmissionSubsetJson <- toJSON(SubmissionSubsetTemplate, auto_unbox=TRUE, na="string", pretty=TRUE)

write(SubmissionSubsetJson, snakemake@output[['submission']])
file.create(snakemake@output[['done']])
file.create(paste0(submissionDir,"/SubmissionID"))
