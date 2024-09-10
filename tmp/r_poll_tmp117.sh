#!/bin/bash

# Wrapper program used to run TMP117 sensors 
#	Original: T.P. Boyle 07/2020
#	Modified T.P. Boyle 07/2023: Added Meter ID and sensor location parameters
#	Modified T.P. Boyle 02/2024: Added support for i2c address input 
#	Modified T.P. Boyle 07/2024: Shortened parameter names to reduce packet size, added m_sensor_type, m_cal environment variables

source /etc/environment		# force script to use environment variables

while true
do
	python3 /home/meso3/tmp/readTMP.py $TMP_SNAME $TMP_ID $TMP_LOC $TMP_ADDR	# using adjusting env. variables
	sleep 3
done
