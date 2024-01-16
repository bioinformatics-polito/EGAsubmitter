# Start!


### WARNING ###
EGA has changed the API and all the json structures :S
I have updated everything to match the new structure, but the recovery of the upload is still not available.
Regarding all the rest, EGAsubmitter is working!
I am sorry for the inconvenience.

**ATTENTION**: you will need EGA credentials. If you still do not have them, please contact EGA first (https://ega-archive.org/submission-form.php) to create a profile. Ideally, for each big submission a new account is requested (EGA enforces a limit of 10Tb per submission account at any one time). If you have your credentials already, please continue!  
EGA works on two profiles, both linked to the same email you provided:  
The first is the one with the username "ega-box-xxxx": this is the one you will use to manage all the submissions, and these only, and to login to the [EGA's Submitter portal](https://submission.ega-archive.org/) and in EGAsubmitter (see below).
The second uses the email as username, and it is the one to manage everything related to your profile, like the management of DACs and policies in the [DAC portal](https://dac.ega-archive.org/). Here you must create a DAC, giving a title (the name to recognize it later) and wait for it to be accepted by EGA (usually a couple of working days). After that, you need to create a policy to link to the DAC. Again, give the policy a name (title) and write the content. Moreover, you will need to select a specific DUO code, based on the data type you want to submit, to be linked to the policy. Both DAC and policy can be used for different submissions.

Please move in a folder of your choice and clone EGASubmitter repo, with:  
`$ git clone https://github.com/bioinformatics-polito/EGAsubmitter.git`  
you can specify the name of your project if you want, adding *yourprojectname* after the clone command  
`$ git clone https://github.com/bioinformatics-polito/EGAsubmitter.git yourprojectname`  
Then, move into the new folder. Inside it, you will find a file named “*EGAsubmitter.yml*”: this is the environment to install with conda in order to have all the needed packages.  
This can be done using `$ conda env create -f EGAsubmitter.yml` (solving environment can take a few minutes, please be patient). Then activate it with `$ conda activate EGAsubmitter`.  
Now, the fun can begin!

# Metadata file creation:
First of all, what you need to complete is local/share/data/metadata/Samples_Information.csv: please download it, add all the information you have, paying attention to respect the column order: if you do not have a specific information, please do not delete the column, but leave it blank instead (or use "unknown" where it is not asked otherwise), then reload it with scp/copy in dataset/user_folder/metadata/ with the same file name.
In the same folder you can find a file that shows what to write in each column, and an example of a filled file. Note that the path should have the file included as well.
**ATTENTION**: if you want to upload **both** FASTQ and BAM, use the last two columns for .bam files information ("fileName.bam", "filePath.bam"), filling them accordingly. If you are submitting **only** BAM, use the normal ones ("fileName", "filePath"). *"fileName.bam" and "filePath.bam" columns must be used **only** in the first case.*  

**Before uploading your files please make sure that any files that will be uploaded to EGA do not use special characters in their naming convention such as # ? ( ) [ ] / \ = + < > : ; " ' , * ^ | &. This can cause issues with the archiving process, leading to problems for end users.**

***
**TIP**  
An easy way to get the filename in command line is  
`$ basename -a *.gz > basename`  
inside the folder that contains all the files. (*.gz will get every file that ends with .gz: if you have other .gz files that are not fastq, you should be more specific, like *.fastq.gz)
For filepaths instead, you can use  
`$ realpath *.gz > paths`  
to save the full path for each file. Again, be more specific in the case you have other .gz files that are not fastq, or that end with other extensions type.  
**Please, be careful that alias, fileName and filePath belong to the same sample.**  
After you have completed it, please copy it in the *dataset/user_folder/metadata* folder.  
***

# Crypt4GH:
The second step you need to do is to encrypt all your files in order to upload them to the EGA database. You need to have a three-columns file called “Samples_Information_3cols.tsv” in dataset/user_folder/metadata/, with sample ID, name of the related file, and the path where to find this file. All these information will be automatically taken by the .csv file you filled before, so please launch  
`$ ./getPaths.sh`  
Because EGAsubmitter can manage the upload of both FASTQ and BAM files of the same experiment, it needs some information about what you are going to do.
```
Is this the second phase of encryption for .bam files, AFTER .fastq?
Answer "yes" if you encrypted and uploaded .fastq files already and you want to encrypt/upload .bam.
Answer "no" to encrypt and upload other files for the first time
```
if this run you are doing is the first, please answer "no". In case you want to upload **both** FASTQ and BAM files of the same experiment, and you have uploaded .fastq **already**, please answer "yes".

After this, you can login using your credentials. In the main folder, launch the command  
`$ source ./login.sh`  
and fill your username (ega-box-xxxx) and password.  
In case you close your shell, it crashes, or the connection times out (error: “Session timed out”), you will need to re-login with the same command `$ source ./login.sh` again.  

Once the .csv file is ready, please launch the command  
`$ ./encrypt-upload.sh`  
It will ask you the name of your project, or simply the folder where to store encrypted files (dataset/encrypting-uploading/crypt4GH/*yourprojectname*/), and the number of cores you want to use. Depending on what machine you are working, be careful to set a reasonable number :-).  
We suggest to use different folders for different files type, if you have more than one.  

If the encryption stops, please use `$ ./encrypt-upload.sh` again.  
**Unfortunately, after the structure has been changed by EGA, I still was not able to re-implement the recovery of the upload if it stops. Therefore, if it does, you will need to restart it from 0. I advise you to start it in a bash screen to reduce risks. I am sorry for this drawback: I will fix this asap.**

# Filling other metadata files (.yaml):
Once you have encrypted and uploaded all your files, it is time to fill and submit your metadata.  
You already have filled Samples_Information.csv, so, you need to complete all the .yaml files you find in local/share/data/metadata/yamlTemplates folder accordingly. Every file is commented to allow an easier completion: when you find a comment “*local/share/data/metadata/enums/whatever*”, please look at *local/share/data/metadata/enums/{WHAT}_.txt* and fill it with the line that better describe the type of your study

**enums pick example:**
you are completing local/share/data/metadata/yamlTemplates/Study.yaml  
This is the Study.yaml file

```yaml
title: ''  # REQUIRED - The title of your work. (string)
description: '' # REQUIRED - Description of your work. (string)
study_type: '' # REQUIRED - local/share/data/metadata/enums/study_types.txt (string)
pubmed_ids: [] # Not required - The pubmed ID if you have it already (array integer)
custom_tags: [''] # Not required - MONDO tag if you have one already [MONDO:XXXXXX] (array string)
### If you have 'extra_attributes' or 'repositories' information, please uncomment these following lines accordingly
# extra_attributes: # Not required
#   - tag: '' # (string)
#     value: '' # (string)
#     unit: '' # (string)
# repositories: # Not required
#   - repository_id: '' # (string)
#     url: '' # (string)
#     label: '' # (string)
```

To correctly complete the "*study_type*" field, you need to go to local/share/data/metadata/enums/study_types.txt and pick the right type.  
These "enums" are always mandatory information: you must fill all lines commented with “*local/share/data/metadata/enums/whatever*” you will find in .yaml files.
*It is possible that there is not a type that perfectly recalls what the user is going to submit, but the one that best describes the protocol shall be picked.*

After you have completed all the .yaml files, please copy them in *dataset/user_folder/metadata/yaml/* folder.  

# Pre-Submission:
Once you copied all .yaml files and the .csv with all samples information, you should be able to launch  
`$ ./metadataSubmission.sh `  
It asks you only one last information, that is the type of the files you have transferred: pick the right type from the prompted list.  
Note that a backup of the Submission ID is saved in the dataset/user_folder/SubmissionID_backup folder with the current date, in order to allow you to access the submission project in case you need it to modify/delete/whatever the objects you submitted.  
The pipeline will start, creating all the .json objects needed and uploading them automatically to EGA. You can follow the pipeline on the terminal or directly on  
*https://submission.ega-archive.org/*: here you will see appear the different object gradually.  
If, for any reason, the pipeline stops, just launch again `$ ./metadataSubmission.sh `; the pipeline will start from where it stopped. The pipeline is structured to ease the own fix if an error occurs, thanks also to saved logs for each step, but feel free to contact me for any question. 

# Adding .BAM files
If you want to upload BAM files as well, after you uploaded the FASTQ you need to launch again `$ ./getPaths.sh` and answer *yes* to the question. Samples_information_3cols.tsv files should slighty change, keeping now the "fileName.bam" and "filePath.bam" columns from .csv file.  
Now launch again `$ ./encrypt-upload.sh`, specifying a different project folder. Like for .fastq, .bam files will be encrypted and uploaded automatically :-)  
To upload encrypted files metadata, launch `$ ./BAMsubmission.sh`. When it ends, you should have both .fastq and .bam uploaded.  

# Finalisation:
If the pre-submission part went right, you should go to the [EGA submitter portal](https://submission.ega-archive.org/) to look at your submission: everything should be present: you can look at it to see that everything has been correctly submitted.  
If so, click on the green "FINALISE" button (top right). You can again check everything, then you need to pick an expected release date and confirm everything with the "FINALISE SUBMISSION" button. Note that, in case of big files, the link between them and the metadata could take some time (it is done by EGA itself), so you could need to wait some time that everything is linked, and then go for the finalization. Anyway, in case, an error will prompt after you hit "FINALISE".
Now EGA will check it and admit or refuse: if EGA will reject your submission, a message icon will appear near the main title. Clicking on it will reveal the message with the problems the Helpdesk encountered, asking you to correct them. In case the message is not clear enough, you can write to the [EGA helpdesk](helpdesk@ega-archive.org) to ask further instruction.

# How to get EGA assigned ID back:
After the final submission and the approval by EGA, EGA assigns a specific ID to each identity:
```
EGA: EGA Submission ID  
EGAS: EGA Study Accession ID  
EGAN: EGA Sample Accession ID  
EGAR: EGA Run Accession ID  
EGAX: EGA Experiment ID  
EGAD: EGA Dataset Accession ID  
EGAF: EGA File Unique Accession ID
```  
These can be useful to have in case of dataset publication, and EGAsubmitter can retrieve them for you! Just launch  
`$ ./getEGAIDs.sh` while you are logged in, and prompt the EGA submission ID that you can find in the "id" column of the page "My Submissions", or in the url bar after clicking on the submission (e.g.: https://submission.ega-archive.org/submissions/**EGA00000000000**): the tool will download all the information and convert them to tab separated files in  
*dataset/submission/EGASTORE/*

# File deletion:
If at any time, you need to delete the files you created, or you want to restart your submission, you can use these commands to delete all the created files.  
`$ ./delete_SubmissionMetadata.sh`  
It will ask you if you are sure to delete everything, because as it has been said before, this will restart the whole pipeline. However, filled .csv and .yaml files will not be deleted.  
About the encrypted files, you can use  
`$ ./delete_EncryptedFiles.sh`  
Again, it will ask you to confirm the action: note that this should be used if you have submitted and validated all your project and you do not need those file anymore, for other purposes.
***
***
# Testing the code
We implemented a minimum working example of metadata and sequencing files to allow users to try the code before proceeding with their datasets/before creating EGA credentials
to access EGA servers. 
The `dry-run` scripts provided run all the code that can run without interacting with EGA: they encrypt the files and create the required .gpg to check them, then they
convert all yaml files to json and perform all the metadata setup steps, then they stop as soon as an answer from EGA API is required (the entities IDs required
to link them correctly). They also check that the correct number of files (and lines in intermediate rules inputs) are created.
These are the instructions to test the code in this way from scratch:

```
git clone https://github.com/bioinformatics-polito/EGAsubmitter.git
cd EGAsubmitter
# creating the conda env can take a few minutes;
# we limited version limits as much as possible but had to keep some of them
conda env create -f EGAsubmitter.yml
conda activate EGAsubmitter
# to test single-end FASTQ process copy the dummy csv to the user folder metadata
cp local/share/data/dummy/Samples_Information.csv dataset/user_folder/metadata/
# create other supporting files and setup mode 
# (bam after fastq or uploading a single kind of files)
# answer "no" for testing.
./getPaths.sh
# encrypt only your files using the dummy script, skip login.sh
# Input a name for the test and the wanted number of cores
./encrypt-upload_DUMMY.sh
# This should show two different passed tests.
# copy dummy yamls to the correct directory:
cp local/share/data/dummy/yaml/* dataset/user_folder/metadata/yaml/
# repeat the same name as before for your test and choose 4 for
# single-ended FASTQ files, 5 for paired-end ones.
./metadataSubmission_DUMMY.sh
# This should show three different passed tests.
```
***

# Appendix

Here you can find a table that explain what each command does:
|  COMMAND  |  DOES  |
|:----:|:----:|
getPaths.sh | Retrieves a three-columns file from your filled .csv
login.sh | Logs in your EGA account, where everything will be submitted
encrypt-upload.sh | Starts the encryption of your files and starts to upload them to your ega-box
transferRecovery.sh | Recovers your stopped *transfer*
metadataSubmission.sh | Links and submits EGA entities
BAMsubmission.sh | Submits BAM files *only after* FASTQ
getEGAIDs.sh | Retrieves EGA spcific ID *after* the final submission
delete_SubmissionMetadata.sh | Deletes all the files created in the metadata submission
delete_EncryptedFiles.sh | Deletes all the encrypted files
