__description__ = \
"""
Control a clock that displays an RGB value to represent time.  
"""
__author__ = "Michael J. Harms"
__date__ = "2018-04-30"

import time, datetime, json, sys, copy, multiprocessing, math

class PantoneClock:
    """
    Control a pantone clock.
    """
    
    def __init__(self,
                 update_interval=0.1,
                 brightness=1.0,
                 min_brightness=0.05):
        """
        update_interval: how often to update the clock in seconds.
        brightness: overall brightness of the clock (between 0 and 1).  If an 
                    ambient light sensor is used, the brightness scalar will
                    be applied on top of brightness changes indicated by the
                    sensor.
        min_brightness: minimum brightness of clock
        """

        self._update_interval = update_interval
        if self._update_interval <= 0:
            err = "update interval must be greater than zero.\n"
            raise ValueError(err)

        self._brightness = brightness
        if self._brightness < 0 or self._brightness > 1:
            err = "brightness must be between 0 and 1.\n"
            raise ValueError(err)

        self._min_brightness = min_brightness
        if self._min_brightness < 0 or self._min_brightness > 1:
            err = "minimum brightness must be between 0 and 1.\n"
            raise ValueError(err)

        # Currently no colorwheel
        self._colorwheel = None

        # Currently no led
        self._led = None

        # Currently no light sensor
        self._light_sensor = None

        # Currently stopped
        self._running = False

        self._rgb = [0.,0.,0.]

    def _update(self):
        """
        Update the clock.
        """  

        # Get the current time.
        now = datetime.datetime.now()

        # Convert into seconds since midnight
        time_in_seconds = (now.hour*60 + now.minute)*60 + now.second

        # Update the RGB values with this new time 
        if self._colorwheel is not None:
            self._rgb = self._colorwheel.rgb(time_in_seconds)[:]

        # Set the brightness, imposing limit that forces value to be between
        # 1 and the minimum brightness. 
        bright_scalar = self.brightness*self.ambient_brightness
        if bright_scalar > 1:
            bright_scalar = 1.0
        if bright_scalar < self._min_brightness:
            bright_scalar = self._min_brightness

        # Normalize channels so intensity is always sum(rgb)*bright_scalar.
        # This keeps the intensity the same, whether light is coming from
        # one, two, or three output channels
        total = sum(self.rgb)
        values = []
        for i in range(3):
            values.append(int(round(255*bright_scalar*self.rgb[i]/total,0)))

        # Set the LEDs to have desired RGB valuse
        values = tuple(values)
        if self._led is not None:
            self._led.set(values)

    def _run(self):
        """
        Loop that updates clock every update_interval seconds.
        """    

        while True:
            self._update()
            time.sleep(self._update_interval)
 
    def start(self):
        """
        Start the clock on its own thread.
        """

        # If already running, do not start
        if self._running:
            return

        self._process = multiprocessing.Process(target=self._run)
        self._process.start()
        self._running = True
 
    def stop(self):
        """
        Stop the clock.
        """           

        # Do not running, do not stop
        if not self._running:
            return

        self._process.terminate()
        self._running = False

    def add_colorwheel(self,colorwheel):

        self._colorwheel = colorwheel
        try:
            self._colorwheel.rgb
        except AttributeError:
            err = "colorwheel must have 'rgb' attribute.\n"
            raise ValueError(err)

    def add_led(self,led):
        """
        """

        self._led = led
        try:
            self._led.set
        except AttributeError:
            err = "LEDs not available.  Must have 'set' attribute.\n"
            raise ValueError(err)

    def add_ambient_light_sensor(self,light_sensor):
        """
        Add an ambient light sensor.
        """

        self._light_sensor = light_sensor
        try:
            self._light_sensor.brightness
        except AttributeError:
            err = "Light sensor not readable.  Must have 'brightness' attribute.\n"
            raise ValueError(err)

    @property
    def brightness(self):
        """
        Brightness (controlled by user).  Read, but NOT set by thread.  This
        means the brightness can be adjusted while the clock is running.
        """       
 
        return self._brightness

    @brightness.setter
    def brightness(self,brightness):
        """
        Set the brightness.
        """

        if brightness < 0 or brightness > 1:
            err = "Brightness must be between zero and 1.\n"
            raise ValueError(err)

        self._brightness = float(brightness)

        # Make the thread come up for air and grab the new brightness value
        if self._running:
            self.stop()
            self.start()

    @property
    def rgb(self): 
        return self._rgb

    @property
    def ambient_brightness(self):
        """
        Ambient brightness.  If no sensor has been added, return 1.0.  
        """
        
        if self._light_sensor is None:
            return 1.0
        else:
            return self._light_sensor.brightness
                

