# ==========================================================================
#                           EGAsubmitter
# ==========================================================================
# This file is part of EGAsubmitter.
#
# EGAsubmitter is Free Software: you can redistribute it and/or modify it
# under the terms found in the LICENSE.rst file distributed
# together with this file.
#
# EGAsubmitter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# ==========================================================================
# Author: Marco Viviani <marco.viviani@ircc.it>
# ==========================================================================
#                           buildRuns.py
# This script will produce a Run.json for each sample in the .csv file given
# by the user. Moreover, it creates three file lists that will be used
# further on in the pipeline
# ==========================================================================

import argparse as ap
import pandas as pd
import json, glob, sys, os, re
import random

parser = ap.ArgumentParser(description="Build all the Runs object for the samples to upload")
parser.add_argument("-p", "--path", help="Main path to store everything")
parser.add_argument("-i", "--input", help="Dataframe with the Files provisional IDs")
parser.add_argument("-j", "--template", help="Path to json templates for paired and single runs")
parser.add_argument("-t", "--type", help="File type given by the user")
parser.add_argument("-o", "--output", help="Output .csv file name")
parser.add_argument("-d", "--done", help=".done file")

args = parser.parse_args()

mainDir = args.path

### Needed paths
EGACryptor = os.path.join(mainDir,"encrypting-uploading/EGACryptor")
metadataDir = os.path.join(mainDir,"user_folder/metadata")
samplesDir = os.path.join(metadataDir,"samples")
runsDir = os.path.join(metadataDir,"runs")
expsDir = os.path.join(metadataDir,"exps")
jsonTemplate = args.template

j = open(os.path.join(jsonTemplate,"RunsTemplate.json"))
template = json.load(j)

template['run_file_type'] = args.type

df = pd.read_csv(os.path.join(metadataDir,"Files_IDs.tsv"), sep='\t', header=0, usecols=['provisional_id','relative_path']) ### Load the df with the files provisional IDs
df['relative_path'] = df['relative_path'].str.lstrip('/')
df['relative_path'] = df['relative_path'].str.rstrip('.c4gh')

csv = pd.read_csv(os.path.join(metadataDir,"Samples_Information.csv"), sep=',', header=0) ### Load the .csv filled by the user
### The header must follow this order, or EGA will return an error when EGAsubmitter will upload the samples .json file
csv.sort_values(by=['fileName'], axis=0, ascending=True, inplace=True)
rightOrder = ["alias","title","description","biological_sex","subject_id","phenotype","biosample_id","case_control","organism_part","cell_line","fileName","filePath","fileName.bam","filePath.bam"] #,"extra_attributes.tag","extra_attributes.value","extra_attributes.unit"
if ( any(csv.axes[1] != rightOrder) ):
    print("The columns of the file you provide must be in the exact same order we gave in the template.\nPlease, order them accordingly.")
    sys.exit()

csv = csv.merge(df, left_on='fileName', right_on='relative_path', how='left')

samples = set(csv['alias'])

for sample in csv['alias']:
    tmp = csv.loc[csv['alias']==sample]
    template['files'] = tmp['provisional_id'].tolist()
    with open(os.path.join(runsDir,"Run_"+sample+".json"), 'w') as final:
        json.dump(template, final, indent=2)
        
### These 4 columns were manually added to be used while specific portion of the tool, but for the creation of the Sample.json they must be removed, because are not recognized by EGA server
csv = csv.drop(columns=['filePath', 'fileName', 'filePath.bam', 'fileName.bam'])
csv.drop_duplicates(subset=['alias'], keep='first', inplace=True) ### In case there are paired fastq, here I remove one row, cause there should be only one Sample.json per sample.

csv.to_csv(samplesDir+"/SamplesInformation.csv", header=True, index=False)

### produces files lists for submission functions. These lists will be used by checkpoints rule in the snakemake workflow
getRun = [] ### Submitted runs
getSample = [] ### Submitted samples
getJson = [] ### Submitted samples.json

for sample in csv['alias']:
    getRun.append(os.path.join(runsDir,"IDs",'Run_'+sample+"_ID"))
    getJson.append(os.path.join(samplesDir,sample+".json"))
    getSample.append(os.path.join(samplesDir,"IDs",sample+"_ID"))

with open(runsDir+"/Allfiles_list.txt", 'w+') as r:
    for row in getRun:
        r.write(row+'\n')
with open(samplesDir+"/Allfiles_list.txt", 'w+') as s:
    for row in getSample:
        s.write(row+'\n')
with open(metadataDir+"/AllSamples_list.txt", 'w+') as j:
    for row in getJson:
        j.write(row+'\n')

j.close()
