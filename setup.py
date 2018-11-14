#!/usr/bin/env python3

import sys

if sys.version_info[0] < 3:
    sys.exit('Sorry, Python < 3.x is not supported')

# Try using setuptools first, if it's installed
from setuptools import setup, find_packages

# Need to add all dependencies to setup as we go!
setup(name='pantone',
      packages=find_packages(),
      version='0.1',
      description="Software for using a raspberry pi to drive RGB LED(s) as a pantone clock.",
      long_description=open("README.md").read(),
      author='Michael J. Harms',
      author_email='harmsm@gmail.com',
      url='https://github.com/harmsm/pantone',
      download_url='https://github.com/harmsm/pantone/tarball/0.1',
      zip_safe=False,
      install_requires=["rpi_ws281x","adafruit-circuitpython-neopixel","python3-smbus"],
      classifiers=['Programming Language :: Python'])
