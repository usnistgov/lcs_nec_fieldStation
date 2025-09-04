#!/bin/bash
#
# This script creates a json message, appends the proper metrics file to it, and routes it to a python program to flatten/export to a csv
#
# 	Original: T.P. Boyle 04/2020
#	Modified: T.P. Boyle 08/2024 -  Modified to add metrics packet via jq, send to local MQTT bridge
#	Modifief: T.P. Boyle 08/2025 - Modified to support local logging for offline stations
#
# Syntax
# 	bash /home/meso3/scripts/json_to_mqtt.sh [redis_stream] [# key values] [avg_window] [topic]

REDIS_STREAM_NAME=$1
NUM_KEY_VAL_PAIRS=$2
INTERVAL_SECONDS=$3
MQTT_BROKER="127.0.0.1"
MQTT_TOPIC=$4

MESSAGE_FILE="./${REDIS_STREAM_NAME}_msg.json"

cd /home/meso3/scripts

python3 ./redis_to_json.py $REDIS_STREAM_NAME $NUM_KEY_VAL_PAIRS $INTERVAL_SECONDS $MQTT_TOPIC > $MESSAGE_FILE
file_size=$(wc -c $MESSAGE_FILE | awk '{print $1}')
if ((file_size > 0)); then
  DATE_DIR=$(date +"%Y%m%d")
  LOG_DIR="/home/meso3/stn_logs/${DATE_DIR}"
  OUTPUT_FILE="${LOG_DIR}/${DATE_DIR}_${REDIS_STREAM_NAME}.csv"
  mkdir -p $LOG_DIR
  
  python3 /home/meso3/scripts/flatten_json.py $MESSAGE_FILE $OUTPUT_FILE
fi
