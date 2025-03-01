#!/usr/bin/python3.9

# Script used in conjunction with runCals.sh to grab json packets returned by each process, append them to one summary json sent to MQTT
#
# 	Original: T.P. Boyle 07/2024

import json
import sys
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv("/etc/environment")	# used to load environment variables from /etc/environment 

def combine_jsons(file1, file2, file3, file4, mqtt_topic):
	with open(file1, 'r') as f1, open(file2, 'r') as f2, open(file3, 'r') as f3, open(file4, 'r') as f4 :
		data1 = json.load(f1)
		data2 = json.load(f2)
		data3 = json.load(f3)
		data4 = json.load(f4)
	
	epoch = int(time.time())	
	
	combined_result = {
		"valve 1": {
			"valve_open": data1["valve_open"],
			"valve_closed": data1["valve_close"],
			"tank_conc": data1["tank_conc"],
			"tank_num": data1["tank_num"]
        	},
		"valve 2": {
			"valve_open": data2["valve_open"],
			"valve_closed": data2["valve_close"],
			"tank_conc": data2["tank_conc"],
                        "tank_num": data2["tank_num"]
		},
		"emc2101": {
			"fan_low_epoch": data3["epoch"],
			"fan_low_dc": data3["duty_cycle"],
			"fan_high_epoch": data4["epoch"],
			"fan_high_dc": data4["duty_cycle"]
		},
		"topic": mqtt_topic,
		"cal_type": "co2",
		"stn_id": os.getenv("STN_NAME"),
		"stn_loc": os.getenv("STN_LOC"),
		"calibrated_sensor": os.getenv("ACTIVE_SENSOR_CAL"),
		"cal_start_epoch": data1["valve_open"] 
		#"cal_start_epoch": epoch - ( epoch % 3600)
	}
	# other parameters to add in: sensor(s) being calibrated,station_id
	print(json.dumps(combined_result, indent=4))

if __name__ == "__main__":
	if len(sys.argv) != 6:
		print("Usage: python3 combine_jsons.py <json_400ppm> <json_600ppm> <json_fan_low> <json_fan_high> <mqtt_topic>")
		sys.exit(1)

	os.chdir("/home/meso3/co2/calibrateSys")

	file1 = sys.argv[1]
	file2 = sys.argv[2]
	file3 = sys.argv[3]
	file4 = sys.argv[4]
	topic = str(sys.argv[5])

	combine_jsons(file1, file2, file3, file4, topic)
	
