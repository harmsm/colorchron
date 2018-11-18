__description__ = \
"""
Base class for ambient light sensors.
"""
__author__ = "Michael J. Harms"
__date__ = "2018-11-12"

class AmbientLightSensor:
    """
    Base class for reading an ambient light sensor and return a value between
    min_out and max_out.  To implement for real hardware, create a subclass of 
    AmbientLightSensor and redefine _initialize_hardware and _read_brightness.
    """

    def __init__(self,
                 min_out=0.05,max_out=1.0,
                 min_meas=0,max_meas=65792):
        """
        min_out: lowest value that will ever be put out by class 
        max_out: highest value that will ever be put out by class 
        min_meas: measurement value corresponding to min_out
        max_meas: measurement value corresponding to max_out
        """

        self._min_out = min_out
        self._max_out = max_out
        self._min_meas = min_meas
        self._max_meas = max_meas

        # Define linear relationship between measurement and output values
        self._slope = (self._max_out - self._min_out)/(self._max_meas - self._min_meas)
        self._intercept = self._max_out - self._slope*self._max_meas

        self._initialize_hardware()
  
    @property
    def brightness(self):
        """
        Return the brightness.
        """

        value = self._read_brightness()

        if value < self._min_meas:
            return self._min_out

        if value > self._max_meas:
            return self._max_out

        return self._intercept + self._slope*value

    
    def _initialize_hardware(self):
        """
        Initialize hardware (dummy method).
        """

        pass

    def _read_brightness(self):
        """
        Read brightness from hardware (dummy method).
        """  

        return self._max_meas
        

