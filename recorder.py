'''
File:           recorder.py
Purpose:        Encapsulates the code necessary to record a sample from
                the microphone.

Authors:        Ryan Berge

Last Updated:   May 9th, 2018
Version:        0.2
'''

import datetime
import copy
import wave
import os
import configparser
import time
from sys import byteorder
from array import array
from struct import pack
import logger
import led

SAMPLING_RATE = 5000
SAMPLING_SIZE = 8

file_timestamp = ''
recording_succeeded = False

def record_sample(start, stop):
    '''Begins recording a sample up to the designated stop time.'''

    logger.write('Beginning recording...')


    try:
        configpath = 'config.ini'
        config = configparser.ConfigParser()
        config.read(configpath)
    except Exception as e:
        logger.write('There was an error reading the configuration file:')
        logger.write(str(e))

    global SAMPLING_RATE
    global SAMPLING_SIZE
    SAMPLING_RATE = config.get('Recording', 'sampling_rate')
    SAMPLING_SIZE = config.get('Recording', 'sampling_size')

    now = datetime.datetime.now()
    datestamp = str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2)
    timestamp = str(now.hour).zfill(2) + '-' + str(now.minute).zfill(2) + '-' + str(now.second).zfill(2)
    path = 'data/recording_' + datestamp + '_' + timestamp
    print("Path: %s  StopTime: %s" % (path,stop))

    start = start.split(':')
    stop = stop.split(':')

    start = datetime.time(int(start[0]), int(start[1]))
    stop = datetime.time(int(stop[0]), int(stop[1]))

    # Note: This could produce errors for recordings over 1 hour in length
    recording_length = stop.minute - start.minute
    if recording_length < 0:
        recording_length += 60

    # Convert from minutes to seconds
    recording_length *= 60

    success = record(recording_length, path)

    if success:
        start = time.time()

        os.system('sox ' + path + '.wav ' + '-b '+ str(SAMPLING_SIZE) + ' -r ' + str(SAMPLING_RATE) + ' ' + path + '.flac')
        if os.path.isfile(path + '.flac'):
            os.remove(path + '.wav')
        else:
            logger.write('There was an error converting the file.')
            return

        logger.write('Recording completed.')
        global file_timestamp
        file_timestamp = path + '.flac'
        global recording_succeeded
        recording_succeeded = True

        end = time.time()
        elapsed = end - start

        logger.write('Recording at ' + str(start) + ' lasting ' + str(recording_length))
        logger.write('File conversion took ' + str(elapsed) + ' seconds.\n')
    else:
        recording_succeeded = False
        file_timestamp = ''

def get_filepath():
    global file_timestamp
    global recording_succeeded
    if recording_succeeded:
        timestamp = file_timestamp
        file_timestamp = ''
        recording_succeeded = False
        return timestamp
    else:
        file_timestamp = ''
        recording_succeeded = False
        return None

def record(recording_length, path):
    '''
    Perform a recording of the designated length and save it to the designated path.
    Returns true if the recording succeeds and false if there is an exception thrown.
    '''
    recording_light = led.led(16) # GPIO 16 = Recording LED
    recording_light.on()
    try:
        os.system('arecord --device=hw:U22,0 --format S32_LE --rate 44100 --channels=2 --duration=' + str(recording_length) + ' ' + path + '.wav')
    except Exception as e:
        logger.write('An error occurred while recording.')
        logger.write(str(e))
        recording_light.off()
        return False

    recording_light.off()
    return True


def _test():
    '''Module-level testing code.'''
    now = datetime.datetime.now()
    t_m = now.minute
    t_h = now.hour

    start = str(t_h) + ':' + str(t_m)
    stop = str(t_h) + ':' + str(t_m + 1)

    record_sample(start, stop)

    return 0

if __name__ == '__main__':
    _test()
