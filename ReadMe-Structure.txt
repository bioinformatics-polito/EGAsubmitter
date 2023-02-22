                # ==========================================================================#
                #                           EGAsubmitter structure                          #
                # ==========================================================================#

In the main folder you can find all the shell script to launch the different steps of the pipeline,
together with the conda environment file (EGAsubmitter.yml) to install all the dipendencies needed to run the 
tool correctly, the license to use this software, and the README.md where it is extensively described.

In the local/ folder are stored all the scripts (src/ and bin/) and Snakefile (snakerule/) used in the processes.
All Snakefiles include paths and functions from two main configuration files, stored in snakemake/ folder.
Moreover, local/share/data are present all the templates (.csv and .yaml files) to be filled with metadata and samples information.

In the dataset/ folder will be stored all the files that EGAsubmitter will produce and submit to EGA, like encrypted files,
modified json, etc.
