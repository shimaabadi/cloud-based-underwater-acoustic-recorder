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

SAMPLING_RATE = 5000
SAMPLING_SIZE = 8

file_timestamp = ''
recording_succeeded = False

def record_sample(start, stop):
    '''Begins recording a sample up to the designated stop time.'''

    print('Beginning recording...')

    try:
        configpath = 'config.ini'
        config = configparser.ConfigParser()
        config.read(configpath)
    except Exception:
        print('There was an error reading the configuration file.')

    global SAMPLING_RATE
    global SAMPLING_SIZE
    SAMPLING_RATE = config.get('Recording', 'sampling_rate')
    SAMPLING_SIZE = config.get('Recording', 'sampling_size')

    now = datetime.datetime.now()
    datestamp = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    timestamp = str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)
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

        os.system('sox -v 0.87 -b '+ SAMPLING_SIZE + ' -r ' + SAMPLING_RATE + ' ' + path + '.wav ' + path + '.flac')
        if os.path.isfile(path + '.flac'):
            os.remove(path + '.wav')
        else:
            print('Recording failed.')
            return

        print('Recording completed.')
        global file_timestamp
        file_timestamp = path + '.flac'
        global recording_succeeded
        recording_succeeded = True

        end = time.time()
        elapsed = end - start

        log = open('log.txt', 'a')
        log.write('Recording at ' + str(start) + ' lasting ' + str(recording_length) + '\n')
        log.write('File conversion took ' + str(elapsed) + ' seconds.\n\n')
        log.close()
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
        print(timestamp)
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
    try:
        os.system('arecord --device=hw:U22,0 --format S32_LE --rate 44100 --channels=2 --duration=' + str(recording_length) + ' ' + path + '.wav')
    except Exception as e:
        print('An error occurred in function recorder::record():')
        print(e)
        return False

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
