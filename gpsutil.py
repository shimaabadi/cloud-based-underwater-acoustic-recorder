'''
File:           gpsutil.py
Purpose:        Provides a utility function for getting information from the GPS
Author:         Jeremy DeHaan
Last Updated:   May 19th, 2018
Version:        1.0
'''
import subprocess

def getGPSInfo():
    result = subprocess.run(['python2', 'gpsinterface.py'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').split(" ")
    fix = (output[0] == 'True')
    time = output[1]
    latitude = output[2]
    longitude = output[3]

    return (fix, time, latitude, longitude)

