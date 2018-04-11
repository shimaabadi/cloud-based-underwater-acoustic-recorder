'''
File:           cloud.py

Purpose:        TODO

Author:         Ryan Berge

Last Updated:   April 11th, 2018
Version:        0.2
'''

import configparser
import os
from azure.storage.blob import BlockBlobService

def upload_recording(filename: str):
    print('Uploading...')
    configpath = 'credentials.ini'
    config = configparser.ConfigParser()
    config.read(configpath)

    username = config.get('Azure', 'Username')
    password = config.get('Azure', 'Password')

    block_blob_service = BlockBlobService(account_name=username, account_key=password)
    block_blob_service.create_blob_from_path('ryanblob2', os.path.basename(filename), filename)

def _test():
    upload_recording('test.wav')
    pass

if __name__ == '__main__':
    _test()
