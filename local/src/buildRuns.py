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
import json, sys, os

parser = ap.ArgumentParser(description="Build all the Runs object for the samples to upload")
parser.add_argument("-p", "--path", help="Main path to store everything", required=True)
parser.add_argument("-i", "--input", help="Dataframe with the Files provisional IDs", required=True)
parser.add_argument("-j", "--template", help="Path to JSON templates for paired and single runs", required=True)
parser.add_argument("-t", "--type", help="File type given by the user", required=True)
parser.add_argument("-o", "--output", help="Output .csv file name", required=True)
parser.add_argument("-d", "--done", help=".done file", required=True)

args = parser.parse_args()

### Needed paths
mainDir = args.path
metadataDir = os.path.join(mainDir, "user_folder/metadata")
samplesDir = os.path.join(metadataDir, "samples")
runsDir = os.path.join(metadataDir, "runs")

### Load the JSON template
with open(os.path.join(args.template, "RunsTemplate.json")) as j_file:
    template = json.load(j_file)
template['run_file_type'] = args.type

### Load the Files_IDs dataframe
df = pd.read_csv(os.path.join(metadataDir, "Files_IDs.tsv"), sep='\t', usecols=['provisional_id', 'relative_path'])
df['relative_path'] = df['relative_path'].str.strip('/').str.rstrip('.c4gh')

### Load the user-provided samples CSV and ensure correct column order
csv_file = pd.read_csv(os.path.join(metadataDir, "Samples_Information.csv"), sep=',')
csv_file.sort_values(by=['fileName'], axis=0, inplace=True)

### Define the expected column order
expected_order = ["alias", "title", "description", "biological_sex", "subject_id", "phenotype", "biosample_id", 
                  "case_control", "organism_part", "cell_line", "fileName", "filePath", "fileName.bam", "filePath.bam"]
### Validate the columns
if list(csv_file.columns) != expected_order:
    print("The columns of the file must be in the exact order as specified in the template.")
    sys.exit()

### Merge the CSV and IDs dataframes
merged_csv = csv_file.merge(df, left_on='fileName', right_on='relative_path', how='left')

### Create unique set of samples
samples = set(merged_csv['alias'])

### Create JSON files for each sample
for sample in samples:
    sample_data = merged_csv.loc[merged_csv['alias'] == sample]
    template['files'] = sample_data['provisional_id'].tolist()
    ### Write the JSON run file
    with open(os.path.join(runsDir, f"Run_{sample}.json"), 'w') as json_file:
        json.dump(template, json_file, indent=2)

### Drop unnecessary columns and remove duplicates
### These 4 columns were manually added to be used while specific portion of the tool,
    ### but for the creation of the Sample.json they must be removed, because are not recognized by EGA server
merged_csv.drop(columns=['filePath', 'fileName', 'filePath.bam', 'fileName.bam'], inplace=True)
merged_csv.drop_duplicates(subset=['alias'], inplace=True)
### Write the updated samples CSV
merged_csv.to_csv(os.path.join(samplesDir, "SamplesInformation.csv"), index=False)

### Prepare lists for submission
    ### Produces files lists for submission functions. These lists will be used by checkpoints rule in the snakemake workflow
getRun = [os.path.join(runsDir, "IDs", f'Run_{sample}_ID') for sample in samples]
getSample = [os.path.join(samplesDir, "IDs", f'{sample}_ID') for sample in samples]
getJson = [os.path.join(samplesDir, f'{sample}.json') for sample in samples]

### Write file lists for the submission
with open(os.path.join(runsDir, "Allfiles_list.txt"), 'w') as run_file:
    run_file.write('\n'.join(getRun) + '\n')
with open(os.path.join(samplesDir, "Allfiles_list.txt"), 'w') as sample_file:
    sample_file.write('\n'.join(getSample) + '\n')
with open(os.path.join(metadataDir, "AllSamples_list.txt"), 'w') as json_file:
    json_file.write('\n'.join(getJson) + '\n')
