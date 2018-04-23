'''
File:           cuar.py

Purpose:        Cloud-Based Underwater Acoustic Recorder is a project with the
                University of Washington Bothell to measure sound pollution in
                Lake Washington. This file is the controller that runs the software
                for the buoy system.

                Based in part on prototype code written by Derek DeLizo.

Author:         Ryan Berge

Last Updated:   April 23rd, 2018
Version:        0.2
'''

import configparser
import scheduler
import cloud

if __name__ == '__main__':
    try:
        configpath = 'config.ini'
        config = configparser.ConfigParser()
        config.read(configpath)
    except Exception as e:
        print('There was an error reading the configuration file.')

    scheduler.load_schedule(config)

    while True:
        file = scheduler.run_pending()
        if file != '':
            cloud.upload_recording(file, config)
