#!/usr/bin/env python3
__description__ = \
"""
Driver for GPIO LED array.
"""
__author__ = "Michael J. Harms"
__date__ = "2018-11-12"

from .base import LED

from RPi import GPIO
GPIO.setmode(GPIO.BCM)

class GPIO(LED):

    def __init__(self,pin_numbers):

        self._pin_numbers = pin_numbers[:]
        if len(self._pin_numbers) != 3:
            err = "GPIO LEDs require three GPIO pins.\n"
            raise ValueError(err)

        # Configure GPIO pins
        self._pins = []
        for pin in self._pin_numbers:
            GPIO.setup(pin,GPIO.OUT)
            self._pins.append(GPIO.PWM(pin,50))
            self._pins[-1].start(50)


    def set(self,rgb):

        for i in range(3):

            self._pins[i].ChangeDutyCycle(value)

