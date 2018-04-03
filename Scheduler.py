# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:24:07 2018

@author: Derek DeLizo

Description:
Reads in arugements from the command line then builds a schedule to record audio.
Command format: python Scheduler.py [Schedule] [Start Time] [End Time]

Note:
Script must be run from the command line.

"""

import sys
import schedule
import time
import datetime as dt
import pyaudio
import wave
import copy
from sys import byteorder
from array import array
from struct import pack

THRESHOLD = 500  # audio levels not normalised.
CHUNK_SIZE = 1024
SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
RATE = 1
CHANNELS = 1
TRIM_APPEND = RATE / 4

def record_to_file(stop):
    "Records from the microphone and outputs the resulting data to 'path'"
    today = dt.date.today()
    currTime = dt.datetime.now()
    currTime = dt.time(currTime.hour,currTime.minute)
    path = 'test.wav'
    print ("Path: %s  StopTime: %s" % (path,stop))
    sample_width, data = record(stop)
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record(stop):
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')
    now = dt.datetime.now()
    now = dt.time(now.hour,now.minute)
    stop = stop.split(':')
    stopTime = dt.time(int(stop[0]),int(stop[1]))
    while now != stopTime:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)
        now = dt.datetime.now()
        now = dt.time(now.hour,now.minute)


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

    return copy.deepcopy(data_all[_from:(_to + 1)])

def monday(start,stop):
    schedule.every().monday.at(start).do(record_to_file,stop)

def tuesday(start,stop):
    schedule.every().tuesday.at(start).do(record_to_file,stop)

def wednesday(start,stop):
    schedule.every().wednesday.at(start).do(record_to_file,stop)

def thursday(start,stop):
    schedule.every().thursday.at(start).do(record_to_file,stop)

def friday(start,stop):
    schedule.every().friday.at(start).do(record_to_file,stop)

def saturday(start,stop):
    schedule.every().saturday.at(start).do(record_to_file,stop)

def sunday(start,stop):
    schedule.every().sunday.at(start).do(record_to_file,stop)

def dayTokenizer(newSched):
    x = 0
    day = ''
    scheduleToken = []
    while x < len(newSched):
        day = newSched[x]
        if newSched[x] == 'T':
            if x+1 >= len(newSched):
                day = 'T'
            elif newSched[x+1] == 'h':
                    day = newSched[x] + newSched[x+1]
                    newSched.remove(day[1])
            else:
                    day = newSched[x]

        if newSched[x] == 'S':
            if x+1 >= len(newSched):
                day = 'S'
            elif newSched[x+1] == 'n':
                    day = newSched[x] + newSched[x+1]
                    newSched.remove(day[1])
            else:
                    day = newSched[x]

        scheduleToken.append(day)
        x+=1

    return scheduleToken

def _test():
    '''Module-level testing code.'''
    now = dt.datetime.now()
    stop_m = now.minute
    stop_h = now.hour

    print('Recording...')
    stop = str(stop_h) + ':' + str(stop_m + 1)
    record_to_file(stop)
    print('Recording completed.')

    return 0

_test()

schedules = []
options = {'M':monday,
           'T':tuesday,
           'W':wednesday,
           'Th':thursday,
           'F':friday,
           'S':saturday,
           'Sn':sunday}

commands = sys.argv
newSched = [i for i in commands[1]]
startTime = commands[2]
stopTime = commands[3]

schedDays = dayTokenizer(newSched)

for token in schedDays:
    options[token](startTime,stopTime)

while True:
    schedule.run_pending()
    time.sleep(1)
