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
    #parser.add_argument("-l", "--log", help="Write log messages to a file")
    parser.add_argument("-r", "--recovery", help="If specified, restart an aborted upload", action='store_true')
    

    args = parser.parse_args()
    retval = 0
    try:
        # Open a connection to EGA FTP server
        ftp = ftplib.FTP(args.ftp_server)
        print("user={}, password={}".format(args.username, args.password))
        ftp.login(args.username, args.password)
        print(ftp.getwelcome())
        if args.recovery:
            #retrieve remote files
            remotefiles = ftp.nlst()

            # Iterate through local files
            for localfile in args.input:
                #get localfile size
                size_local = os.stat(localfile).st_size 

                remotefile = os.path.basename(localfile)
                #check if remotefile exists
                with open(localfile, "rb") as file:
                    if remotefile in remotefiles:
                        #check how many bytes have already been uploaded
                        size_remote = ftp.size(remotefile)
                        if size_local > size_remote:
                            print("Resuming transfer of {f} from {s}...".format(f=localfile, s=size_remote), end='')
                            file.seek(size_remote)
                            ftp.storbinary('STOR %s' % remotefile, file)
                            print("complete.")
                    else:
                        print("Transfering {} ... ".format(localfile), end='')
                        ftp.storbinary('STOR %s' % remotefile, file)
                        print("complete.")

        else:
            # Upload files to the FPT server
            for localfile in args.input:
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

"""
finished = False

local_path = "/local/source/path/file.zip"
remote_path = "/remote/desti/path/file.zip"

with open(local_path, 'rb') as f:
    while (not finished):
        try:
            if ftp is None:
                print("Connecting...")
                ftp = FTP(host, user, passwd)

            if f.tell() > 0:
                rest = ftp.size(remote_path)
                print(f"Resuming transfer from {rest}...")
                f.seek(rest)
            else:
                print("Starting from the beginning...")
                rest = None
            ftp.storbinary(f"STOR {remote_path}", f, rest=rest)
            print("Done")
            finished = True
        except Exception as e:
            ftp = None
            sec = 5
            print(f"Transfer failed: {e}, will retry in {sec} seconds...")
            time.sleep(sec)
"""