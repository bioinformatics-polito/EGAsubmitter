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
# Author: Marco Viviani <marco.viviani@ircc.it>
# Co-Author: Elena Grassi  <elena.grassi@ircc.it>
# ==========================================================================
#                           sftp_transfer.py
# This script opens a connection to the ega-box through sftp
# and transfers encrypted samples files. It can recover stopped uploads.
# ==========================================================================

import argparse
import sys, os
import pysftp

def upload_file(sftp, localfile, remotefile):
    try:
        if sftp.exists(remotefile):
            # If recovery is enabled, check the file size and resume from where it left off
            remote_size = sftp.stat(remotefile).st_size
            local_size = os.path.getsize(localfile)

            if remote_size < local_size:
                print(f"Resuming upload for {localfile} from byte {remote_size}")
                with open(localfile, 'rb') as f:
                    f.seek(remote_size)
                    sftp.putfo(f, remotefile, file_size=local_size, seek=remote_size)
            elif remote_size == local_size:
                print(f"{localfile} already fully uploaded. Skipping.")
                return
        else:
            # No file exists remotely, start from scratch
            print(f"Starting upload for {localfile}")
            sftp.put(localfile, remotefile, confirm=True)
        print(f"Completed upload for {localfile}.")
    except Exception as e:
        print(f"Error uploading {localfile}: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Transfer sample files to EGA box through FTP with recovery.")
    parser.add_argument("-i", "--input", help="Input file list", required=True)
    parser.add_argument("-c", "--ftp_server", help="FTP server address", required=True)
    parser.add_argument("-u", "--username", help="EGA submission username", required=True)
    parser.add_argument("-p", "--password", help="EGA submission password", required=True)
    parser.add_argument("-r", "--recovery", help="Enable recovery for interrupted uploads", action='store_true')
    
    args = parser.parse_args()
    
    paths_to_upload = args.input
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    try:
        # Open the connection to EGA inbox
        with pysftp.Connection(host=args.ftp_server, username=args.username, password=args.password, default_path='/encrypted', cnopts=cnopts) as sftp:
            print(f"Connected to {args.ftp_server} as {args.username}")

            with open(paths_to_upload, 'r') as f:
                for line in f:
                    localfile = line.strip()
                    remotefile = os.path.basename(localfile)
                    if args.recovery:
                        upload_file(sftp, localfile, remotefile)
                    else:
                        print(f"Starting fresh upload for {localfile}")
                        sftp.put(localfile, remotefile, confirm=True)
                        print(f"Completed upload for {localfile}")
                    
    except Exception as e:
        print(f"Transfer failed: {e}")
        return 1
    finally:
        if 'sftp' in locals():
            sftp.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())






# import argparse
# import sys, os
# import pysftp

# def main():
#     parser = argparse.ArgumentParser(description="Tranfer sample files to ega-box through FTP.")
#     parser.add_argument("-i", "--input", help="Input file list")
#     parser.add_argument("-c", "--ftp_server", help="FPT server address")
#     parser.add_argument("-u", "--username", help="EGA submission username")
#     parser.add_argument("-p", "--password", help="EGA submission password")
#     parser.add_argument("-r", "--recovery", help="If specified, restart an aborted upload", action='store_true')
    

#     args = parser.parse_args()
#     paths_to_upload = args.input
#     retval = 0
#     cnopts = pysftp.CnOpts()
#     cnopts.hostkeys = None
#     try:
#         ### Open the connection to EGA inbox
#         with pysftp.Connection(host=args.ftp_server, username=args.username, password=args.password, default_path='/encrypted', cnopts=cnopts) as sftp:
#             print("Welcome user {} to {}".format(args.username,args.ftp_server))
#             with open(paths_to_upload, 'r') as f:
#                 for line in f:
#                     localfile = line.rstrip()
#                     print("Transfering {} ... ".format(localfile), end='')
#                     remotefile = os.path.basename(localfile)
#                     # with open(localfile, "rb") as file:
#                     sftp.put(localfile, confirm=True)
#                     print("complete.")
#         # if args.recovery: ### It will check which file are uploaded already to re-start where it stopped
#         #     ### Retrieve remote files
#         #     remotefiles = ftp.nlst()

#         #     ### Iterate through local files
#         #     with open(paths_to_upload, 'r') as f:
#         #         for line in f:
#         #             localfile = line.rstrip()
#         #             ### Get localfile size
#         #             size_local = os.stat(localfile).st_size 

#         #             remotefile = os.path.basename(localfile)
#         #             ### Check if remotefile exists
#         #             with open(localfile, "rb") as file:
#         #                 if remotefile in remotefiles:
#         #                     ### Check how many bytes have already been uploaded
#         #                     size_remote = ftp.size(remotefile)
#         #                     if size_local > size_remote:
#         #                         print("Resuming transfer of {f} from {s}...".format(f=localfile, s=size_remote), end='')
#         #                         file.seek(size_remote)
#         #                         ftp.storbinary('STOR %s' % remotefile, file, rest=size_remote)
#         #                         print("complete.")
#         #                     else: 
#         #                         print("{f} is ok".format(f=localfile))
#         #                 else:
#         #                     print("Transfering {} ... ".format(localfile), end='')
#         #                     ftp.storbinary('STOR %s' % remotefile, file)
#         #                     print("complete.")

#         # else: ### If recovery is not called, it starts the upload normally
#         #     ### Upload files to the FTP server
#             # with open(paths_to_upload, 'r') as f:
#             #     for line in f:
#             #         localfile = line.rstrip()
#             #         print("Transfering {} ... ".format(localfile), end='')
#             #         remotefile = os.path.basename(localfile)
#             #         with open(localfile, "rb") as file:
#             #             ftp.storbinary('STOR %s' % remotefile, file)
#             #         print("complete.")

#     except Exception as e:
#         print('Error {}'.format(e))
#         retval = 1
#     finally:
#         sftp.close()
#     return retval

# if __name__ == "__main__":
#     sys.exit(main())
