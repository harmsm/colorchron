#!/usr/bin/env python3
                
import pantone

clock = pantone.PantoneClock()
led = pantone.led.Neopixel()
light_sensor = pantone.light_sensor.CJMCU3216()

clock.add_ambient_light_sensor(light_sensor)
clock.add_led(led)

clock.start()

