'''
File:           scheduler.py
Purpose:        Encapsulates the code necessary load a schedule from a configuration
                file and register events.

Authors:        Ryan Berge, Derek DeLizo

Last Updated:   April 23rd, 2018
Version:        0.2
'''

import recorder
import schedule
import configparser

def monday(start, stop):
    print('Scheduler: Adding a recording on Mondays from ', start, ' to ', stop)
    schedule.every().monday.at(start).do(recorder.record_sample, start, stop)

def tuesday(start, stop):
    print('Scheduler: Adding a recording on Tuesdays from ', start, ' to ', stop)
    schedule.every().tuesday.at(start).do(recorder.record_sample, start, stop)

def wednesday(start, stop):
    print('Scheduler: Adding a recording on Wednesdays from ', start, ' to ', stop)
    schedule.every().wednesday.at(start).do(recorder.record_sample, start, stop)

def thursday(start, stop):
    print('Scheduler: Adding a recording on Thursdays from ', start, ' to ', stop)
    schedule.every().thursday.at(start).do(recorder.record_sample, start, stop)

def friday(start, stop):
    print('Scheduler: Adding a recording on Fridays from ', start, ' to ', stop)
    schedule.every().friday.at(start).do(recorder.record_sample, start, stop)

def saturday(start, stop):
    print('Scheduler: Adding a recording on Saturdays from ', start, ' to ', stop)
    schedule.every().saturday.at(start).do(recorder.record_sample, start, stop)

def sunday(start, stop):
    print('Scheduler: Adding a recording on Sundays from ', start, ' to ', stop)
    schedule.every().sunday.at(start).do(recorder.record_sample, start, stop)

def register_config(check_config, config):
    checkin_frequency = config.getint('Cloud', 'checkin_frequency')
    print('Scheduler: Registering config check-in every', checkin_frequency, 'minutes.')
    #TODO: Change to minutes before deployment
    schedule.every(checkin_frequency).seconds.do(check_config)

def load_schedule(config: configparser.ConfigParser, check_config):
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

    print('Loading schedule...')

    options = config.options('Schedule')

    for o in options:
        times = config.get('Schedule', o).split(',')
        for t in times:
            time = t.strip(' []')
            pair = time.split(' ')
            start = pair[0]
            stop = pair[1]

            schedule_map[o](start, stop)

    register_config(check_config, config)

def run_pending():
    schedule.run_pending()
    timestamp = recorder.get_filepath()
    if timestamp != None:
        return timestamp
    else:
        return ''

def _dummy_config_check():
    return

def _test():
    config = configparser.ConfigParser()
    config.read('config.ini')
    load_schedule(config, _dummy_config_check)

if __name__ == '__main__':
    _test()
