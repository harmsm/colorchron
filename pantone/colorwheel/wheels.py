__description__ = \
"""
Subclasses defining avaiable color wheels.  Each class defines an .rgb method
that takes time as an argument.  This returns the RGB value for that time 
corresponding to the value on whatever color wheel is being traversed.
"""
__author__ = "Michael J. Harms"
__date__ = "2018-11-15"

from .base import ColorWheel
import colorsys, math

class RGB(ColorWheel):
    """
    Red-Green-Blue color wheel.
    """

    def rgb(self,time):

        values = self.get_three_channel(time)

        return [math.ceil(255*v) for v in values]

class CMY(ColorWheel):
    """
    Go around the Cyan-Magenta-Yellow color wheel.
    """

    def rgb(self,time):

        values = self.get_three_channel(time)

        return [math.ceil(255*(1 - v)) for v in values]

class HSV(ColorWheel):
    """
    Hue color wheel, using fixed saturation and value.
    """

    def __init__(self,
                 seconds_per_cycle=86400,
                 pantone_zero_position=240,
                 counterclockwise=True,
                 saturation=1.0,value=1.0):

        self._saturation = saturation
        self._value = value

        super().__init__(self,
                         seconds_per_cycle,
                         pantone_zero_position,
                         counterclockwise)
    
    def rgb(self,time):
        """
        RGB values are determined by a single channel.
        """

        hue = self.get_single_channel(time)
        
        values = colorsys.hsv_to_rgb(hue,self._saturation,self._value)
        
        return [math.ceil(255*v) for v in values] 


class RYB(ColorWheel):
    """
    Red-Yellow-Blue color wheel.
    """
    
    _magic = [[1,     1,     1],
              [1,     1,     0],
              [1,     0,     0],
              [1,     0.5,   0],
              [0.163, 0.373, 0.6],
              [0.0,   0.66,  0.2],
              [0.5,   0.0,   0.5],
              [0.2,   0.094, 0.0]]

    def rgb(self,time):

        values = self.get_three_channel(time)
  
        values = rxb.rxb_to_rgb(values,self._magic)

        return [math.ceil(255*v) for v in values]



