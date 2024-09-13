#!/usr/bin/python3.9
'''
run_calibration_kill.py


Script Description: Python script to turn on/off calibration gas solenoid valves and switch between calibrating different sensors depending on stdin

History
	Original: C. Martin 8/2018
	Modified: T.P. Boyle 2/2020 - Simplified, output open/closed time, RPIO.GPIO
	Modified: T.P. Boyle 1/2022 - Added support for multiple valve, input valve and time when running. 
		- Added Python3 support
		- Open/close data return in JSON
	Modified: T.P. Boyle 3/3022 - Added keyboard exception, closes valves when ctrl+C is run
	Modified: T.P. Boyle 2/2023 - Removed LED pin w/ hardware revision, added support for V3 and V4
	Modified: T.P. Boyle 07/2024 - Added tank concentration and serial number inputs, logic to detect missing input variables, support for sensor switching

USAGE
	sudo python3 run_calibration.py [valve_num] [cal_time_sec] [mqtt_topic] [tank_conc] [tank_#] [calibrated_sensor]
	sudo python3 run_calibration.py 1 $CAL_TIME cl/raw/$STN_OWNER/$STN_LOC/$STN_NAME/cal_val1 $TANK_CONC_400 $TANK_NUM_400 $ACTIVE_SENSOR_CAL
'''

import sys
import datetime
import RPi.GPIO as GPIO
import time
import json

if len(sys.argv) != 7:
	print("Usage: python3 run_calibration_kill.py <valve_#> <cal_time> <mqtt_topic> <tank_conc> <tank_#> <calibrated_sensor> ")
	sys.exit(1)

VALVE_NUM = int(sys.argv[1])                     # convert inputed string to text, get valve number
calTime = int(sys.argv[2])                      # convert inputed string to text, get cal. time duration
topic = str(sys.argv[3])
TANK_CONC = sys.argv[4]
TANK_NUM = str(sys.argv[5])
ACTIVE_SENSOR = str(sys.argv[6])

if VALVE_NUM == 1:
	cal_GPIOPin = 20

elif VALVE_NUM == 2:
	cal_GPIOPin = 21
	
else:
	print("Invalid calibration valve selection, quitting program")
	sys.exit(1)

sensor_GPIOPin = 12	# system uses V3 for sensor toggling
	
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(cal_GPIOPin,GPIO.OUT) 	# Initialize calibration GPIO Pin
	GPIO.setup(sensor_GPIOPin,GPIO.OUT)	# initialize sensor toggling GPIO pin
	
	if ACTIVE_SENSOR == "k96_1":
		GPIO.output(sensor_GPIOPin,GPIO.LOW)
		
	elif ACTIVE_SENSOR == "k96_2":
		GPIO.output(sensor_GPIOPin,GPIO.HIGH)
	
	else:
		print("Invalid sensor calibration selection, quitting program")
		sys.exit(1)

	GPIO.output(cal_GPIOPin,GPIO.HIGH)	# Open valve

	timeOpen = int(time.time())	# Store exact time when valve is opened
	timeout = timeOpen + calTime		# Calculate time for valve to remain open

	# Loop to keep the valve open
	while True:
		if time.time() > timeout:
			break

	GPIO.output(cal_GPIOPin,GPIO.LOW)
	GPIO.output(sensor_GPIOPin,GPIO.LOW)
	timeClosed = int(time.time())

	echo_json = {
		"epoch": int(time.time()),
		"valve_num": VALVE_NUM,
		"cal_time": calTime,
		"valve_open": timeOpen,
		"valve_close": timeClosed,
		"topic": topic,
		"tank_conc": float(TANK_CONC),
		"tank_num": TANK_NUM,
		"calibrated_sensor": ACTIVE_SENSOR
	}

	print(json.dumps(echo_json))

	GPIO.cleanup()
	
except KeyboardInterrupt:				# Exception - close valve when ctl-c and print info
	GPIO.output(cal_GPIOPin,GPIO.LOW)
	GPIO.output(sensor_GPIOPin,GPIO.LOW)
	timeClosed = int(time.time())

	echo_json = {
		"epoch": int(time.time()),
		"valve_num": valveNum,
		"cal_time": calTime,
		"valve_open": timeOpen,
		"valve_close": timeClosed,
		"topic": topic,
		"tank_conc": TANK_CONC,
		"tank_num": TANK_NUM,
		"calibrated_sensor": ACTIVE_SENSOR
	}

	print(json.dumps(echo_json))
	GPIO.cleanup()
	sys.exit()



