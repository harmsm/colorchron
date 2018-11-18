__description__ = \
"""
Driver for a CJMCU 3216 ambient light sensor.
"""
__author__ = "Michael J. Harms"
__date__ = "2018-11-12"

import smbus

from .base import AmbientLightSensor

class CJMCU3216(AmbientLightSensor):
    """
    Read an ambient light sensor and return a value between min_out and
    max_out.  Implemented for a CJMCU-3216 sensor plugged into I2C bus.
    """
    
    def _initialize_hardware(self):
        """
        Initialize hardware (CJMCU 3216 values).
        """

        self._sensor_bus = 1
        self._sensor_address = 0x1E
        self._low_address = 0x0C 
        self._high_address = 0x0D

        # Activate device
        self._bus = smbus.SMBus(self._sensor_bus)
        self._bus.write_byte_data(self._sensor_address,0x00,0x01)

    def _read_brightness(self):
        """
        Read brightness from hardware.
        """  
        
        # Combine readings from low-sensitivity and high-sensitivity sensors
        # to get full 16-bit range 
        low =  self._bus.read_byte_data(self._sensor_address,self._low_address)
        high = self._bus.read_byte_data(self._sensor_address,self._high_address)
        value = (high << 8) + low

        return value

