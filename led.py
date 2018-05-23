'''
File:           led.py
Purpose:        A class that abstracts the GPIO pins away when using LED's
Author:         Jeremy DeHaan
Last Updated:   May 19th, 2018
Version:        1.0
'''
import RPi.GPIO as GPIO

class led:
    pin = 0
    lit = False
    def __init__(self, pinNumber):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pin = pinNumber
        GPIO.setup(self.pin,GPIO.OUT)

    def on(self):
        self.lit = True
        GPIO.output(self.pin,GPIO.HIGH)

    def off(self):
        self.lit = False
        GPIO.output(self.pin,GPIO.LOW)

    def flip(self):
        GPIO.output(self.pin,GPIO.LOW) if self.lit else GPIO.output(self.pin,GPIO.HIGH)
        self.lit = not self.lit

