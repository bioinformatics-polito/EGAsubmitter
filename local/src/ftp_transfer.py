#!/usr/env python

#####################################################################
#                                                                   #
#   This script opens a connection to the ega-box through ftp and   #
#   transfers encrypted samples.                                    #
#                                                                   #
#####################################################################

import ftplib
import sys, os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Tranfer sample files to ega-box through FTP.")
    parser.add_argument("-i", "--input", help="Input file list", nargs='+')
    parser.add_argument("-c", "--ftp_server", help="FPT server address")
    parser.add_argument("-u", "--username", help="EGA submission username")
    parser.add_argument("-p", "--password", help="EGA submission password")

    args = parser.parse_args()

    try:
        # Open a connection to EGA FTP server
        ftp = ftplib.FTP(args.ftp_server)
        ftp.login(args.username, args.password)

        # Upload files to the FPT server
        for localfile in args.input:
            remotefile = os.path.basename(localfile)
            with open(localfile, "rb") as file:
                ftp.storbinary('STOR %s' % remotefile, file)

        # Print the content of the current directory 
        print("Directory: {}".format(ftp.pwd()))
        ftp.retrlines("LIST")
    
        ftp.quit()
    except ftplib.all_errors as e:
        print(e)

if __name__ == "__main__":
    sys.exit(main())