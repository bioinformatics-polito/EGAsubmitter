# ==========================================================================
#                           EGAsubmitter
# ==========================================================================
# This file is part of EGAsubmitter.
#
# EGAsubmitter is Free Software: you can redistribute it and/or modify it
# under the terms found in the LICENSE.rst file distributed
# together with this file.
#
# EGAsubmitter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# ==========================================================================
# Author: Marilisa Montemurro <marilisa.montemurro@polito.it>
# Co-Author: Marco Viviani <marco.viviani@ircc.it>
#            Elena Grassi  <elena.grassi@ircc.it>
# ==========================================================================
#                           ftp_transfer.py
# This script opens a connection to the ega-box through ftp
# and transfers encrypted samples files.
# ==========================================================================

import argparse
import sys, os
import ftplib

def main():
    parser = argparse.ArgumentParser(description="Tranfer sample files to ega-box through FTP.")
    parser.add_argument("-i", "--input", help="Input file list")
    parser.add_argument("-c", "--ftp_server", help="FPT server address")
    parser.add_argument("-u", "--username", help="EGA submission username")
    parser.add_argument("-p", "--password", help="EGA submission password")
    parser.add_argument("-r", "--recovery", help="If specified, restart an aborted upload", action='store_true')
    

    args = parser.parse_args()
    paths_to_upload = args.input
    retval = 0
    try:
        ### Open the connection to EGA FTP server
        ftp = ftplib.FTP(args.ftp_server)
        # print("user={}".format(args.username))#, password={} #, args.password
        ftp.login(args.username, args.password)
        print(ftp.getwelcome())
        if args.recovery: ### It will check which file are uploaded already to re-start where it stopped
            ### Retrieve remote files
            remotefiles = ftp.nlst()

            ### Iterate through local files
            with open(paths_to_upload, 'r') as f:
                for line in f:
                    localfile = line.rstrip()
                    ### Get localfile size
                    size_local = os.stat(localfile).st_size 

                    remotefile = os.path.basename(localfile)
                    ### Check if remotefile exists
                    with open(localfile, "rb") as file:
                        if remotefile in remotefiles:
                            ### Check how many bytes have already been uploaded
                            size_remote = ftp.size(remotefile)
                            if size_local > size_remote:
                                print("Resuming transfer of {f} from {s}...".format(f=localfile, s=size_remote), end='')
                                file.seek(size_remote)
                                ftp.storbinary('STOR %s' % remotefile, file, rest=size_remote)
                                print("complete.")
                            else: 
                                print("{f} is ok".format(f=localfile))
                        else:
                            print("Transfering {} ... ".format(localfile), end='')
                            ftp.storbinary('STOR %s' % remotefile, file)
                            print("complete.")

        else: ### If recovery is not called, it starts the upload normally
            ### Upload files to the FTP server
            with open(paths_to_upload, 'r') as f:
                for line in f:
                    localfile = line.rstrip()
                    print("Transfering {} ... ".format(localfile), end='')
                    remotefile = os.path.basename(localfile)
                    with open(localfile, "rb") as file:
                        ftp.storbinary('STOR %s' % remotefile, file)
                    print("complete.")

    except Exception as e:
        print('Error {}'.format(e))
        retval = 1
    finally:
        ftp.close()
    return retval

if __name__ == "__main__":
    sys.exit(main())
