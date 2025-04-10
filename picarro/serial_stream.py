#!/usr/bin/python3.9

import serial

ser = serial.Serial(port="/dev/ttyUSB0",baudrate=19200,bytesize=8,stopbits=1,parity="N")

while True:
	results = ser.readline()
	print(results)

