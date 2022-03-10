### #!/usr/bin/env Rscript

set.seed(42)

library(tidyverse)
library(yaml)
library(jsonlite)

yamlTemplate <-
"
alias: ''
sampleId: ''
runFileTypeId: ''
experimentId: ''
files:
  - fileId: ''
    fileName: ''
    checksum: ''
    unencryptedChecksum: ''
    checksumMethod: ''
"

yaml <- read_yaml(text = yamlTemplate)
yaml$runFileTypeId <- snakemake@params[['runType']] ### TODO given by the user

mainDir <- snakemake@params[['path']]
EGACryptor <- paste0(mainDir,"/crypting-uploading/EGACryptor")
metadataDir <- paste0(mainDir,"/user_folder/metadata")
samplesDir <- paste0(metadataDir,"/samples")
runsDir <- paste0(metadataDir,"/runs")
expsDir <- paste0(metadataDir,"/exps")
logsDir <- paste0(mainDir,"/submission/logs")


### .csv passed by the user with all samples' informations
# csvNaive = list.files(path=metadataDir, pattern="*.tsv", full.names=TRUE)
csv <- read.csv(paste0(metadataDir,"/Samples_Informations.tsv"), stringsAsFactors = FALSE)
rightOrder <- c("alias","title","description","caseOrControlId","genderId","organismPart","cellLine","region","phenotype","subjectId","anonymizedName","bioSampleId","sampleAge","sampleDetail","attributes.tag","attributes.value","filePaths")
if ( !all(colnames(csv) ==  rightOrder) )  {
  stop("The columns of the file you provide must be in the exact same order we gave in the template.\nPlease, order them accordingly.")
}

### lists for all checksums' files
gpg <- list.files(path=EGACryptor, pattern="*.gpg.md5", recursive=TRUE, full.names=TRUE)
md5 <- list.files(path=EGACryptor, recursive=TRUE, pattern="*.gz.md5", full.names=TRUE)

### I take these two informations for the later submission
sink(paste0(metadataDir,"/title"))
writeLines(csv$title[1])
sink()
sink(paste0(metadataDir,"/description"))
writeLines(csv$description[1])
sink()

txt <- NULL
for ( s in seq(csv[,"alias"]) ) {
  sample <- csv[s,"alias"]
  file <- basename(csv[s,"filePaths"])
  checksum <- paste0(file,".gpg.md5")
  unencryptedChecksum <- paste0(file,".md5")
  yaml[["files"]][[1]][["fileId"]] <- file
  yaml[["files"]][[1]][["fileName"]] <- fileName <- paste0(file,".gpg")
  yaml[["files"]][[1]][["checksum"]] <- readLines(gpg[basename(gpg)==checksum], n=1, warn=FALSE)
  yaml[["files"]][[1]][["unencryptedChecksum"]] <- readLines(md5[basename(md5)==unencryptedChecksum], n=1, warn=FALSE)
  check <- list(c(checksum, unencryptedChecksum)) #fileName
  # for ( i in seq(check) ) {
    # if ( !check[i] %in% basename(list.files(path=EGACryptor, recursive=TRUE, full.names=FALSE)) ) {
    if ( !checksum %in% basename(gpg) | !unencryptedChecksum %in% basename(md5) ) {
      stop(paste("Sorry, a file from the crypting phase is missing for the sample",sample))
    }
  # }
  json <- toJSON(yaml, auto_unbox=TRUE, na="string", pretty=TRUE)
  write(json, paste0(runsDir,"/Run_",sample,".json"))
  txt <- append(txt, paste0(logsDir,"/done/runs/",sample,"-runSubmission.done"))
}

write.table(txt, paste0(runsDir,"/Allfiles_list.txt"), quote=FALSE, row.names=FALSE, col.names=FALSE)

csv$filePaths <- NULL # we remove this column for the json
write.csv(csv, file=paste0(samplesDir,"/SamplesInformations.csv"), row.names=FALSE)

### produces files lists for submissionfunctions
getJson <- NULL
getSample <- NULL
# getExps <- NULL
for ( r in 1:nrow(csv) ) {
  sample <- paste0(csv[r,"alias"])
  getJson <- append(getJson, paste0(samplesDir,"/",sample,".json"))
  getSample <- append(getSample, paste0(logsDir,"/done/samples/",sample,"-sampleSubmission.done"))
  # getExps <- append(getExps, paste0(logsDir,"/done/exps/",sample,"-experimentSubmission.done"))
}

write.table(getJson, paste0(metadataDir,"/AllSamples_list.txt"), quote=FALSE, row.names=FALSE, col.names=FALSE)
write.table(getSample, paste0(samplesDir,"/Allfiles_list.txt"), quote=FALSE, row.names=FALSE, col.names=FALSE)
# write.table(getExps, paste0(expsDir,"/AllExps_list.txt"), quote=FALSE, row.names=FALSE, col.names=FALSE)
file.create(snakemake@output[['done']])
