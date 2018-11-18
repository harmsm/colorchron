#!/usr/bin/env python3
                
import pantone

# create clock instance
clock = pantone.PantoneClock() 

# create colorwheel, led, and light sensor instances
colorwheel = pantone.colorwheel.Chromachron(seconds_per_cycle=60)
led = pantone.led.Neopixel()
light_sensor = pantone.light_sensor.CJMCU3216()

# append the color wheel, light sensor, and led to the clock
clock.add_colorwheel(colorwheel)
clock.add_ambient_light_sensor(light_sensor)
clock.add_led(led)

# start the clock
clock.start()


