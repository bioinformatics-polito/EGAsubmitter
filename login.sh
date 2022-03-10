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

EGA_USER=$user EGA_PWD=$password snakemake -s local/share/snakerule/Snakefile_login
