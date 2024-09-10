#!/bin/bash

# Wrapper program used to run BME280 sensors 
#	Original: T.P. Boyle 03/2020
#	Modified T.P. Boyle 07/2023: Added Meter ID and sensor location parameters
#	Modified T.P. Boyle 02/2024: Added support for i2c address input 
#	Modified T.P. Boyle 07/2024: Shortened parameter names to reduce packet size, added m_sensor_type, m_cal environment variables

source /etc/environment

while true
do
	python3 /home/meso3/bme/readBME.py $BME_SNAME $BME_ID $BME_LOC $BME_ADDR
	sleep 3
done
