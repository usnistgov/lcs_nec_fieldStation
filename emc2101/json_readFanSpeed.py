#!/usr/bin/python3.9
'''
Script Description: Read fan speed (rpm), print output as json to stdout

History: Modified code from Adafruit (learn.adafruit.com)
	Original: T.P. Boyle 5/2021 (w/ provision from Adafruit opensource code)
	Modified: T.P. Boyle 12/2022 - modified output to json, to work with mqtt_publish script
	Modified: T.P. Boyle 07/2024 - appended "m_sensor_type", "stn_id", and "stn_loc" parameters to the json

Usage
	sudo python3 json_readFanSpeed.py [mqtt_topic]

'''

import time
import board
from adafruit_emc2101 import EMC2101
import sys
import json
import os
from dotenv import load_dotenv

load_dotenv("/etc/environment")

MQTT_TOPIC = str(sys.argv[1])

i2c = board.I2C()  # uses board.SCL and board.SDA
emc = EMC2101(i2c)

speed = round(emc.fan_speed,2)
dict = {"epoch": int(time.time()), "topic": MQTT_TOPIC, "fan_speed": speed,"m_sensor_type":"emc2101","stn_id":os.getenv("STN_NAME"),"stn_loc":os.getenv("STN_LOC")}
json_str = json.dumps(dict)
print(json_str)

