# Start!

**ATTENTION**: you will need your EGA credentials. If you still do not have them, please contact EGA first (https://ega-archive.org/submission-form.php) to create a profile. Ideally, for each big submission a new account is requested.

Please move in a folder of your choice and clone EGASubmitter repo, with:
$ git clone git@github.com:MaddyPlayer/EGAsubmitter.git
you can specify the name of your project if you want adding yourprojectname after the clone command
$ git clone git@github.com:MaddyPlayer/EGAsubmitter.git yourprojectname
Then, move into the new folder.

If you have already your credentials, please launch
`$ ./login.sh`
and fill your username and password.
In case you close your shell, it crashes, or whatever, or the connection times out (error: “Session timed out”), you will need to re-login with the same command “$ ./login.sh” again.


# Metadata file creation:
First of all, you need to complete is local/share/data/metadata/Samples_Informations.csv: please download it, add all the information you have, paying attention to respect the column order: if you do not have a specific information, please do not delete the column, but leave it blank instead, then reload it with scp/copy.
Some of these are anyway mandatory for a proper submission:
“alias”: that is the samples ID
“title”: that is the title of your project
“description”: that is a short description of your project, or just what these samples are
“fileName”: that is the name of the file related to that sample (.BAM, .fastq, .FASTA, etc)
An easy way to get the filename is to use the command
`$ basename -a *.gz > basename`
inside the folder that contains all the files. (*.gz will get every file that ends with .gz: if you have other .gz files that are not fastq, you should be more specific, like *.fastq.gz)
“filePath”: that is the path where your files are stored
Again, to retrieve this information, use
`$ realpath *.gz > paths`
to save the full path for each file. Again, be more specific in the case you have other .gz files that are not fastq.
Please, be careful that alias, fileName and filePath belong to the same sample.
After you have completed it, please copy it in the dataset/user_folder/metadata folder.


# EGACryptor:
The second step you need to do is to encrypt all your files in order to upload them to the EGA database. You need to have a three-columns file called “Samples_Informations_3cols.tsv” in dataset/user_folder/metadata/, with sample ID, name of the related file (e.g. fastq), and the path where to find this file, like the example you see below. Note that a header is not present.
ABC1234XYZ	ABC1234XYZ_R1.fastq.gz	/where/ever/the/file/is/stored/ABC1234XYZ_R1.fastq.gz
ABC5678XYZ	ABC5678XYZ_R1.fastq.gz	/where/ever/the/file/is/stored/ABC5678XYZ_R1.fastq.gz

How to create Samples_Informations_3cols.tsv? Simply launch $ ./getPaths.sh. It should create the file where it is needed: please, check in dataset/user_folder/metadata/ folder that Samples_Informations_3cols.tsv has been created. If it is not, please use this in the same folder:
$ cat Samples_Informations.csv | tr "," "\t" | cut -f1,17,18 > Samples_Informations_3cols.tsv

Once this file is ready, please launch the command
`$ ./encrypt-upload.sh`
It will ask you the name of your project, or simply the folder where to store encrypted files (dataset/encrypting-uploading/EGACryptor/projectname/), and the number of cores you want to use. Be careful to set a reasonable number :).

If, for any reasons, your transfer stops, please, continue it with the command:
`$ ./transferRecovery.sh`
This should restart the transfer from where it stopped.

**WARNING**: There exists a time window between the data upload and the availability of such files via the Submitter Portal. For this reason, the files can be linked with the samples only a few hours (or overnight to be sure) after the upload. (https://ega-archive.org/submission/FAQ). If you validate or submit your dataset prior this time, they might fail.


# Filling other metadata files (.yaml):
Once you have encrypted and uploaded all your files, and you are waiting for them to be linkable, it is time to fill and submit your metadata.
You already have filled Samples_Informations.csv, so, you should complete all the .yaml files you find in local/share/data/metadata/yamlTemplates folder accordingly. Every file is commented to allow an easier completion: when you find a comment “enums/whatever”, please look a the corresponding file in local/share/data/metadata/enums and fill the .yaml with the tag that better describe the type of your study

enums pick example:
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
This must be done for all the # enums/whatever you will find.

After you have completed all the .yaml files, please copy them in dataset/user_folder/metadata/yaml/ folder.
Pre-Submission:
Once you copied all .yaml files and the .csv with all samples informations, you should be able to launch
`$ . ./metadataSubmission.sh `
It asks you only one last information, that is the type of the files you have transferred: pick the right number from the prompted list.
Note that a backup of the Submission ID is saved in the dataset/user_folder/SubmissionID_backup folder with the current date, in order to allow you to access the submission project in case you need it to modify/delete/whatever the objects you submitted.

Validation:
If the pre-submission part went right, you should go to https://ega-archive.org/submitter-portal/#/ to look at your submission: everything should be signed by a yellow D (DRAFT) in the Status tab, like you see below.

If it is the case, go back on your shell and launch the command:
`$ . ./validation.sh`
It will validate everything you have submitted. After the job is completed, depending on the feedback you get, go back on the page https://ega-archive.org/submitter-portal/#/: you should see a green V (VALIDATED) now. 

If this is the case, you can launch the last job (see Final Submission part). If you see objects with a red VE (VALIDATED_WITH_ERRORS), please look at the error the job gave you, and correct your submission accordingly. The final submission will submit only the objects with the green V


TBA
# Final Submission:






File deletion:
If at any time, you need to delete the files you created, or you want to restart your submission, you can use these commands to delete all the created files.
`$ ./delete_SubmissionMetadata.sh`
It will ask you if you are sure to delete everything, because as I said before, this will restart the whole pipeline.
About the encrypted files, you can use
`$ ./delete_EncryptedFiles.sh`
Again, it will ask you to confirm the action: note that this should be used if you have submitted and validated all your project and you do not need those file anymore, for other purposes.

