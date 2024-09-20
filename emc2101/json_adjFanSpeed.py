#!/usr/bin/python3.9
'''
Script Description: Changes fan speed to user-inputed duty cycle, print output as json to stdout

History
	Original: T.P. Boyle 5/2021 (w/ provision from Adafruit opensource code)
	Modified: T.P. Boyle 12/2022 - modified output to json, to work with mqtt_publish script
	Modified: T.P. Boyle 07/2024 - appended "m_sensor_type", "stn_id", and "stn_loc" parameters to the json
	Modified: T.P. Boyle 09/2024 - added pkt_type parameter for AWS validation

Usage
	sudo python3 json_adjFanSpeed.py [duty_cycle] [mqtt_topic]

'''

import time
import board
from adafruit_emc2101 import EMC2101
import sys
import json
import os
from dotenv import load_dotenv

load_dotenv("/etc/environment")

FAN_SPEED = int(sys.argv[1])
MQTT_TOPIC = str(sys.argv[2])

i2c = board.I2C()  # uses board.SCL and board.SDA
emc = EMC2101(i2c)

emc.manual_fan_speed = FAN_SPEED							# set fan speed
dict = {"epoch": int(time.time()), "topic": MQTT_TOPIC, "duty_cycle": FAN_SPEED, "m_sensor_type":"emc2101","stn_id":os.getenv("STN_NAME"),"stn_loc":os.getenv("STN_LOC"),"pkt_type":"emc2101"}	# create dict with packet info
json_str = json.dumps(dict)								# convert dict to json for stdout
print(json_str)

