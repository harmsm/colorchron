#!/usr/bin/env python3
__description__ = \
"""
Base class for leds.
"""
__author__ = "Michael J. Harms"
__date__ = "2018-11-12"

class LED:
    """
    Drivers for LED arrays should be subclasses of this class.  They must
    expose a set method that takes an 3-element list of rgb values between 
    0-255.
    """
    
    def __init__(self):

        pass

    def set(self,rgb):

        pass
