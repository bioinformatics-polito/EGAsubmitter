#!/bin/sh


printf "User: "
read user

stty -echo
printf "Password: "
read password
stty echo

printf "\n"

export EGA_USER=$user EGA_PWD=$password

snakemake -f -s local/share/snakerule/Snakefile_login -j1
