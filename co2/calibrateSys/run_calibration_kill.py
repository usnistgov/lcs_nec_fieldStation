#!/usr/bin/python3.9
'''
run_calibration_kill.py


Script Description: Python script to turn on/off calibration gas solenoid valve using GPIO pins and PCB, close valve if killed via ctrl c

History
	Original: C. Martin 8/2018
	Modified: T.P. Boyle 2/2020 - Simplified, output open/closed time, RPIO.GPIO
	Modified: T.P. Boyle 1/2022 - Added support for multiple valve, input valve and time when running. 
		- Added Python3 support
		- Open/close data return in JSON
	Modified: T.P. Boyle 3/3022 - Added keyboard exception, closes valves when ctrl+C is run
	Modified: T.P. Boyle 2/2023 - Removed LED pin w/ hardware revision, added support for V3 and V4

USAGE
	sudo python3 run_calibration.py [valve_num] [cal_time_sec] [topic]
	sudo python3 run_calibration.py 1 60 cl/raw/$STN_OWNER/$STN_LOC/$STN_NAME/cal_val1
'''

import sys
import datetime
import RPi.GPIO as GPIO
import time
import json

valveNum = int(sys.argv[1])                     # convert inputed string to text, get valve number
calTime = int(sys.argv[2])                      # convert inputed string to text, get cal. time duration
topic = str(sys.argv[3])

if valveNum == 1:
	GPIOPin = 20

elif valveNum == 2:
	GPIOPin = 21

elif valveNum == 3:
	GPIOPin = 12

elif valveNum == 4:
	GPIOPin = 27

else:
	print("Invalid valve selection")
	
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(GPIOPin,GPIO.OUT) 	# Initialize GPIO Pin
	GPIO.output(GPIOPin,GPIO.HIGH)	# Open valve

	timeOpen = int(time.time())	# Store exact time when valve is opened
	timeout = timeOpen + calTime		# Calculate time for valve to remain open

	# Loop to keep the valve open
	while True:
		if time.time() > timeout:
			break

	GPIO.output(GPIOPin,GPIO.LOW)
	timeClosed = int(time.time())

	echo_json = {
		"epoch": int(time.time()),
		"valve_num": valveNum,
		"cal_time": calTime,
		"valve_open": timeOpen,
		"valve_close": timeClosed,
		"topic": topic
	}

	print(json.dumps(echo_json))

	GPIO.cleanup()
	
except KeyboardInterrupt:				# Exception - close valve when ctl-c and print info
	GPIO.output(GPIOPin,GPIO.LOW)
	timeClosed = int(time.time())

	echo_json = {
		"epoch": int(time.time()),
		"valve_num": valveNum,
		"cal_time": calTime,
		"valve_open": timeOpen,
		"valve_close": timeClosed,
		"topic": topic
	}

	print(json.dumps(echo_json))
	GPIO.cleanup()
	sys.exit()



