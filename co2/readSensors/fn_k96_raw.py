#!/usr/bin/env python3
# Function-based program used to query K96 processed/raw measurements
'''
	History: Basis courtesy of Cory Martin and Ning Zeng
		Original: T.P. Boyle 09/2020
		Modified: T.P. Boyle 07/2021 - supports functionality and raw bytes
		Modified: T.P. Boyle 02/2022 - switched from python 2 -> python 3
		Modified: T.P. Boyle 06/2024 - Adjusted meter id parameter to fit "m_" metadata standards
		Modified: T.P. Boyle 07/2024 - Added m_cal parameter for AWS synchronization, added serial.close(), manually added m_sensor_location & m_sensor_type
		Modified: T.P. Boyle 09/2024 - Added pkt_type parameter for AWS validation, revised U32 memory read (meter_id) to be an string for sensor_to_redis.py, added pkt_type parameter for AWS infrastructure

# Note, you want to return all responses in key value pairs through a LIST!

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
	command_s16 = [b'\xFE\x44\x00\x00\x02\x98\xE5',b'\xFE\x44\x00\x02\x02\x99\x85', \
	b'\xFE\x44\x00\x04\x02\x9A\x25',b'\xFE\x44\x00\x06\x02\x9B\x45', \
	b'\xFE\x44\x00\x08\x02\x9F\x25',b'\xFE\x44\x00\x0A\x02\x9E\x45', \
	b'\xFE\x44\x00\x0C\x02\x9D\xE5',b'\xFE\x44\x00\x0E\x02\x9C\x85', \
	b'\xFE\x44\x00\x10\x02\x95\x25',b'\xFE\x44\x00\x12\x02\x94\x45', \
	b'\xFE\x44\x04\x2A\x02\xC6\x44',b'\xFE\x44\x04\x4A\x02\xEE\x44', \
	b'\xFE\x44\x03\x8A\x02\x0F\x85',b'\xFE\x44\x03\xAA\x02\x16\x45', \
	b'\xFE\x44\x04\x8A\x02\xBE\x44',b'\xFE\x44\x04\xAA\x02\xA7\x84'
]
	
	# List for raw commands
	command_s32 = [b'\xFE\x44\x01\x80\x04\x28\xE7',b'\xFE\x44\x01\x90\x04\x25\x27', \
	b'\xFE\x44\x03\x60\x04\xC0\xE7', b'\xFE\x44\x01\x70\x04\x6C\xE7', \
	b'\xFE\x44\x01\x74\x04\x6E\x27',b'\xFE\x44\x01\x78\x04\x6B\x27', \
	b'\xFE\x44\x01\x7C\x04\x69\xE7',b'\xFE\x44\x03\x50\x04\xD4\xE7', \
	b'\xFE\x44\x03\x54\x04\xD6\x27']
	
	command_s32_16 = [b'\xFE\x44\x01\x84\x06\xAB\xE6',b'\xFE\x44\x01\x94\x06\xA6\x26', \
	b'\xFE\x44\x03\x64\x06\x43\xE6']

	command_u32 = [b'\xFE\x44\x00\x28\x04\x06\xE7']
	
	# Names of response used for Redis
	name = ["LPL_flt_ConcPC", "SPL_flt_ConcPC", \
	"MPL_flt_ConcPC", "P_Sensor0_flt", \
	"NTC0_Temp_flt", "NTC1_Temp_flt", \
	"NTC2_Temp_flt", "ADuCDie_Temp_Filtered", \
	"RH_Sensor0", "RH_Temp_Sensor0", \
	'LPL_uflt_conc', 'LPL_flt_conc', \
	'MPL_uflt_conc', 'MPL_flt_conc', \
	'SPL_uflt_conc', 'SPL_flt_conc', \
	'LPL_Signal','SPL_Signal', \
	'MPL_Signal','LPL_Signal_Low', \
	'LPL_Signal_High','SPL_Signal_Low', \
	'SPL_Signal_High','MPL_Signal_Low', \
	'MPL_Signal_High','LPL_Signal_filtered', \
	'SPL_Signal_filtered','MPL_Signal_filtered', \
	'm_meter_id']

	
	# Units multiple, based on SenseAir Documentation
	units_s16 = [0.1, 1, 1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 1, 1, 1, 1]
	
		
	# Units multiple for RAW values
	units_s32 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	
	units_s32_16 = [1,1,1]

	units_u32 = [1]

	response = []			#Empty list for sensor responses
	returnVals = []			# Empty list to store sensor key value pairs

	UNDEF = -9999.						# undefined value

	#===================== Read Data =====================

	try:
		K30IO = serial.Serial(IOdevice,baudrate =115200,timeout=1)	# connect to serial port
	except serial.SerialException as e:
		print(f"Serial exception occured at {e}")
	except Exception as e:
		print(f"An unexpected error occured: {e}")

	K30IO.flushInput()						# flush serial input buffer
	time.sleep(0.01)
	i = 0
	j = 0
	k = 0
	m = 0								# Incrementor for units
	n = 0

	# Request CO2 from sensor
	try:
		#Read s16 memory addresses
		while i < len(command_s16):					# Loop to read through command list
			K30IO.flushInput()				# flush serial $
			time.sleep(0.01)				# 10 milisecond pause
			K30IO.write(command_s16[i])				# Send hex command to sensor from command list
			time.sleep(0.01)				# 10 milisecond pause for sensor
			K30out = K30IO.read(7)				# read 7 bytes from the sensor, store in list
			CO2 = bytes_to_s16(K30out[3], K30out[4], True)
			CO2 = CO2 * units_s16[i]				# Multiply by units value for correct response
			response.append(CO2)				# Add sensor responses to list
			i = i+1						# Increment for next command
			k = k+1
		
		# Read s32 memory addresses	
		while j < len(command_s32):					# Loop to read through command list
			K30IO.flushInput()				# flush serial $
			time.sleep(0.01)				# 10 milisecond pause
			K30IO.write(command_s32[j])				# Send hex command to sensor from command list
			time.sleep(0.01)				# 10 milisecond pause for sensor
			K30out = K30IO.read(9)				# read 7 bytes from the sensor, store in list
			CO2 = bytes_to_s32(K30out[3], K30out[4], K30out[5], K30out[5]) * units_s32[j]
			response.append(CO2)				# Add sensor responses to list
			j = j+1						# Increment for next command
			k = k+1

		# Read s32 memory addresses	
		while m < len(command_s32_16):					# Loop to read through command list
			K30IO.flushInput()				# flush serial $
			time.sleep(0.01)				# 10 milisecond pause
			K30IO.write(command_s32_16[m])				# Send hex command to sensor from command list
			time.sleep(0.01)				# 10 milisecond pause for sensor
			K30out = K30IO.read(11)				# read 7 bytes from the sensor, store in list
			CO2 = str(bytes_to_s32(K30out[3], K30out[4], K30out[5], K30out[6]))
			CO2_frac = str(bytes_to_s16(K30out[7], K30out[8],False))
			CO2 = CO2 + "." + CO2_frac			# Concentinate whole with fractional part
			response.append(CO2)				# Add sensor responses to list
			m = m+1						# Increment for next command
			k = k+1

		# NOTE: This is only reading meter_id (which needs to be a string). Revise if reading other U32 addresses
		while n < len(command_u32):
			K30IO.flushInput()                              # flush serial $
			time.sleep(0.01)                                # 10 milisecond pause
			K30IO.write(command_u32[n])                             # Send hex command to sensor from command list
			time.sleep(0.01)                                # 10 milisecond pause for sensor
			K30out = K30IO.read(9)                          # read 7 bytes from the sensor, store in list
			CO2 = (K30out[3] * 16**4) + (K30out[4] * 16**3) + (K30out[5] * 16**2) + K30out[6]
			CO2 = 'k96_' + str(CO2)			# add the k96 header, convert to a string and right format
			response.append(CO2)                            # Add sensor responses to list
			n = n+1                                         # Increment for next command
			k = k+1

	except:
		print("Error")						# store CO2 ppm value as undefined

	returnVals.append(sensorName)					# Add sensorname to list of return variables

	for x in range(len(name)):					# Loop to build sensor key value pairs list
		returnVals.append(name[x])				# Add response streamname
		returnVals.append(response[x])				# Add response value

	returnVals.append('m_cal')
	returnVals.append(2)
	returnVals.append('m_sensor_location')
	returnVals.append(1)
	returnVals.append('m_sensor_type')
	returnVals.append('k96')
	returnVals.append('pkt_type')
	returnVals.append('k96')
	
	K30IO.close()							# Close serial port before ending progra,

	return returnVals						# Pass key values list back to calling program

# Use False if unsigned integer
def bytes_to_s16(byte_2, byte_1, signed):
	value_s16 = ((byte_2<<1)>>1)*2**8 + byte_1	
	if byte_2>>7 == 1 and signed == True:
		sign = -1
	else:
		sign = 1
	value_s16 = value_s16*sign
	return value_s16

def bytes_to_s32(byte_4, byte_3, byte_2, byte_1):
	value_s32 = ((byte_4<<1)>>1)*2**24 + byte_3*2**16 + byte_2*2**8 + byte_1
	if byte_4>>7 == 1:
		sign = -1
	else:
		sign = 1
	value_s32 = value_s32 * sign
	return value_s32
	
if __name__ == '__main__':						# Allows this script to be called from other programs
	readSensors(sensorName)
