#!/bin/sh


while true; do
    read -p "Are you sure you want to delete all files in submission folder?
WARNING: This will restart the whole pipeline: if you still need to upload something do not delete them yet" yn
    case $yn in
        [Yy]* ) find dataset/submission/ ! -name *.gitkeep -type f -delete; echo "All files have been deleted"; break;;
        [Nn]* ) exit;;
        * ) echo "Please, answer y|yes or n|no.";;
    esac
done


while true; do
    read -p "Are you sure you want to delete all files in user_folder folder?
NOTE: Your .csv and .yaml files will not be deleted anyway " yn
    case $yn in
        [Yy]* ) find dataset/user_folder/ ! -name *.yaml ! -name *.gitkeep ! -name *.csv ! -name *.tsv -type f -delete; echo "All files have been deleted"; break;;
        [Nn]* ) exit;;
        * ) echo "Please, answer y|yes or n|no.";;
    esac
done
