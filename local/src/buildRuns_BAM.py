#!/usr/env python

import argparse as ap
import pandas as pd
import json, glob, sys, os

parser = ap.ArgumentParser(description="Build all the Runs object for the samples to upload")
parser.add_argument("-p", "--path", help="Main path to store everything")
parser.add_argument("-j", "--template", help="Path to json templates for paired and single runs")
parser.add_argument("-t", "--type", help="File type given by the user", type=int)
parser.add_argument("-f", "--folder", help="Project folder, where encrypted files are stored")
parser.add_argument("-o", "--output", help="Output .csv file name")
parser.add_argument("-d", "--done", help=".done file")

args = parser.parse_args()

mainDir = args.path
files = args.folder

### Needed paths
EGACryptor = mainDir+"/encrypting-uploading/EGACryptor"
metadataDir = mainDir+"/user_folder/metadata"
samplesDir = metadataDir+"/samples"
runsDir = metadataDir+"/runs"
expsDir = metadataDir+"/exps"
logsDir = mainDir+"/submission/logs"
jsonTemplate = args.template

j = open(jsonTemplate+"/SingleRunsTemplate.json")
template = json.load(j)

template['runFileTypeId'] = 0 # This script is for BAM only 

csv = pd.read_csv(metadataDir+"/Samples_Informations.csv", sep=',', header=0) ### Load the .csv filled by the user
### The header must follow this order, or EGA will return an error when EGAsubmitter will upload the samples .json file
rightOrder = ["alias","title","description","caseOrControlId","genderId","organismPart","cellLine","region","phenotype","subjectId","anonymizedName","bioSampleId","sampleAge","sampleDetail","attributes.tag","attributes.value","fileName","filePath","fileName.bam","filePath.bam"]
if ( any(csv.axes[1] != rightOrder) ):
    print("The columns of the file you provide must be in the exact same order we gave in the template.\nPlease, order them accordingly.")
    sys.exit()

### lists for all checksums' files created during the encryption phase: this will be used later to recover the specific checksum value
gpg = sorted(glob.glob(EGACryptor+"/**/*.gpg.md5", recursive=True))
md5 = [f for f in sorted(glob.glob(EGACryptor+"/**/*.md5", recursive=True)) 
         if not os.path.basename(f).endswith('.gpg.md5')]

for sample in csv['alias']:
    if len(csv.loc[csv['alias']==sample]) != 1:
        print("Something is wrong for sample {}: there are more than one file for it: you inputted single FASTQ. Please, check the csv file you filled".format(sample))
        sys.exit()
    file = csv.loc[csv['alias']==sample, 'fileName'].iloc[0]
    checksum = file+".gpg.md5"
    unencryptedChecksum = file+".md5"
    gpgtmp = list(filter(lambda x:sample in x, gpg))
    md5tmp = list(filter(lambda x:sample in x, md5))
    #if ( !checksum %in% basename(gpgtmp) | !unencryptedChecksum %in% basename(md5tmp) ) {
        #   stop(paste("Sorry, a file from the crypting phase is missing for the sample",sample))
    #}
    template['files'][0]['fileId'] = file
    template['files'][0]['fileName'] = fileName = file+'.gpg'
    with open(gpgtmp[0]) as g:
        line = g.readline().strip('\n')
    template['files'][0]['checksum'] = line
    with open(md5tmp[0]) as g:
        line = g.readline().strip('\n')
    template['files'][0]['unencryptedChecksum'] = line
    with open(runsDir+"/Run_"+sample+".json", 'w') as final:
        json.dump(template, final, indent=2)

### These 4 columns were manually added to be used while specific portion of the tool, but for the creation of the Sample.json they must be removed, because are not recognized by EGA server
csv = csv.drop(columns=['filePath', 'fileName', 'filePath.bam', 'fileName.bam'])

### produces files lists for submission functions. These lists will be used by checkpoints rule in the snakemake workflow
getRun = [] ### Submitted runs

for sample in csv['alias']:
    getRun == getRun.append(logsDir+"/done/runs/"+sample+"-BAM_runSubmission.done")

with open(runsDir+"/Allfiles_list-BAM.txt", 'w+') as r:
    for row in getRun:
        r.write(row+'\n')
        
open(args.done, 'a').close()
j.close()
