'''
File:           status.py

Purpose:        asdasd

Author:         Ryan Berge

Last Updated:   June 4th, 2018
Version:        0.2
'''

import Adafruit_MCP9808.MCP9808 as MCP9808
import led
import logger
import gpsutil
import os
import configparser
from azure.storage.blob import BlockBlobService


def upload_status(filename, is_fatal):
    try:
        logger.write('Uploading Status...')

        credential_path = 'credentials.ini'
        credentials = configparser.ConfigParser()
        credentials.read(credential_path)

        username = credentials.get('Azure', 'Username')
        password = credentials.get('Azure', 'Password')

        block_blob_service = BlockBlobService(account_name=username, account_key=password)

        block_blob_service.create_blob_from_path('status', 'status.ini', 'status.ini')

        if is_fatal:
            block_blob_service.create_blob_from_path('status', 'log.txt', 'log.txt')

        return True

    except Exception as e:
        logger.write('Something went wrong when uploading a status file...')
        logger.write(str(e))
        return False


def update_status(is_recording, is_uploading, fatal_error):
    '''
    GPS Coordinates
    Temperature
    IsRecording
    IsUploading
    '''

    latitude = '?'
    longitude = '?'

    try:
        gps_light = led.led(22)
        logger.write('Synchronizing clock with GPS...')
        fix, current_time, latitude, longitude = gpsutil.getGPSInfo()
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
            latitude = '?'
            longitude = '?'
            gps_light.off()
    except Exception as e:
        logger.write('Something with the GPS raised an exception.')
        logger.write(str(e))
        gps_light.off()
        fix = False
        latitude = '?'
        longitude = '?'
        return

    temp = '?'
    try:
        temp_sensor = MCP9808.MCP9808()
        online = temp_sensor.begin()
        if not online:
            temp = '?'
        else:
            temp = temp_sensor.readTempC()
    except Exception as e:
        logger.write('Something with the temperature sensor raised an exception.')
        logger.write(str(e))

    status_file = open('status.ini', 'w')
    status_file.writelines('''[GPS]
Latitude = %s
Longitude = %s

[Temperature]
Celsius = %s

[Status]
IsRecording = %s
IsUploading = %s
FatalError = %s
''' % (str(latitude), str(longitude), temp, str(is_recording), str(is_uploading), str(fatal_error)))

    return 'status.ini'


def _test():
    update_status(False, False, False)
    pass

if __name__ == '__main__':
    _test()
