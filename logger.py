'''
File:           logger.py

Purpose:        Utility to enable easy logging

Author:         Ryan Berge

Last Updated:   May 25th, 2018
Version:        0.2
'''

def write(message: str):
    try:
        log = open('log.txt', 'a')
        log.write(message + '\n')
        log.close()
        return True
    except:
        return False

def clear():
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
