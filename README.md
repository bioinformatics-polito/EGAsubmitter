# Start!

**ATTENTION**: you will need EGA credentials. If you still do not have them, please contact EGA first (https://ega-archive.org/submission-form.php) to create a profile. Ideally, for each big submission a new account is requested.

Please move in a folder of your choice and clone EGASubmitter repo, with:  
`$ git clone git@github.com:MaddyPlayer/EGAsubmitter.git`  
you can specify the name of your project if you want, adding *yourprojectname* after the clone command  
`$ git clone git@github.com:MaddyPlayer/EGAsubmitter.git yourprojectname`  
Then, move into the new folder.

If you have already your credentials, please continue!  

# Metadata file creation:
First of all, you need to complete is local/share/data/metadata/Samples_Informations.csv: please download it, add all the information you have, paying attention to respect the column order: if you do not have a specific information, please do not delete the column, but leave it blank instead (or use "unknown" where it is not asked otherwise), then reload it with scp/copy.
In the same folder you can find a file that shows what to write in each column, and an example.
**ATTENTION**: if you want to upload **both** .fastq and .bam, use the last two columns for .bam files information ("fileName.bam", "filePath.bam"), filling them accordingly. If not, use the normal ones ("fileName", "filePath") for .bam as well.

**TIP**
An easy way to get the filename is to use the command  
`$ basename -a *.gz > basename`  
inside the folder that contains all the files. (*.gz will get every file that ends with .gz: if you have other .gz files that are not fastq, you should be more specific, like *.fastq.gz)
For filepaths instead, you can use  
`$ realpath *.gz > paths`  
to save the full path for each file. Again, be more specific in the case you have other .gz files that are not fastq, or that end with other extensions type.  
Please, be careful that alias, fileName and filePath belong to the same sample.  
After you have completed it, please copy it in the *dataset/user_folder/metadata* folder.  

After this, you can login using your credentials. Launch the command in the main folder.  
`$ ./login.sh`  
and fill your username and password.  
In case you close your shell, it crashes, or whatever, or the connection times out (error: “Session timed out”), you will need to re-login with the same command `$ ./login.sh` again.  

# EGACryptor:
The second step you need to do is to encrypt all your files in order to upload them to the EGA database. You need to have a three-columns file called “Samples_Informations_3cols.tsv” in dataset/user_folder/metadata/, with sample ID, name of the related file, and the path where to find this file. All these information will be automatically taken by the .csv file you filled before, so please launch  
`$ ./getPaths.sh`  
It will ask you what you are going to do: if this run you are doing is the first, please answer "no". In case you want to upload **both** fastq and bam files, and you have uploaded .fastq already, please answer "yes". Either way, it should create the file where it is needed: please, check in *dataset/user_folder/metadata/* folder that Samples_Informations_3cols.tsv has been created. If it has not, please use this command in the same folder:  
`$ cat Samples_Informations.csv | tr "," "\t" | cut -f1,17,18 > Samples_Informations_3cols.tsv` for the first round  
`$ cat Samples_Informations.csv | tr "," "\t" | cut -f1,19,20 > Samples_Informations_3cols.tsv` to upload .bam files **after** .fastq.  

Once the file is ready, please launch the command  
`$ ./encrypt-upload.sh`  
It will ask you the name of your project, or simply the folder where to store encrypted files (dataset/encrypting-uploading/EGACryptor/*yourprojectname*/), and the number of cores you want to use. Be careful to set a reasonable number :-).  
We suggest to use different folders for different files type, if you have more than one.  

If, for any reasons, your transfer stops, please, continue it with the command:  
`$ ./transferRecovery.sh`  
This should restart the transfer from where it stopped.  

