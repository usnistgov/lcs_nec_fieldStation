#!/usr/bin/env python
# k30.py
#	Python module to read CO2 concentrations from a K-30 CO2 sensor.
#
#	Based off of sample code provided by CO2meter.com
#
#	History:
#	Original: C. Martin - 1/3/2014
#	Modified: C. Martin - 1/8/2014 - Added variables for device and undefined
#	Modified: C. Martin - 5/5/2016 - added in raw variable as well
#	Modified: T.P. Boyle - 1/20/2020 - Simplified code, added unix time, removed raw conversion
#	Modified: T.P. Boyle - 08/31/2020 - Supports key value pairs for REDIS, callable from other programs

'''
USAGE FROM OTHER PROGRAMS:
	fn_k30.readSensor([stream_name])
	fn_k30.readSensor(k96_1)
'''

#========== Import Necessary Python Modules ==========

import serial			# for serial I/O
import time

def readSensor(sensorName):
	#================== Define Variables =================

	IOdevice = '/dev/ttyS0'				#define port for I/O
	
	# List of commands
	sendCO2 = '\xFE\x44\x00\x08\x02\x9F\x25' 
	sendRaw = '\xFE\x44\x00\x04\x02\x9A\x25'
	sendTemp = '\xFE\x44\x00\x0A\x02\x9E\x45'	
	names = ["co2", "raw", "temp"]				# Names of key value pairs

	UNDEF = -9999.						# undefined value
	returnVals = []						#	

	#===================== Read Data =====================

	K30IO = serial.Serial(IOdevice,baudrate =9600,timeout=1)	# connect to serial port
	K30IO.flushInput()						# flush serial input buffer
	time.sleep(0.01)						# sleep for 10 milliseconds

	returnVals.append(sensorName)
	# Request CO2 from sensor
	try:
		K30IO.write(sendCO2)				# send command to K-30
		time.sleep(0.01)				# sleep for 10 milliseconds
		K30out = K30IO.read(7)				# save bytes returned by K-30
		high = ord(K30out[3])				# high value is fourth byte
		low = ord(K30out[4])				# low value is fifth byte
		CO2 = (high*256) + low				# convert bytes to CO2 ppm value
		if CO2 > 65000:					# 16-bit so subtract to get negative values
			CO2 = CO2-65536
		
		returnVals.append(names[0])
		returnVals.append(CO2)
	except:
		CO2 = UNDEF					# store CO2 ppm value as undefined
		
		
	# Request raw data from sensor
	K30IO = serial.Serial(IOdevice,timeout=1)		# connect to serial port
	K30IO.flushInput()					# flush serial input buffer
	time.sleep(0.01)					# sleep for 10 milliseconds
	try:
		K30IO.write(sendRaw)				# send command to K-30
		time.sleep(0.01)				# sleep for 10 milliseconds
		K30out = K30IO.read(7)				# save bytes returned by K-30
		high = ord(K30out[3])				# high value is fourth byte
		low = ord(K30out[4])				# low value is fifth byte
		raw = (high*256) + low				# convert bytes to raw value
		
		returnVals.append(names[1])
		returnVals.append(raw)
	except:
		raw = UNDEF					# store CO2raw ppm value as undefined
		
	# Request temp from sensor
	K30IO = serial.Serial(IOdevice,timeout=1)		# connect to serial port
	K30IO.flushInput()					# flush serial input buffer
	time.sleep(0.01)					# sleep for 10 milliseconds
	try:		
		K30IO.write(sendTemp)				# send command to K-30
		time.sleep(0.01)				# sleep for 10 milliseconds
		K30out = K30IO.read(7)				# save bytes returned by K-30
		high = ord(K30out[3])				# high value is fourth byte
		low = ord(K30out[4])				# low value is fifth byte
		temp = (high*256) + low				# convert bytes to temp value
		if temp > 65000:				# 16-bit so subtract to get negative values
			temp = temp-65536
		temp = (temp/3.) + 20				# convert to celsius from raw value 

		returnVals.append(names[2])
		returnVals.append(temp)
	except:
		temp = UNDEF					# store value as undefined

	return returnVals


if __name__ == '__main__':
	readSensors(sensorName)
