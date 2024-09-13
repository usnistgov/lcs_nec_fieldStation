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

Usage
	sudo python3 raw_poll_sensors.py
'''

#========== Import Necessary Python Modules ==========

import serial			# for serial I/O
import time			# for time.sleep
import RPi.GPIO as GPIO
#import fn_k30
import fn_k96_raw
#import fn_hpma

#================== Define Variables =================

IOdevice = '/dev/ttyS0'				#define port for I/O
UNDEF = -9999.					# undefined value
e_pin = 12					# multiplexer enable pin
mx1_s0_pin = 16					# multiplexer s0 pin
mx1_s1_pin = 18					# multiplexer s1 pin
mx2_s0_pin = 7
mx2_s1_pin = 36
mx3_s0_pin = 15
mx3_s1_pin = 35

# Empty list to store K96 results
k96_1_response = []
k96_2_response = []
k96_3_response = []
k96_4_response = []
k96_5_response = []
k96_6_response = []
k96_7_response = []
k96_8_response = []
k96_9_response = []
k96_10_response = []

#=============== Initialize GPIO Pins ================ 

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(e_pin, GPIO.OUT)
GPIO.setup(mx1_s0_pin, GPIO.OUT)
GPIO.setup(mx1_s1_pin, GPIO.OUT)
GPIO.setup(mx2_s0_pin, GPIO.OUT)
GPIO.setup(mx2_s1_pin, GPIO.OUT)
GPIO.setup(mx3_s0_pin, GPIO.OUT)
GPIO.setup(mx3_s1_pin, GPIO.OUT)

# Initialize for reading K30 at A0,B0
GPIO.output(e_pin, GPIO.LOW)
GPIO.output(mx1_s0_pin, GPIO.LOW)
GPIO.output(mx1_s1_pin, GPIO.LOW)
GPIO.output(mx2_s0_pin, GPIO.LOW)
GPIO.output(mx2_s1_pin, GPIO.LOW)
GPIO.output(mx3_s0_pin, GPIO.LOW)
GPIO.output(mx3_s1_pin, GPIO.LOW)

time.sleep(0.1)

#======================== Read Sensors =====================
# Read from MX1

# Read K96_1
GPIO.output(mx1_s0_pin, GPIO.LOW)
GPIO.output(mx1_s1_pin, GPIO.LOW)
time.sleep(0.05)

k96_1_response = fn_k96_raw.readSensor('k96_1')

print(*k96_1_response)

# Read K96_2
GPIO.output(mx1_s0_pin, GPIO.HIGH)
GPIO.output(mx1_s1_pin, GPIO.LOW)
time.sleep(0.05)

k96_2_response = fn_k96_raw.readSensor('k96_2')

print(*k96_2_response)

# Read K96_3
GPIO.output(mx1_s0_pin, GPIO.LOW)
GPIO.output(mx1_s1_pin, GPIO.HIGH)
time.sleep(0.05)

k96_3_response = fn_k96_raw.readSensor('k96_3')

print(*k96_3_response)

# Set MX1 to CH3 to access MX2
GPIO.output(mx1_s0_pin, GPIO.HIGH)
GPIO.output(mx1_s1_pin, GPIO.HIGH)

#Read K96-4
GPIO.output(mx2_s0_pin, GPIO.LOW)
GPIO.output(mx2_s1_pin, GPIO.LOW)
time.sleep(0.05)

k96_4_response = fn_k96_raw.readSensor('k96_4')

print(*k96_4_response)

# Read K96_5
GPIO.output(mx2_s0_pin, GPIO.HIGH)
GPIO.output(mx2_s1_pin, GPIO.LOW)
time.sleep(0.05)

k96_5_response = fn_k96_raw.readSensor('k96_5')

print(*k96_5_response)

# Read K96_6
GPIO.output(mx2_s0_pin, GPIO.LOW)
GPIO.output(mx2_s1_pin, GPIO.HIGH)
time.sleep(0.05)

k96_6_response = fn_k96_raw.readSensor('k96_6')

print(*k96_6_response)

# Set MX2 to CH3 to access MX3
GPIO.output(mx2_s0_pin, GPIO.HIGH)
GPIO.output(mx2_s1_pin, GPIO.HIGH)

#Read K96_7
GPIO.output(mx3_s0_pin, GPIO.LOW)
GPIO.output(mx3_s1_pin, GPIO.LOW)
time.sleep(0.05)

k96_7_response = fn_k96_raw.readSensor('k96_7')

print(*k96_7_response)

# Read K96_8
GPIO.output(mx3_s0_pin, GPIO.HIGH)
GPIO.output(mx3_s1_pin, GPIO.LOW)
time.sleep(0.05)

k96_8_response = fn_k96_raw.readSensor('k96_8')

print(*k96_8_response)

# Read K96_9
GPIO.output(mx3_s0_pin, GPIO.LOW)
GPIO.output(mx3_s1_pin, GPIO.HIGH)
time.sleep(0.05)

k96_9_response = fn_k96_raw.readSensor('k96_9')

print(*k96_9_response)

# Read K96_10
GPIO.output(mx3_s0_pin, GPIO.HIGH)
GPIO.output(mx3_s1_pin, GPIO.HIGH)
time.sleep(0.05)

k96_10_response = fn_k96_raw.readSensor('k96_10')

print(*k96_10_response)
