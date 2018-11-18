#!/usr/bin/env python3
                
import colorchron

# create clock instance
clock = colorchron.Clock()

# create colorwheel, led, and light sensor instances

# Runs for 24 hour cycle by default
colorwheel = colorchron.colorwheel.RYB(counterclockwise=True,
                                       zero_position=240)
led = colorchron.led.Neopixel()
light_sensor = colorchron.light_sensor.CJMCU3216()

# append the color wheel, light sensor, and led to the clock
clock.add_colorwheel(colorwheel)
clock.add_ambient_light_sensor(light_sensor)
clock.add_led(led)

# start the clock
clock.start()


