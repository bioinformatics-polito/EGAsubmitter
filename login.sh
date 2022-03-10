#!/bin/sh


printf "User: "
read user

stty -echo
printf "Password: "
read password
stty echo
printf "\n"

#echo $USER
#echo $PASSWORD

USER=$user PASSWORD=$password snakemake -s local/share/snakerule/Snakefile_login
