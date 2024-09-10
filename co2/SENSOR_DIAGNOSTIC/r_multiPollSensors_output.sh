# Executable shell script to read multiple sensors at a certain interval
# BE SURE TO MAKE EXECUTABLE!
#	chmod +x

while true
do
	python /home/meso3/co2/readSensors/multi_poll_sensors_output.py
	#python /home/meso3/ramdisk/multi_poll_sensors.py
	#sleep 3	#original setup,with 10 only reads 4-5 times a min
	sleep 1
done
