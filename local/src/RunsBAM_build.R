### #!/usr/bin/env Rscript

set.seed(42)

library(tidyverse)
library(yaml)
library(jsonlite)


mainDir <- snakemake@params[['path']]
files <- snakemake@params[['encryptedFiles']]
EGACryptor <- paste0(mainDir,"/encrypting-uploading/EGACryptor")
metadataDir <- paste0(mainDir,"/user_folder/metadata")
samplesDir <- paste0(metadataDir,"/samples")
runsDir <- paste0(metadataDir,"/runs")
expsDir <- paste0(metadataDir,"/exps")
logsDir <- paste0(mainDir,"/submission/logs")


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
  - fileId: ''
    fileName: ''
    checksum: ''
    unencryptedChecksum: ''
    checksumMethod: ''
"
yaml <- read_yaml(text=yamlTemplate)
yaml$runFileTypeId <- 0 # This script is for BAM only 

### .csv passed by the user with all samples' informations
csv <- read.csv(paste0(metadataDir,"/Samples_Informations.csv"), header=TRUE, quote='""',  stringsAsFactors = FALSE)
rightOrder <- c("alias","title","description","caseOrControlId","genderId","organismPart","cellLine","region","phenotype","subjectId","anonymizedName","bioSampleId","sampleAge","sampleDetail","attributes.tag","attributes.value","fileName","filePath")
if ( !all(colnames(csv) ==  rightOrder) )  {
  stop("The columns of the file you provide must be in the exact same order we gave in the template.\nPlease, order them accordingly.")
}

### lists for all checksums' files
gpg <- list.files(path=EGACryptor, pattern="*bam.gpg.md5", recursive=TRUE, full.names=TRUE)
md5 <- list.files(path=EGACryptor, pattern="*bam.md5", recursive=TRUE, full.names=TRUE)
md5 <- md5[!grepl(".gpg.md5", md5)]


for ( s in seq(csv[,"alias"]) ) {
    sample <- csv[s,"alias"]
    file <- csv[s,"fileName"]
    checksum <- paste0(file,".gpg.md5")
    unencryptedChecksum <- paste0(file,".md5")
    gpgtmp <- gpg[grep(sample, gpg)]
    md5tmp <- md5[grep(sample, md5)]
    if ( !checksum %in% basename(gpgtmp) | !unencryptedChecksum %in% basename(md5tmp) ) {
        stop(paste("Sorry, a file from the crypting phase is missing for the sample",sample))
    }
    yaml[["files"]][[1]][["fileId"]] <- file
    yaml[["files"]][[1]][["fileName"]] <- fileName <- paste0(file,".gpg")
    yaml[["files"]][[1]][["checksum"]] <- readLines(gpgtmp[basename(gpgtmp)==checksum], n=1, warn=FALSE)
    yaml[["files"]][[1]][["unencryptedChecksum"]] <- readLines(md5tmp[basename(md5tmp)==unencryptedChecksum], n=1, warn=FALSE)
    check <- list(c(checksum, unencryptedChecksum))
    json <- toJSON(yaml, auto_unbox=TRUE, na="string", pretty=TRUE)
    write(json, paste0(runsDir,"/Run_",sample,".json"))
}

csv$fileName <- NULL # we remove this column for the json
csv$filePath <- NULL # we remove this column for the json
# csv <- csv[!duplicated(csv$alias),]

### produces files lists for submissionfunctions
getRun <- NULL
# getJson <- NULL
# getSample <- NULL
# getExps <- NULL
# allsamples <- unique(csv$alias)
for ( r in 1:nrow(csv) ) {
  sample <- paste0(csv[r,"alias"])
  getRun <- append(getRun, paste0(logsDir,"/done/runs/",sample,"-BAM_runSubmission.done"))
}

write.table(getRun, paste0(runsDir,"/Allfiles_list-BAM.txt"), quote=FALSE, row.names=FALSE, col.names=FALSE)
file.create(snakemake@output[['done']])
