'''
File:           gpsutil.py
Purpose:        Provides a utility function for getting information from the GPS
Author:         Jeremy DeHaan
Last Updated:   May 19th, 2018
Version:        1.0
'''
import subprocess
import logger

def getGPSInfo():
    result = subprocess.run(['python2', 'gpsinterface.py'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').split(" ")
    if(len(output) < 4):
        logger.write('That weird GPS bug happened again...')
        logger.write('Output was:' + str(output))
        return False, 0, 0, 0
    fix = (output[0] == 'True')
    time = output[1]
    latitude = output[2]
    longitude = output[3].rstrip()

    return fix, time, latitude, longitude

