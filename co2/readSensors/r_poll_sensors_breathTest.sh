#!/bin/bash

# Wrapper program used to run UART-based sensors/MUX FOR BREATH TESTS
# Original: T.P. Boyle 07/2020

while true
do
	python /home/meso3/co2/readSensors/raw_poll_sensors_breathTest.py
	sleep 3
done
