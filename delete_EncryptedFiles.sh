#!/bin/sh


while true; do
    read -p "Are you sure you want to delete all the encrypted files?
WARNING: If you did not finish the transfer and metadata uploading, you will need to re-encrypt them
" yn
    case $yn in
        [Yy]* ) find dataset/encrypting-uploading/ ! -name *.gitkeep -type f -delete; echo "All files have been deleted"; break;;
        [Nn]* ) exit;;
        * ) echo "Please, answer y|yes or n|no.";;
    esac
done
