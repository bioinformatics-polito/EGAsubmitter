### #!/usr/bin/env Rscript

df_in <- snakemake@input[[1]]
names_out <- snakemake@output[['samples']]
path <- paste0(snakemake@params[[1]],"/")

df <- read.table(df_in, sep=",",header = TRUE)

# fn <- df$alias

all <- data.frame()

for ( n in 1:nrow(df) ) {
  all[nrow(all)+1,1] <- paste0(path,df[n,"alias"],"/",df[n,"fileName"],".gpg")
  all[nrow(all)+1,1] <- paste0(path,df[n,"alias"],"/",df[n,"fileName"],".gpg.md5")
  all[nrow(all)+1,1] <- paste0(path,df[n,"alias"],"/",df[n,"fileName"],".md5")
}

write.table(all, names_out, sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)

file.create(snakemake@output[['done']])
