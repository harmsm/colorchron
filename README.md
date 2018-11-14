# Pantone Clock

#### Software for using a raspberry pi to drive RGB LED(s) as a pantone clock.

The software uses an RGB value to represent time.  Using the default
configuration, the clock will start at blue and then sweep around the RGB
colorwheel counterclockwise over 24 hours.  

|  time | color   |
|-------|---------|
|  0:00 | blue    |
|  4:00 | cyan    |
|  8:00 | green   |  
| 12:00 | yellow  |
| 16:00 | red     |
| 20:00 | magenta |

The clock can also incorporate an ambient light sensor that dims the clock in
the dark.

A clock instance can be created, started, and 
stopped.  The clock runs on its own thread, so other processes may
run after it spawns.


### Basic example script
```python
import pantone

clock = pantone.PantoneClock()
led = pantone.led.Neopixel()
light_sensor = pantone.light_sensor.CJMCU3216()

clock.add_ambient_light_sensor(light_sensor)
clock.add_led(led)

clock.start()
```

+ The ambient light sensor and LEDs are optional.  (Of course, if you don't load
  the LEDs, the program won't do anything particularly interesting).
+ To see what options you have for tweaking the clock output, run `python3` on
  the command line.  Then run the following:

  ```python
  import pantone
  help(pantone.PantoneClock)
  ```

## Installation

### Activate I2C 

1. At the command line, run `sudo raspi-config`
2. Select `P5 I2C` and hit `Enter.`  
3. Reboot the pi.

### Install git and smbus

1. At the command line, run `sudo apt-get install git python3-smbus`
2. Answer `Y` to any prompts.

### Install pantone clock

1. Clone the `pantone` git repository.  At the command line, run
   `git clone https://github.com/harmsm/pantone.git`
2. Install the pantone clock.  Run `cd pantone` followed by
   `sudo python3 setup.py install` 

### Running the clock
1. At the command line, navigate into the `pantone/example` directory.  This 
   directory has a script called `run_clock.py`.  
2. Run `sudo python3 run_clock.py`.  If the hardware is configured correctly,
   the clock should start running.

### To start the clock on boot
1. In the `pantone/example` directory, run the command `pwd`.  This should 
   print out the path (something like `/home/hermione/pantone/example`). 
   Select and copy the path. 
2. Open the `/etc/rc.local` file in an editor (`nano /etc/rc.local`).  
3. Somewhere before the line reading `exit 0` put the line:

   ```
   python3 /home/hermione/pantone/example/run_clock.py &
   ```

   replacing the path with the one you copied above.  Thie `&` is critical.  If 
   you do not include it, the pi will not boot!
4. Save the file and reboot the pi. 

## Hardware

### Parts list

+ Raspberry pi with necessary accessories (power supply, SD card, header pins,
  case)
+ 74AHCT125 logic-level converter OR 1N4001 diode to allow 3.3V logic on pi to
  interface with 5V logic on LED array diode. [See here](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring).
+ String of WS2812 LEDs.
+ MJMCU 3216 ambient light sensor.  (If you use a different light sensor, it
  must connect via SDA/SCL.  You may have to change the addresses in the file
  `pantone/light_sensor/cjmcu3216.py`.  If you end up writing a driver for a 
  different light sensor, feel free to make a pull request for this project). 
+ Appropriate wires

### Design

![design here](https://github.com/harmsm/pantone/raw/master/design/pantone-clock.png)

+ I used a proximity sensor with similar pins in the diagram (not the MJMCU 
  3216) to avoid having to make a fritzing part just for this picture. 
+ The light sensor is powered by 3.3 V pin and connects via SDA/SCL pins
+ The LED array is powered by a 5 V pin and connects via the D18 pin.  

**NOTE.  This design powers the LED array off of the 5V pin on the raspberry 
pi.  This works for <= 15 LEDs before exceeding the current available on that
pin.  It also assumes you are not powering other peripherals (with the 
exception of the ambient light sensor.  If you want to have more LEDs, use
an external 5V power supply.  [See here](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring).**

