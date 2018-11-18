#!/usr/bin/env python3
                
import colorchron

# create clock instance
clock = colorchron.Clock() 

# create colorwheel, led, and light sensor instances
colorwheel = colorchron.colorwheel.Chromachron(seconds_per_cycle=60)
led = colorchron.led.Neopixel()
light_sensor = colorchron.light_sensor.CJMCU3216()

# append the color wheel, light sensor, and led to the clock
clock.add_colorwheel(colorwheel)
clock.add_ambient_light_sensor(light_sensor)
clock.add_led(led)

# start the clock
clock.start()


