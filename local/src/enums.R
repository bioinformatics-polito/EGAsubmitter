### tbh this script is not needed anymore, we can remove it completely

library(jsonlite)

json <- fromJSON(snakemake@input[[1]])
output <- snakemake@output[[1]]

assoc <- as.data.frame(cbind(json[["response"]][["result"]][["tag"]], json[["response"]][["result"]][["value"]]), stringsAsFactors = FALSE)
names(assoc) <- c("tag","value")
assoc$tag <- as.numeric(assoc$tag)
assoc <- assoc[order(assoc$tag),]

write.table(assoc, output, quote=FALSE, sep='\t', row.names=FALSE, col.names=TRUE)
