'''
File:           logger.py

Purpose:        Utility to enable easy logging

Author:         Ryan Berge

Last Updated:   May 25th, 2018
Version:        0.2
'''

import datetime

def write(message: str):
    now = datetime.datetime.now()
    print(str(now) + ':  \t' + message)
    try:
        log = open('log.txt', 'a')
        log.write(str(now) + ':  \t' + message + '\n')
        log.close()
        return True
    except:
        return False

def clear():
    print('Clearing log file...')
    try:
        log = open('log.txt', 'w')
        log.write('')
        log.close()
        return True
    except:
        return False

def _test():
    write('hello there')

if __name__ == '__main__':
    _test()
