#!/usr/bin/python3.9
# Script used to initialize fans once booted

# Modified code from Adafruit (learn.adafruit.com)
#	Original: T.P. Boyle 05/2021

import time
import board
from adafruit_emc2101 import EMC2101

i2c = board.I2C()  # uses board.SCL and board.SDA
emc = EMC2101(i2c)

emc.manual_fan_speed = 30


