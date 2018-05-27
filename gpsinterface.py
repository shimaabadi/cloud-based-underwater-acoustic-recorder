'''
File:           gpsinterface.py
Purpose:        Interfaces with the GSPD daemon and prints GPS info to the
                terminal.
Author:         Jeremy DeHaan
Last Updated:   May 19th, 2018
Version:        1.0
'''

import signal
import gps

class Timeout(Exception):
    pass

def timeout_handler(signum, frame):
        raise Timeout()

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(1)

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

noFix = True
while noFix:
    try:
        report = session.next()

        #when the GPS device is returning information about itself, this is true
        if report['class'] == 'TPV':
            if hasattr(report, 'time') and hasattr(report, 'lat') and hasattr(report, 'lon'):
                print True, report.time, report.lat, report.lon
            else:
                print False, 0, 0, 0
            noFix = False
    except Timeout:
        print False, 0, 0, 0
        noFix = False

