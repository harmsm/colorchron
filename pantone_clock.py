#!/usr/bin/env python3
__description__ = \
"""
Control a pantone clock that displays an RGB value to represent time.  
Using the default configuration, the clock will start at blue and then
sweep around the RGB colorwheel counterclockwise over 24 hours.  

 0:00 blue
 4:00 cyan
 8:00 green
12:00 yellow
16:00 red
20:00 magenta

The clock can also incorporate an optional ambient light sensor that dims
the clock in the dark.

If run as a standalone program, the library takes a json file containing
the keyword arguments passed to PantoneClock.__init__.  The special 
key "ambient" in that json file should contain a dictionary of keyword
arguments for AmbientLightSensor.__init__, if an ambient light sensor
is to be used with the clock.

If run as a library, a clock instance can be created, started, and 
stopped.  The clock runs on its own thread, so other processes may
run after it spawns.

import pantone_clock
p = pantone_clock.PantoneClock([pin1,pin2,pin3])
p.start()
"""
__usage__ = "pantone_clock.py json_config_file"
__author__ = "Michael J. Harms"
__date__ = "2018-04-30"

import time, datetime, json, sys, copy, multiprocessing, math

import board
import neopixel
import smbus

class AmbientLightSensor:
    """
    Read an ambient light sensor and return a value between min_out and
    max_out.  Implemented for a CJMCU-3216 sensor plugged into I2C bus.
    """

    def __init__(self,
                 sensor_bus=1,
                 sensor_address=0x1E,
                 low_address=0x0C,
                 high_address=0x0D,
                 min_out=0.05,max_out=1.0,
                 min_meas=0,max_meas=65792):
        """
        sensor_bus: sensor bus value (1 for SDA/SCL on pi)
        sensor_address: light sensor address
        low_address: address for low-sensitivity sensor
        high_address: address for high-sensitivity sensor
        min_out: lowest value that will ever be put out by class 
        max_out: highest value that will ever be put out by class 
        min_meas: measurement value corresponding to min_out
        max_meas: measurement value corresponding to max_out
        """

        self._sensor_bus = sensor_bus
        self._sensor_address = sensor_address
        self._low_address = low_address
        self._high_address = high_address
        self._min_out = min_out
        self._max_out = max_out
        self._min_meas = min_meas
        self._max_meas = max_meas

        # Define linear relationship between measurement and output values
        self._slope = (self._max_out - self._min_out)/(self._max_meas - self._min_meas)
        self._intercept = self._max_out - self._slope*self._max_meas

        # Activate device
        self._bus = smbus.SMBus(1)
        self._bus.write_byte_data(self._sensor_address,0x00,0x01)
  
    @property
    def brightness(self):
        """
        Return the brightness.
        """

        # Combine readings from low-sensitivity and high-sensitivity sensors
        # to get full 16-bit range 
        low =  self._bus.read_byte_data(self._sensor_address,self._low_address)
        high = self._bus.read_byte_data(self._sensor_address,self._high_address)
        value = (high << 8) + low

        if value < self._min_meas:
            return self._min_out

        if value > self._max_meas:
            return self._max_out

        return self._intercept + self._slope*value
          

