# Executable shell script to read multiple sensors at a certain interval
# BE SURE TO MAKE EXECUTABLE!
#	chmod +x

while true
do
	python /home/meso3/co2/readSensors/multi_poll_sensors_output.py
	sleep 1
done
