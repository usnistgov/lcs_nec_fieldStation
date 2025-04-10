#!/usr/bin/python3.9
# readPicarro_dict.py
# Python script to read Picarro serial data stream and add to redis. Note that
#	var names are hard-coded
#
# 	History
#	Original: T.P. Boyle, 02/2022
#	Modified: T.P. Boyle, 02/2023
#		Changed to 
#
# USAGE
#	./readPicarro_dict.py [redis_stream] [max_len_entries]
	

import serial
import numpy
import time
import redis
import sys

def Convert(a):				# Needed to convert list to dict for redis
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

ser = serial.Serial(port="/dev/ttyUSB0",baudrate=19200,bytesize=8,stopbits=1,parity="N")

# HARD_CODED Picarro variables, will change with machine
var_names = ["epoch","cavity_press","cavity_temp", \
"das_temp","species","mpv_position","outlet_valve", \
"co2","co2_dry","ch4","ch4_dry","h2o","extra_1","extra_2"]

returnVals = []

#REDIS_STREAM = str(sys.argv[1])
#REDIS_STREAM = 'picarro'
#MAX_LEN = int(sys.argv[2])			# Num. of entries redis will save

#r = redis.Redis(host='localhost', port=6379, db=0) # Open redis

species_select = 3				# b/c Picarro returns duplicates, only add one species to redis

while True:
	results = ser.readline()		# Read serial port, add newline after each mesg
	s = results.decode("utf-8")		# readline() returns in bytes, convert to string
	new_s = s.split()			# split string entries
	returnVals.append('time_rcvd')		# add time recieved by pi
	returnVals.append(int(time.time()))

	for x in range(len(new_s)):		# Loop building key-value pairs for redis
		returnVals.append(var_names[x])
		returnVals.append(new_s[x])

	returnVals_dict = Convert(returnVals)


	if (len(new_s) > 13):			# Picarro sometimes returns incomplete messages, ignore those
		if float(new_s[4]) == species_select:		# run nested because short messages cause errors
			print(*returnVals)			# Print array without qoutes
			#r.xadd(REDIS_STREAM, returnVals_dict, maxlen=MAX_LEN)

	returnVals = []			# clear variables