class PantoneClock:
    """
    Control a pantone clock attached to DIN (pin 18). 
    """
    
    def __init__(self,
                 num_leds=15,
                 seconds_per_cycle=86400,
                 pantone_zero_position=240,
                 counterclockwise=True,
                 update_interval=0.1,
                 brightness=1.0,
                 min_brightness=0.05):
        """
        num_leds: number of leds in the array
        seconds_per_cycle: number of seconds that it takes to sweep the entire
                           RGB wheel.  86400 s corresponds to 24 hr
        pantone_zero_position: wheel position, in degrees, corresponding to 0
                               seconds.  This is midnight for the default 24 
                               hour clock.  0: red, 60: yellow, 120: green,
                               180: cyan, 240: blue, 300: magenta.  
        counterclockwise: go counterclockwise around the RGB wheel
        update_interval: how often to update the clock in seconds.
        brightness: overall brightness of the clock (between 0 and 1).  If an 
                    ambient light sensor is used, the brightness scalar will
                    be applied on top of brightness changes indicated by the
                    sensor.
        min_brightness: minimum brightness of clock
        """

        self._num_leds = num_leds
        if self._num_leds <= 0:
            err = "number of leds must be greater than zero.\n"
            raise ValueError(err)

        self._sec_per_cycle = seconds_per_cycle
        if self._sec_per_cycle <= 0:
            err = "seconds_per_cycle must be greater than zero.\n"
            raise ValueError(err)

        self._pantone_zero_position = pantone_zero_position
        self._counterclockwise = bool(counterclockwise)

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

        self._neopixels = neopixel.NeoPixel(board.D18, self._num_leds)

        # Put starting position in terms of a fraction of the total
        # sweep 
        fx_pantone_zero = self._pantone_zero_position % 360
        fx_pantone_zero = fx_pantone_zero/360.0

        # Configure each channel
        self._rgb = [0.,0.,0.]
        self._channel_offsets = []
        for i in range(3):
            v = fx_pantone_zero + i*self._sec_per_cycle/3
            self._channel_offsets.append(v)

        # Configure intervals for cycling the clock
        self._intervals = [1/6.,3/6.,4/6.]

        # Currently no light sensor
        self._light_sensor = None

        # Currently stopped
        self._running = False

    def _calc_rgb_values(self,time):
        """
        Calculate the RGB channel values corresponding to this time.
        """

        for i in range(3):

            # Figure out how far around the clock we should be
            channel_time = time + self._channel_offsets[i]
            fx_time = (channel_time % self._sec_per_cycle)/self._sec_per_cycle

            # Run counter clockwise if requested
            if self._counterclockwise:
                fx_time = 1 - fx_time
        
            # Ramp between 0 and 1 for the 1st sixth of the clock
            if fx_time < self._intervals[0]:
                self._rgb[i] = fx_time/self._intervals[0]
                continue

            # Hold at 1 for the 2nd and 3rd sixth of the clock
            if fx_time >= self._intervals[0] and fx_time < self._intervals[1]:
                self._rgb[i] = 1.0
                continue

            # Ramp between 1 and 0 for the 4th sixth of the clock 
            if fx_time >= self._intervals[1] and fx_time < self._intervals[2]:
                m = 1/(self._intervals[1] - self._intervals[2]) 
                b = 1 - self._intervals[1]*m 
                self._rgb[i] = fx_time*m + b
                continue
       
            # Hold at 0 for the 5th and 6th sixth of the clock
            self._rgb[i] = 0.0

    def _update(self):
        """
        Update the clock.
        """  

        # Get the current time.
        now = datetime.datetime.now()

        # Convert into seconds since midnight
        time_in_seconds = (now.hour*60 + now.minute)*60 + now.second

        # Update the RGB values with this new time 
        self._calc_rgb_values(time_in_seconds)

        # Set the brightness, imposing limit that forces value to be between
        # 1 and the minimum brightness. 
        bright_scalar = self.brightness*self.ambient_brightness
        if bright_scalar > 1:
            bright_scalar = 1.0
        if bright_scalar < self._min_brightness:
            bright_scalar = self._min_brightness

        # Normalize channels so total duty cycle is always 100*bright_scalar.
        # This keeps the intensity the same, whether light is coming from
        # one or two output channels
        total = sum(self.rgb)
        values = []
        for i in range(3):
            values.append(int(math.floor(bright_scalar*255*self.rgb[i]/total)))

        for i in range(self._num_leds):
            self._neopixels[i] = tuple(values)

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
    def rgb(self): return self._rgb

    @property
    def ambient_brightness(self):
        """
        Ambient brightness.  If no sensor has been added, return 1.0.  
        """
        
        if self._light_sensor is None:
            return 1.0
        else:
            return self._light_sensor.brightness
                

def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    # Parse command line
    try:
        control_file = argv[0]
    except IndexError:
        err = "Incorrect arguments. Usage:\n\n{}\n\n".format(__usage__)
        raise ValueError(err)

    # load in json file
    data = json.loads(open(control_file,'r').read())

    # Parse configuration file.  Keys should be keyword arguments to 
    # PantoneClock.__init__.  The key "ambient" is a special key that should
    # point to a dictionary of keywords to be passed to 
    # AmbientLightSensor.__init__.
    ambient_kwargs = {}
    pantone_kwargs = {}
    for k in data.keys():
        if k == "ambient":
            ambient_kwargs = copy.deepcopy(data[k])
        else:
            pantone_kwargs[k] = copy.deepcopy(data[k])

    # Create clock 
    clock = PantoneClock(**pantone_kwargs) 
    
    # Potentially create an ambient light sensor
    if len(ambient_kwargs) > 0:
        light_sensor = AmbientLightSensor(**ambient_kwargs)
        clock.add_ambient_light_sensor(light_sensor)
   
    # Start the clock 
    clock.start() 
  

if __name__ == "__main__":
    main()

