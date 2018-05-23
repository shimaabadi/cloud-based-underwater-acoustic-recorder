'''
File:           cuar.py

Purpose:        Cloud-Based Underwater Acoustic Recorder is a project with the
                University of Washington Bothell to measure sound pollution in
                Lake Washington. This file is the controller that runs the software
                for the buoy system.

                Based in part on prototype code written by Derek DeLizo.

Author:         Ryan Berge

Last Updated:   April 6th, 2018
Version:        0.2
'''

import sys
import configparser
import scheduler

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 cuar.py [configpath]')
        exit(-1)

    configpath = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(configpath)

    scheduler.load_schedule(config)

    while True:
        scheduler.run_pending()