**WARNING**: There exists a time window between the data upload and the availability of such files via the Submitter Portal. For this reason, the files can be linked with the samples only a few hours (or overnight to be sure) after the upload. (https://ega-archive.org/submission/FAQ). If you validate or submit your dataset prior this time, it might fail.
If you want to upload more than one file type (e.g. fastq + bam), we suggest to do the encryption/upload of every file first, in order to no waste too much time waiting for files to be available (see below "Adding .BAM files").  
You can upload metadata anyway (see belowe), just do not try to validate them before enough time has passed.

# Filling other metadata files (.yaml):
Once you have encrypted and uploaded all your files, and you are waiting for them to be linkable, it is time to fill and submit your metadata.  
You already have filled Samples_Informations.csv, so, you should complete all the .yaml files you find in local/share/data/metadata/yamlTemplates folder accordingly (but Analysis.yaml). Every file is commented to allow an easier completion: when you find a comment “*enums/whatever*”, please look a the corresponding file in *local/share/data/metadata/enums* and fill the .yaml with the tag that better describe the type of your study

**enums pick example:**
you are completing local/share/data/metadata/yamlTemplates/Study.yaml  
This is the Study.yaml file

```
alias: '' # Given by EGA when uploaded
studyTypeId: '' # enums/study_type
shortName: '' # Not required
title: ''  # The title of your work: same for every "title"
studyAbstract: ''
ownTerm: '' # Not required
pubMedIds: [] # Not required
customTags: # Not required
 - tag: ''
   value: ''
```

To correctly complete the studyTypeId field, you need to go to local/share/data/metadata/enums/study_types_association_list.txt and pick the right tag. Are you submitting RNASeq data? use the tag 10; is it a Whole Genome Sequencing? tag 0. And so on.  
These "enums" are mandatory information: you must fill all the # enums/whatever you will find in .yaml files.  

After you have completed all the .yaml files, please copy them in *dataset/user_folder/metadata/yaml/* folder.  

# Pre-Submission:
Once you copied all .yaml files and the .csv with all samples informations, you should be able to launch  
`$ ./metadataSubmission.sh `  
It asks you only one last information, that is the type of the files you have transferred: pick the right number from the prompted list.  
Note that a backup of the Submission ID is saved in the dataset/user_folder/SubmissionID_backup folder with the current date, in order to allow you to access the submission project in case you need it to modify/delete/whatever the objects you submitted.  
The pipeline will start, creating all the .json objects needed and uploading them automatically to EGA. You can follow the pipeline on the terminal or directly on  
*https://ega-archive.org/submitter-portal/#/login*  
If, for any reason, the pipeline stops, just launch again `$ ./metadataSubmission.sh `; the pipeline will start from where it stopped.  

# Adding .BAM files
If you want to upload .bam files as well, after you uploaded .fastq you need to launch again `$ ./getPaths.sh` and answer *yes* to the question. Samples_Informations_3cols.tsv files should slighty change, keeping now the "fileName.bam" and "filePath.bam" columns from .csv file.  
Now launch again `$ ./encrypt-upload.sh`, specifying a different project folder. Like for .fastq, .bam files will be encrypted and uploaded automatically :-)  
To upload encrypted files metadata, launch `$ ./BAMsubmission.sh`. When it ends, you should have both .fastq and .bam uploaded.  

# Validation:
If the pre-submission part went right, you should go to https://ega-archive.org/submitter-portal/#/ to look at your submission: everything should be signed by a yellow D (DRAFT) in the Status tab.
You should be able to validate using the green check that appears when you hover your cursor on the submission in the main page. Click on it and wait the needed time: a window prompt will tell you whether the validation was succesful or not (usually "validated with errors).  
If the whole validation went right you should see a green V (VALIDATED) now beside the submission, and you can procede with the submission. If the validation had some errors, go in the submission, and click on "Submission errors console". This will give you the list of all the happened errors during validation (same if the final submission fails). Look at the errors and try to solve them, then repeat the validation/submission.


# File deletion:
If at any time, you need to delete the files you created, or you want to restart your submission, you can use these commands to delete all the created files.  
`$ ./delete_SubmissionMetadata.sh`  
It will ask you if you are sure to delete everything, because as it has been said before, this will restart the whole pipeline. However, filled .csv and .yaml files will not be deleted.  
About the encrypted files, you can use  
`$ ./delete_EncryptedFiles.sh`  
Again, it will ask you to confirm the action: note that this should be used if you have submitted and validated all your project and you do not need those file anymore, for other purposes.
