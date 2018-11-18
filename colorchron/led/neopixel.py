#!/usr/bin/env python3
__description__ = \
"""
Driver for neopixel-style led array.
"""
__author__ = "Michael J. Harms"
__date__ = "2018-11-12"

from .base import LED

import board, neopixel

class Neopixel(LED):

    def __init__(self,num_leds=15):
        """
        num_leds: number of leds in the array
        """

        self._num_leds = num_leds
        if self._num_leds <= 0:
            err = "number of leds must be greater than zero.\n"
            raise ValueError(err)

        self._neopixels = neopixel.NeoPixel(board.D18, self._num_leds)

    def set(self,rgb):
        for i in range(self._num_leds):
            self._neopixels[i] = tuple(rgb)
        
