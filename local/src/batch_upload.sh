#!/usr/bin/bash

BATCH1="5eb3dec9e4ddfe4434335f65/fastq"
BATCH2="5ef5ddec4bcc3bb94bc4d335/fastq"
BATCH3="5efc46814bcc3bb94bc4d344"
PDXBANK="pdxbankrw@pdxbank.polito.it"

if [ $# -ne 3 ]; then
    echo "illegal number of parameters"
fi

if [ $1 == 1 ]; then
    batch=$BATCH1
elif [ $1 == 2 ]; then
    batch=$BATCH2
elif [ $1 == 3 ]; then
    batch=$BATCH3 
else
    echo "Wrong option: " + $1
    exit 1
fi

infile=$2
outpath=$3

#Open the master

SSHSOCKET=~/.ssh/"$PDXBANK"
ssh -M -f -N -o ControlPath=$SSHSOCKET "$PDXBANK"

#Open and close other connections without re-authenticating as you like
dir=$PWD
cd $outpath

echo "Moved to $outpath"
for s in $(awk -v batch=$1 '{if($2 == batch) print $1}'); do 
    #echo $PDXBANK:"/volume1/las_rawdata/$batch/fastq/${s}_R1.fastq.gz - Uploading..."
    scp -o ControlPath=$SSHSOCKET "${PDXBANK}:/volume1/las_rawdata/${batch}/${s}_R1.fastq.gz" . 
    md5sum "$s"_R1.fastq.gz > "$s"_R1.fastq.gz.md5 
done < $infile

cd $dir
echo "Moved to $dir"

#Close the master connection

ssh -S $SSHSOCKET -O exit "$PDXBANK"