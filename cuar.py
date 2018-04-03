'''
File:           cuar.py

Purpose:        Cloud-Based Underwater Acoustic Recorder is a project with the
                University of Washington Bothell to measure sound pollution in
                Lake Washington. This file is the controller that runs the software
                for the buoy system.

                Based in part on prototype code written by Derek DeLizo

Author:         Ryan Berge

Last Updated:   April 4th, 2018
Version:        0.2
'''

import sys
import configparser
import schedule
import recorder

def monday(start, stop):
    schedule.every().monday.at(start).do(recorder.record_sample, stop)

def tuesday(start, stop):
    schedule.every().tuesday.at(start).do(recorder.record_sample, stop)

def wednesday(start, stop):
    schedule.every().wednesday.at(start).do(recorder.record_sample, stop)

def thursday(start, stop):
    schedule.every().thursday.at(start).do(recorder.record_sample, stop)

def friday(start, stop):
    schedule.every().friday.at(start).do(recorder.record_sample, stop)

def saturday(start, stop):
    schedule.every().saturday.at(start).do(recorder.record_sample, stop)

def sunday(start, stop):
    schedule.every().sunday.at(start).do(recorder.record_sample, stop)

def load_schedule(config: configparser.ConfigParser):
    '''Load a schedule from the configuration file and register it with the scheduler.'''
    schedule_map = {
        'monday' : monday,
        'tuesday' : tuesday,
        'wednesday' : wednesday,
        'thursday' : thursday,
        'friday' : friday,
        'saturday' : saturday,
        'sunday' : sunday
    }

    options = config.options('Schedule')

    for o in options:
        times = config.get('Schedule', o).split(',')
        for t in times:
            time = t.strip(' []')
            pair = time.split(' ')
            start = pair[0]
            stop = pair[1]

            schedule_map[o](start, stop)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 cuar.py [configpath]')
        exit(-1)

    configpath = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(configpath)

    load_schedule(config)

    while True:
        schedule.run_pending()
