#/usr/bin/python3.9
'''
checkConc.py
Developed to change concentration side environmental chamber and output results with stdout

History
	Original: T.P. Boyle 12/2022

Syntax
	python3 checkConc.py [conc_json_file] [mqtt_topic]
'''

import sys
import json
import time
import RPi.GPIO as GPIO
import os

def buildOutputJson(startTime, endTime, topic):
	echo_json = {
		"epoch": int(time.time()),
		"topic": topic,
		"current_conc": pic_data['co2_dry']['average'],
		"reqested_conc": req_conc,
		"requested_thresh": req_threshold,
		"enrichment_time": enrich_time,
		"valve_open": startTime,
		"valve_close": endTime
		}
	return echo_json

def openValve(openTime):
	try:
		GPIOPin = 20
		LEDpin = 12
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(GPIOPin,GPIO.OUT)    # Initialize GPIO Pin
		GPIO.setup(LEDpin,GPIO.OUT)
		GPIO.output(GPIOPin,GPIO.HIGH)  # Open valve
		GPIO.output(LEDpin,GPIO.LOW)

		timeOpened = int(time.time())
		time.sleep(openTime)		# block program for time without killing cpu

		GPIO.output(GPIOPin,GPIO.LOW)
		GPIO.output(LEDpin,GPIO.HIGH)
		timeClosed = int(time.time())

	
	except KeyboardInterrupt:						# if ctrl+c, close valve
		GPIO.output(GPIOPin,GPIO.LOW)
		GPIO.output(LEDpin,GPIO.HIGH)
		timeClosed = int(time.time())
		
	GPIO.cleanup()
	return [timeOpened, timeClosed]


JSON_FILE = str(sys.argv[1])
MQTT_TOPIC = str(sys.argv[2])

enrich_time_max = 120								# max # of sec to open valve for

conc_json = open(JSON_FILE)							# open json file
req_data = json.load(conc_json)							# save json object as a python dictionary
conc_json.close()								# good practice, close json file when done reading

req_conc = float(req_data['concentration'])
req_threshold = float(req_data['threshold'])


# build in exception, if empty file, wait x amount of time and try certain retry

data_json = open('/home/meso3/ramdisk/picarro_msg.json')			# read most recent picarro packet

while os.path.getsize('/home/meso3/ramdisk/picarro_msg.json') < 600:		# stall program until picarro message file exists
	#print("File not complete, waiting for sys to create file")		# DEBUG
	time.sleep(1)

pic_data = json.load(data_json)							# parse data from json, store as dict
data_json.close()

last_conc = pic_data['co2_dry']['average']					# dictionary w/ multiple values, get average value
delta = req_conc - last_conc

if delta > 0 and delta > abs(req_threshold):					# if delta is positive AND outside of threshold
	enrich_time = (delta + 1.6975)/1.8982
	
	if enrich_time > enrich_time_max:					# only allow valve to be opened for certain time
		enrich_time = enrich_time_max
		#print("Calculated enrichment time exceeds max allowable amount, using max amount")	# DEBUG
	
	#print("Current Chamber Concentration: ", last_conc, " ppm")		# DEBUG
	#print("Concentration difference: ", delta, " ppm");			# DEBUG
	#print("Opening Valve for ", enrich_time, " seconds")			# DEBUG
	open_summary = openValve(enrich_time)
	json_packet = buildOutputJson(open_summary[0], open_summary[1], MQTT_TOPIC)
	print(json.dumps(json_packet))
	sys.stdout.flush()


elif delta < abs(req_threshold):						# if delta w/in threshold, create packet + exit
	enrich_time = 0
	json_packet = buildOutputJson(int(time.time()), int(time.time()), MQTT_TOPIC)
	print(json.dumps(json_packet))
	sys.stdout.flush()
	#print("Requested concentration is within threshold")			# DEBUG
	sys.exit()

else:										# if req conc < current conc, create packet + exit
	enrich_time = 0
	json_packet = buildOutputJson(int(time.time()), int(time.time()), MQTT_TOPIC)
	print(json.dumps(json_packet))
	sys.stdout.flush()
	#print("Requested concentration is lower than current concentration")	# DEBUG
	sys.exit()





