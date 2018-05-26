'''
File:           cloud.py

Purpose:        Specifies the functions necessary to communciate with the cloud server

Author:         Ryan Berge

Last Updated:   May 10th, 2018
Version:        0.2
'''

import configparser
import os
import subprocess
import datetime
from azure.storage.blob import BlockBlobService
import time
import logger
import led
import gpsutil

# A simple callback to report the current progress of the upload.
def progressCallback(current, total):
    print("Progress {0}/{1} ({2:.2f}%)".format(current, total, 100*current/total))

def upload_recording(filename: str, config):
    upload_light = led.led(20) # GPIO 20 is the Uploading indicator
    upload_light.on()
    try:
        start = time.time()
        logger.write('Uploading...')

        credential_path = 'credentials.ini'
        credentials = configparser.ConfigParser()
        credentials.read(credential_path)

        container = config.get('Cloud', 'container')

        username = credentials.get('Azure', 'Username')
        password = credentials.get('Azure', 'Password')

        block_blob_service = BlockBlobService(account_name=username, account_key=password)

        # Force chunked uploading and set upload block sizes to 8KB
        block_blob_service.MAX_SINGLE_PUT_SIZE=16
        block_blob_service.MAX_BLOCK_SIZE=8*1024

        timestamp = os.path.basename(filename).split('.')[0]
        extension = os.path.basename(filename).split('.')[1]

        timestamp_day = timestamp.split('_')[1]
        timestamp_time = timestamp.split('_')[2]

        timestamp_day = timestamp_day.replace('-', '_')
        timestamp_time = timestamp_time.replace('-', '_')

        blob_name = timestamp_day + '/' + timestamp_time + '/recording.' + extension

        block_blob_service.create_blob_from_path(container, blob_name, filename)

        end = time.time()
        elapsed = end - start

        logger.write('Upload Succeeded: ' + blob_name)
        logger.write('Upload took ' + str(elapsed) + ' seconds.\n')

        os.remove(filename)

    except Exception as e:
        logger.write('CheckConfig: There was an error uploading to the cloud.')
        logger.write(str(e))
        upload_light.off()
        return

    upload_light.off()
    logger.write('Upload complete')


def check_config():
    gps_light = led.led(23)
    logger.write('Synchronizing clock with GPS...')
    fix, current_time, lattitude, longitude = gpsutil.getGPSInfo()
    if fix == True:
        logger.write('GPS Fix established.')
        gps_light.on()
        try:
            os.system('sudo date -s ' + current_time)
        except Exception as e:
            logger.write(str(e))
        pass
    else:
        logger.write('GPS Fix failed.')
        gps_light.off()

    try:
        logger.write('Cloud: Checking for new configuration.')

        credential_path = 'credentials.ini'
        credentials = configparser.ConfigParser()
        credentials.read(credential_path)

        username = credentials.get('Azure', 'Username')
        password = credentials.get('Azure', 'Password')

        blob_service = BlockBlobService(account_name=username, account_key=password)

        generator = blob_service.list_blobs('configuration')
        for b in generator:
            timestamp = b.properties.last_modified
            break

        # The dumbest bullshit I have ever experienced
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime('config.ini'))
        last_modified = last_modified.replace(tzinfo=datetime.timezone.utc).astimezone(tz=datetime.timezone.utc)
        last_modified += datetime.timedelta(hours=time.altzone / 60 / 60)

        if timestamp > last_modified:
            logger.write('Downloading new configuration.')
            blob_service.get_blob_to_path('configuration', 'config.ini', 'config.ini')
            logger.write('Rebooting...')
            #TODO: Clean-up step
            os.system('reboot')

    except:
        logger.write('CheckConfig: There was an error connecting to the cloud.\n')
        return


def _test():
    config = configparser.ConfigParser()
    config.read('config.ini')
    upload_recording('data/recording_2018-04-11_14-09-00.flac', config)
    # check_config()

if __name__ == '__main__':
    _test()
