# Pantone Clock

Software for using a raspberry pi to drive RGB LED(s) as a pantone clock.

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
```
import pantone

clock = pantone.PantoneClock()
led = pantone.led.Neopixel()
light_sensor = pantone.light_sensor.CJMCU3216()

clock.add_ambient_light_sensor(light_sensor)
clock.add_led(led)

clock.start()
```

## Prepping the pi

### Activate I2C 

1. At the command line, run `sudo raspi-config`
2. Select `P5 I2C` and hit `Enter.`  
3. Reboot the pi.

### Install pip3 and git

1. At the command line, run `sudo apt-get install pip3 git`
2. Answer `Y` to any prompts.

### Install pantone clock

1. Clone the `pantone` git repository.  At the command line, run
   `git clone https://github.com/harmsm/pantone.git`
2. Install the pantone clock.  Run either:
    A. `sudo pip3 install pantone` OR
    B. `cd pantone` followed by `sudo python3 setup.py install` 

### Running the clock
1. At the command line, run `cd pantone/example`.  This will put you in a 
   directory with a script called `run_clock.py`.  
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


