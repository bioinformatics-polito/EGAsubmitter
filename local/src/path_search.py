#!/usr/env python

import sys
import os
import glob
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Looks for RNAseq paths and builds a tsv")
    parser.add_argument("-p", "--input_prefix", required=True, 
                        help="Input directory prefix. e.g. /mnt/bioionfotree/prj/RNAseq_biodiversa/local/share/data/shipment_")
    parser.add_argument("-a", "--annot_file", required=True,
                        help="File containing samples' final batch")
    parser.add_argument("-o", "--output_file", required=True,
                        help="Output file")

    parser.add_argument("-b", "--batches", nargs="*", type=int,
                        help="Only consider a number of batches")

    args = parser.parse_args()

    df = pd.read_csv(args.annot_file, sep="\t", header=None)
    # if only some batches should be consideres, filter them in
    if args.batches:
        df = df[df[1].isin(args.batches)]

    outfile = pd.DataFrame(columns=["id", "basename", "path"])
    for idx, row in df.iterrows():
        #dirpath = args.input_prefix + str(row[3])
        fpath = os.path.join(args.input_prefix, "**", row[0]+ "_R1.fastq.gz")
        files = glob.glob(fpath,  recursive=True)
        if not files:
            print("File not found: " + fpath)
        else:
            outfile = outfile.append({"id":row[0], "basename":os.path.basename(files[0]), "path":files[0]}, ignore_index=True)

    outfile.to_csv(args.output_file, sep="\t", index=False, header=None)

if __name__ == "__main__":
    sys.exit(main())