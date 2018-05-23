'''
File:           scheduler.py
Purpose:        Encapsulates the code necessary load a schedule from a configuration
                file and register events.

Authors:        Ryan Berge, Derek DeLizo

Last Updated:   April 6th, 2018
Version:        0.2
'''

import recorder
import schedule
import configparser

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
    '''Load a schedule from a configuration file and register it with the scheduler.'''
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

def run_pending():
    schedule.run_pending()

def _test():
    pass

if __name__ == '__main__':
    _test()
