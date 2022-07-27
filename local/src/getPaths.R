### #!/usr/bin/env Rscript

df_in <- snakemake@input[[1]]
paths_out <- snakemake@output[['paths']]
names_out <- snakemake@output[['samples']]

df <- read.table(df_in, sep=",",header = TRUE)

fn <- df$fileName

all <- data.frame()

for ( name in fn ) {
  all[nrow(all)+1,1] <- paste0("/scratch/trcanmed/EGAv2/EGAsubmitter/dataset/encrypting-uploading/EGACryptor/",name,".gpg")
  all[nrow(all)+1,1] <- paste0("/scratch/trcanmed/EGAv2/EGAsubmitter/dataset/encrypting-uploading/EGACryptor/",name,".gpg.md5")
  all[nrow(all)+1,1] <- paste0("/scratch/trcanmed/EGAv2/EGAsubmitter/dataset/encrypting-uploading/EGACryptor/",name,".md5")
}

write.table(all, names_out,sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)


paths <- as.data.frame(df$filePath)
write.table(paths, paths_out, sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)
