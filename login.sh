#!/bin/sh

stty -echo

printf "User: "
read user

printf "Password: "
read password

stty echo

printf "\n"

EGA_USER=$user EGA_PWD=$password 
snakemake -f -s local/share/snakerule/Snakefile_login
