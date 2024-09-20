!/usr/bin/env python3

# redis_to_json.py
#       Original: T.P. Boyle 06/2021
#       Modified: T.P. Boyle 06/2024 - Added support for "m_" parameters
#       Modified: T.P. Boyle 07/2024 - supports use of strings for "m_" parameters, pulling of stn_id from environment variables
#       Modified: T.P. Boyle 09/2024 - Instead of using m_parameters, script detects if variables are not float and doesn't average them
#
# Script designed to be run as a cronjob on the station, used to grab specific data from Redis,
#       calculate statistics, and export a json to be grabbed by the MQTT agent.
#
# Syntax
# python3 redis_to_json.py [redis_stream] [#_key_value_pairs] [averaging_interval_seconds] [mqtt_topic]


import redis
import sys
import time
import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv("/etc/environment")

REDIS_STREAM = str(sys.argv[1])
NUM_KEY_VALUE_PAIRS = int(sys.argv[2])
INTERVAL_SECONDS = int(sys.argv[3])  # If INTERVAL_SECONDS=1, then not averaging
MQTT_TOPIC = str(sys.argv[4])

# Calculate query interval start and end time
epoch = int(np.floor(time.time()))
secs = epoch % 60

# Determine start and end times for redis query
if INTERVAL_SECONDS == 0:
    average = False
else:
    average = True

epoch_end = epoch - secs
epoch_start = epoch_end - INTERVAL_SECONDS
epoch_end = epoch_end - 1
epoch_start_key = str(epoch_start) + "000"
epoch_start_key = int(epoch_start_key)
epoch_end_key = str(epoch_end) + '999'
epoch_end_key = int(epoch_end_key)

# Create empty lists to hold stats parameters for each key value
avgs = []
sdevs = []

r = redis.Redis(host='localhost', port=6379, db=0)

if average:
    msg = r.xrange(REDIS_STREAM, epoch_start_key, epoch_end_key)
else:
    msg = r.xrevrange(REDIS_STREAM, '+', '-', count=1)

# Create dictionary to hold message values
vals = {}
key_names = []

for entry in msg:
    entry_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in entry[1].items()}
    if not key_names:
        key_names = list(entry_data.keys())
        vals = {key: [] for key in key_names}

    for key in key_names:
        val = entry_data[key]
        try:
            # Try converting to float, if fails, keep as string
            val = float(val)
            vals[key].append(val)
        except ValueError:
            vals[key].append(val)

# Only average parameters that are not strings
filtered_keys = [key for key in key_names if isinstance(vals[key][0], float)]

if average:
    filtered_vals = {key: np.array(vals[key]) for key in filtered_keys}
    avg = {key: np.mean(filtered_vals[key]).round(2) for key in filtered_vals}
    sdev = {key: np.std(filtered_vals[key]).round(2) for key in filtered_vals}

data_file = {
    "epoch": epoch,
    "start_epoch": epoch_start,
    "end_epoch": epoch_end,
    "count": len(msg),
    "topic": MQTT_TOPIC,
    "s_name": REDIS_STREAM,
    "stn_id": os.getenv("STN_NAME"),
    "stn_loc": os.getenv("STN_LOC")
}

if average:
    for key in key_names:
        if key in filtered_vals:
            data_file[key] = {
                "average": avg[key],
                "sdev": sdev[key]
            }
        else:
            last_value = vals[key][-1]  # Get the last value for this key
            data_file[key] = last_value
else:
    for key in key_names:
        last_value = vals[key][-1]
        data_file[key] = last_value

print(json.dumps(data_file, indent=2))
