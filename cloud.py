'''
File:           cloud.py

Purpose:        TODO

Author:         Ryan Berge

Last Updated:   April 23rd, 2018
Version:        0.2
'''

import configparser
import os
import subprocess
from azure.storage.blob import BlockBlobService

# A simple callback to report the current progress of the upload.
def progressCallback(current, total):
    print("Progress {0}/{1} ({2:.2f}%)".format(current, total, 100*current/total))

def upload_recording(filename: str, config):
    try:
        print('Uploading...')
        credential_path = 'credentials.ini'
        credentials = configparser.ConfigParser()
        credentials.read(credential_path)

        container = config.get('Cloud', 'container')

        username = credentials.get('Azure', 'Username')
        password = credentials.get('Azure', 'Password')

        block_blob_service = BlockBlobService(account_name=username, account_key=password)
        #block_blob_service.create_blob_from_path('ryanblob2', os.path.basename(filename), filename)

        # Force chunked uploading and set upload block sizes to 8KB
        block_blob_service.MAX_SINGLE_PUT_SIZE=16
        block_blob_service.MAX_BLOCK_SIZE=8*1024

        # Create a temp directory for the 7zip files to go into
        temp_dir = os.path.join(os.getcwd(), "temp")
        temp_path = os.path.join(temp_dir, "upload.7z")

        # The local path to the file
        local_path = os.path.join(os.getcwd(), filename)

        timestamp = os.path.basename(filename).split('.')[0]

        # Run 7zip to split the file into 512KB parts to be uploaded individually
        subprocess.run(["7z", "-v512k", "a", temp_path, local_path])

        # Upload all fileparts into azure blob storage
        for filename in os.listdir(temp_dir):
            zip_path = os.path.join(temp_dir, filename)
            output_path = os.path.join(timestamp, filename)
            block_blob_service.create_blob_from_path(container, output_path, zip_path, None, None, False, progressCallback)

            #remove file after upload
            os.remove(zip_path)

        #remove the temp directory and local file
        os.rmdir(temp_dir)

    except Exception as e:
        print('An exception occurred while uploading the file:')
        print(e)
        return

    print('Upload complete')

def _test():
    config = configparser.ConfigParser()
    config.read('config.ini')
    upload_recording('data/recording_2018-4-22_19-23-0.wav', config)
    pass

if __name__ == '__main__':
    _test()
