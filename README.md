# Pantone Clock

Software for using a raspberry pi to drive RGB LED(s) as a pantone clock.

The software uses an RGB value to represent time.  Using the default
configuration, the clock will start at blue and then sweep around the RGB
colorwheel counterclockwise over 24 hours.  

 0:00 blue
 4:00 cyan
 8:00 green
12:00 yellow
16:00 red
20:00 magenta

The clock can also incorporate an ambient light sensor that dims the clock in
the dark.

A clock instance can be created, started, and 
stopped.  The clock runs on its own thread, so other processes may
run after it spawns.



```
import pantone

clock = pantone.PantoneClock()
led = pantone.led.Neopixel()
light_sensor = pantone.light_sensor.CJMCU3216()

clock.add_ambient_light_sensor(light_sensor)
clock.add_led(led)

clock.start()
```
