#!/usr/bin/env python

# Function-based program used to query K96 processed measurements
#
# Original: C Martin 2014
#	Modified: T.P. Boyle 08/2020 - updated for the K96, migrated to function format


'''
USAGE FROM OTHER PYTHON PROGRAMS:
	import fn_k96
	fn_k96.readSensor([stream_name])

	For example, in calling script:
	fn_k96.readSensor(k96_1)
'''

#========== Import Necessary Python Modules ==========

import serial			# for serial I/O
import time			# for sleep

#================== Define Variables =================

def readSensor(sensorName):
	IOdevice = '/dev/ttyS0'				#define port for I/O

	# List for commands to send
	command = ['\xFE\x44\x00\x00\x02\x98\xE5','\xFE\x44\x00\x02\x02\x99\x85', \
	'\xFE\x44\x00\x04\x02\x9A\x25','\xFE\x44\x00\x06\x02\x9B\x45', \
	'\xFE\x44\x00\x08\x02\x9F\x25','\xFE\x44\x00\x0A\x02\x9E\x45', \
	'\xFE\x44\x00\x0C\x02\x9D\xE5','\xFE\x44\x00\x0E\x02\x9C\x85', \
	'\xFE\x44\x00\x10\x02\x95\x25','\xFE\x44\x00\x12\x02\x94\x45']

	# Names of response used for Redis
	name = ["LPL_flt_ConcPC", "SPL_flt_ConcPC", \
	"MPL_flt_ConcPC", "P_Sensor0_flt", \
	"NTC0_Temp_flt", "NTC1_Temp_flt", \
	"NTC2_Temp_flt", "ADuCDie_Temp_Filtered", \
	"RH_Sensor0", "RH_Temp_Sensor0"]

	# Units multiple, based on SenseAir Documentation
	units = [0.1, 1, 1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

	response = []			#Empty list for sensor responses
	returnVals = []			# Empty list to store sensor key value pairs

	UNDEF = -9999.						# undefined value

	#===================== Read Data =====================

	K30IO = serial.Serial(IOdevice,baudrate =115200,timeout=1)	# connect to serial port
	K30IO.flushInput()						# flush serial input buffer
	time.sleep(0.01)
	i = 0						# sleep for 10 milliseconds

	# Request CO2 from sensor
	try:
		while i < len(command):					# Loop to read through command list
			K30IO.flushInput()				# flush serial $
			time.sleep(0.01)				# 10 milisecond pause
			K30IO.write(command[i])				# Send hex command to sensor from command list
			time.sleep(0.01)				# 10 milisecond pause for sensor
			K30out = K30IO.read(7)				# read 7 bytes from the sensor, store in list
			high = ord(K30out[3])				# high value is fourth byte
			low = ord(K30out[4])				# low value is fifth byte
			CO2 = ((high*256) + low)				# convert bytes to CO2 ppm value
			if CO2 > 65000:					# 16-bit so subtract to get negative values
				CO2 = CO2-65536
			CO2 = CO2 * units[i]				# Multiply by units value for correct response
			response.append(CO2)				# Add sensor responses to list
			i = i+1						# Increment for next command

	except:
		print("Error")						# store CO2 ppm value as undefined

	returnVals.append(sensorName)					# Add sensorname to list of return variables

	for x in range(len(command)):					# Loop to build sensor key value pairs list
		returnVals.append(name[x])				# Add response streamname
		returnVals.append(response[x])				# Add response value

	return returnVals						# Pass key values list back to calling program

if __name__ == '__main__':						# Allows this script to be called from other programs
	readSensors(sensorName)
