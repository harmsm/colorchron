# Pantone Clock

#### A physical clock that represents the current time using LED color

This project uses a raspberry pi to show the time using the color value of a
collection of LEDs.  This was inspired by work such as 
[what color is it?](http://whatcolorisit.sumbioun.com/), 
the [colour clock](http://thecolourclock.co.uk/), and the famous
[chromachron watch](https://www.hodinkee.com/articles/chromachron-a-radically-new-approach-to-time).

Using the default configuration, the clock will start at 
blue and then sweep around the RGB colorwheel counterclockwise over 24 hours.  

|  time | color   |
|-------|---------|
|  0:00 | blue    |
|  4:00 | cyan    |
|  8:00 | green   |  
| 12:00 | yellow  |
| 16:00 | red     |
| 20:00 | magenta |


The clock can also incorporate an ambient light sensor that tunes the brightness
of the clock so it is brighter in daylight and dimmer at night.

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

### Set up the pi

You will need a raspberry pi running a (relatively) recent operating system that
has python3 available in the package manager.  The instructions below are known
to work work for raspbian stretch light (kernel 4.14).  

The clock uses the system time to determine its color.  If you want the time to
be set automatically, you need to configure the pi to be on the internet while
the clock is running.  If you want to set the date manually, run:

```
sudo date -s '2018-11-14 11:26:00'
```

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

   replacing the path with the one you copied above.  **The `&` is critical.  If 
   you do not include it, the pi will not boot!**
4. Save the file and reboot the pi.  The clock LEDs should light up as soon 
   as the pi finishes booting, even if you do not log in.

## Hardware

[fritzing](http://fritzing.org) design files and pictures are of the
build available in the `design/` directory.

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
+ Appropriate wires. 

### Design

![design here](https://github.com/harmsm/pantone/raw/master/design/pantone-clock.png)

+ I used a proximity sensor with similar pins instead of an MJMCU3216 in the
  diagram to avoid making a special fritzing part just for this picture. 
+ The light sensor is powered by 3.3 V pin and connects via SDA/SCL pins
+ The LED array is powered by a 5 V pin and connects via the D18 pin.  

**NOTE.  This design powers the LED array off of the 5V pin on the raspberry 
pi.  This works for <= 15 LEDs before exceeding the current available on that
pin.  It also assumes you are not powering other peripherals (with the 
exception of the ambient light sensor).  If you want to have more LEDs, use
an external 5V power supply.  [See here](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring).**

### Implementation

+ I ended up soldering the 74AHCT125 logic level converter into a prototype
  board to avoid a huge number of jumper wires. 

![logic level](https://github.com/harmsm/pantone/raw/master/design/level-shift-board.png)
