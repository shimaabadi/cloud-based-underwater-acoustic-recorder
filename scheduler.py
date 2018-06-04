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
import logger

def monday(start, stop):
    logger.write('Scheduler: Adding a recording on Mondays from ' + str(start) + ' to ' + str(stop))
    schedule.every().monday.at(start).do(recorder.record_sample, start, stop)

def tuesday(start, stop):
    logger.write('Scheduler: Adding a recording on Tuesdays from ' + str(start) + ' to ' + str(stop))
    schedule.every().tuesday.at(start).do(recorder.record_sample, start, stop)

def wednesday(start, stop):
    logger.write('Scheduler: Adding a recording on Wednesdays from ' + str(start) + ' to ' + str(stop))
    schedule.every().wednesday.at(start).do(recorder.record_sample, start, stop)

def thursday(start, stop):
    logger.write('Scheduler: Adding a recording on Thursdays from ' + str(start) + ' to ' + str(stop))
    schedule.every().thursday.at(start).do(recorder.record_sample, start, stop)

def friday(start, stop):
    logger.write('Scheduler: Adding a recording on Fridays from ' + str(start) + ' to ' + str(stop))
    schedule.every().friday.at(start).do(recorder.record_sample, start, stop)

def saturday(start, stop):
    logger.write('Scheduler: Adding a recording on Saturdays from ' + str(start) + ' to ' + str(stop))
    schedule.every().saturday.at(start).do(recorder.record_sample, start, stop)

def sunday(start, stop):
    logger.write('Scheduler: Adding a recording on Sundays from ' + str(start) + ' to ' + str(stop))
    schedule.every().sunday.at(start).do(recorder.record_sample, start, stop)

def register_config(check_config, config):
    checkin_frequency = config.getint('Cloud', 'checkin_frequency')
    logger.write('Scheduler: Registering config check-in every ' + str(checkin_frequency) + ' minutes.')
    #TODO: Change to minutes before deployment
    schedule.every(checkin_frequency).minutes.do(check_config)

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

    logger.write('Loading schedule...')

    options = config.options('Schedule')

    for o in options:
        times = config.get('Schedule', o)
        times = times.replace('"', '')
        times = times.split(',')
        if times[0] == '':
            continue
        for t in times:
            time = t.strip(' []')
            pair = time.split(' ')
            start = pair[0]
            stop = pair[1]

            schedule_map[o](start, stop)

    register_config(check_config, config)
    schedule.every(1).days.do(logger.clear)
    check_config()


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
