'''
File:           upload.py

Purpose:        Defines a function to upload a file to Azure blob storage.
		        This function will internally use 7zip to create a multi-part
		        archive to allow large files to succeed in uploading to the
		        cloud.

Author:         Jeremy DeHaan

Last Updated:   April 11th, 2018
Version:        1.0
'''
import os, uuid, sys, subprocess
from azure.storage.blob import BlockBlobService, PublicAccess

# A simple callback to report the current progress of the upload.
def progressCallback(current, total):
    print("Progress {0}/{1} ({2:.2f}%)".format(current, total, 100*current/total))

# Given these parameters, this function will connect with an Azure blob storage
# and upload the file in small chunks.
#
# It also internaly calls 7zip to split the file into even smaller parts.
def upload(account_name, account_key, container, local_dir, local_file, output_dir):
    try:
        # Connect to Azure and open the container (or create it if it doesn't exist)
        block_blob_service = BlockBlobService(account_name, account_key)

        if block_blob_service.create_container(container):
            block_blob_service.set_container_acl(container, public_access=PublicAccess.Container)

        # Force chunked uploading and set upload block sizes to 8KB
        block_blob_service.MAX_SINGLE_PUT_SIZE=16
        block_blob_service.MAX_BLOCK_SIZE=8*1024

        # Create a temp directory for the 7zip files to go into
        temp_dir = os.path.join(local_dir, "temp")
        temp_path = os.path.join(temp_dir, "upload.7z")

        # The local path to the file
        local_path = os.path.join(local_dir, local_file)

        # Run 7zip to split the file into 512KB parts to be uploaded individually
        subprocess.run(["7z", "-v512k", "a", temp_path, local_path])

        # Upload all fileparts into azure blob storage
        for filename in os.listdir(temp_dir):
            zip_path =os.path.join(temp_dir, filename)
            output_path = os.path.join(output_dir, filename)
            block_blob_service.create_blob_from_path(container, output_path, zip_path, None, None, False, progressCallback)

            #remove file after upload
            os.remove(zip_path)

        #remove the temp directory and local file
        os.rmdir(temp_dir)
        #os.remove(local_path) #is this OK to do?

    except Exception as e:
        print(e)

