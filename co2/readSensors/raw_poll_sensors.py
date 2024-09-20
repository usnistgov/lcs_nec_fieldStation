#!/usr/bin/env python3
# raw_poll_sensors.py

'''
Developed to power multiplexer and read from 3 different sensors

This script must be in the same directory as fn_k30.py and fn_k96.py
	Because each station will, for the most part, have the same sensor configurations,
	this is standardized

	History
	Original: T.P. Boyle 07/2021
	Modified: T.P. Boyle 02/2022 - Migrated from python 2 -> python 3
	Modified: T.P. Boyle 06/2023 - Support for bad/null sensor response, not sending to redis

Usage
	sudo python3 raw_poll_sensors.py
'''

#========== Import Necessary Python Modules ==========

import serial			# for serial I/O
import time			# for time.sleep
import RPi.GPIO as GPIO
import fn_k30
import fn_k96_raw

#================== Define Variables =================

IOdevice = '/dev/ttyS0'				#define port for I/O
UNDEF = -9999.					# undefined value
e_pin = 12					# multiplexer enable pin
s0_pin = 16					# multiplexer s0 pin
s1_pin = 18					# multiplexer s1 pin

# Empty list to store K96 results
k96_1_response = []
k96_2_response = []
k96_3_response = []
k96_4_response = []

#=============== Initialize GPIO Pins ================ 

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(e_pin, GPIO.OUT)
GPIO.setup(s0_pin, GPIO.OUT)
GPIO.setup(s1_pin, GPIO.OUT)

# Initialize for reading K30 at A0,B0
GPIO.output(e_pin, GPIO.LOW)
GPIO.output(s0_pin, GPIO.LOW)
GPIO.output(s1_pin, GPIO.LOW)

time.sleep(0.1)

#======================== Read Sensors =====================

# Read K96_1
GPIO.output(s0_pin, GPIO.HIGH)
GPIO.output(s1_pin, GPIO.LOW)
time.sleep(0.1)

k96_1_response = fn_k96_raw.readSensor('k96_1')	# read sensor, store response in variable

if(len(k96_1_response) > 1):				# If sensor reading is returned
	print(*k96_1_response)				# print response to stdout for redis program

# Read K96_2
GPIO.output(s0_pin, GPIO.LOW)
GPIO.output(s1_pin, GPIO.HIGH)
time.sleep(0.1)
k96_2_response = fn_k96_raw.readSensor('k96_2')

if(len(k96_2_response) > 1):                            # If sensor reading is returned
        print(*k96_2_response)                          # print response to stdout for redis program

# Read K96_3
GPIO.output(s0_pin, GPIO.LOW)
GPIO.output(s1_pin, GPIO.LOW)
time.sleep(0.1)
k96_3_response = fn_k96_raw.readSensor('k96_3')

if(len(k96_3_response) > 1):
	print(*k96_3_response)

# MUX supports up to 4 sensors - uncomment if another sensor is needed
# Read K96_4
#GPIO.output(s0_pin, GPIO.HIGH)
#GPIO.output(s1_pin, GPIO.HIGH)
#time.sleep(0.1)
#k96_4_response = fn_k30.readSensor('k30_1')
#
#for x in range(len(k96_4_response)):
#	if x == len(k96_4_response) - 1:
#		print(k96_4_response[x])
#	else:	
#		print(k96_4_response[x]),	


