'''
File:           recorder.py
Purpose:        Encapsulates the code necessary to record a sample from
                the microphone.

Authors:        Ryan Berge, Derek DeLizo

Last Updated:   May 2nd, 2018
Version:        0.2
'''

import pyaudio
import datetime
import copy
import wave
import os
import configparser
from datetime import datetime
from datetime import time
from sys import byteorder
from array import array
from struct import pack

# TODO: These should probably be saved in the config file
FORMAT = pyaudio.paInt16
SAMPLING_RATE = 5000
CHUNK_SIZE = 1024
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
FRAME_MAX_VALUE = 2 ** 15 - 1
TRIM_APPEND = SAMPLING_RATE / 4
THRESHOLD = 500

file_timestamp = ''
recording_succeeded = False

def record_sample(stop):
    '''Begins recording a sample up to the designated stop time.'''

    print('Beginning recording...')

    try:
        configpath = 'config.ini'
        config = configparser.ConfigParser()
        config.read(configpath)
    except Exception:
        print('There was an error reading the configuration file.')

    global SAMPLING_RATE
    SAMPLING_RATE = config.get('Recording', 'sampling_rate')

    # TODO: Update path to be configurable
    now = datetime.now()
    datestamp = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    timestamp = str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)
    path = 'data/recording_' + datestamp + '_' + timestamp
    print("Path: %s  StopTime: %s" % (path,stop))
    sample_width, data = record(stop)
    data = pack('<' + ('h' * len(data)), *data)

    wf = wave.open(path + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(data)
    wf.close()

    os.system('sox '+ path + '.wav ' + path + '.flac')
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

def record(stop):
    '''
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    '''
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=SAMPLING_RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    r = array('h')
    now = datetime.time(datetime.now())
    stop = stop.split(':')
    stopTime = time(int(stop[0]), int(stop[1]))

    while now < stopTime:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)
        now = datetime.now()
        now = time(now.hour, now.minute)


    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def normalize(data_all):
    """Amplify the volume out to max -1dB"""
    # MAXIMUM = 16384
    normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)
                        / max(abs(i) for i in data_all))

    r = array('h')
    for i in data_all:
        r.append(int(i * normalize_factor))
    return r

def trim(data_all):
    _from = 0
    _to = len(data_all) - 1
    for i, b in enumerate(data_all):
        if abs(b) > THRESHOLD:
            _from = max(0, i - TRIM_APPEND)
            break

    for i, b in enumerate(reversed(data_all)):
        if abs(b) > THRESHOLD:
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
            break

    return copy.deepcopy(data_all[_from : (_to + 1)])

def add_silence(snd_data, seconds):
    '''Add silence to the start and end of 'snd_data' of length 'seconds' (float)'''
    r = array('h', [0 for _ in range(int(seconds * SAMPLING_RATE))])
    r.extend(snd_data)
    r.extend([0 for _ in range(int(seconds * SAMPLING_RATE))])
    return r

def _test():
    '''Module-level testing code.'''
    now = datetime.now()
    stop_m = now.minute
    stop_h = now.hour

    stop = str(stop_h) + ':' + str(stop_m + 1)
    record_sample(stop)

    return 0

if __name__ == '__main__':
    _test()
