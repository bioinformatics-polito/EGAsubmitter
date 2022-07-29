### #!/usr/bin/env Rscript

df_in <- snakemake@input[[1]]
paths_out <- snakemake@output[['paths']]
names_out <- snakemake@output[['samples']]

path <- paste0(snakemake@params[['path']],"/encrypting-uploading/EGACryptor/")

df <- read.table(df_in, sep=",",header = TRUE)

fn <- df$fileName

all <- data.frame()

for ( name in fn ) {
  all[nrow(all)+1,1] <- paste0(path,name,".gpg")
  all[nrow(all)+1,1] <- paste0(path,name,".gpg.md5")
  all[nrow(all)+1,1] <- paste0(path,name,".md5")
}

write.table(all, names_out,sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)


paths <- as.data.frame(df$filePath)
write.table(paths, paths_out, sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)

file.create(snakemake@output[['done']])
