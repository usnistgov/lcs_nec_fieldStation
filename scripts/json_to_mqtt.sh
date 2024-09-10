#!/bin/bash
#
# This script creates a json message, appends the proper metrics file to it, and then sends it to an mqtt broker.
#
# 	Original: T.P. Boyle 04/2020
#	Modified: T.P. Boyle 08/2024 -  Modified to add metrics packet via jq, send to local MQTT bridge
#
# Syntax
# 	bash /home/meso3/scripts/json_to_mqtt.sh [redis_stream] [# key values] [avg_window] [topic]

REDIS_STREAM_NAME=$1
NUM_KEY_VAL_PAIRS=$2
INTERVAL_SECONDS=$3
MQTT_BROKER="127.0.0.1"
MQTT_TOPIC=$4

#MQTT_ID="${HOSTNAME}-${USER}"
MQTT_ID=$8
MESSAGE_FILE="./${REDIS_STREAM_NAME}_msg.json"
SCRATCH_FILE="./${REDIS_STREAM_NAME}_scratch.json"
METRICS_FILE="./metrics_jsons/${REDIS_STREAM_NAME}_metrics.json"

cd /home/meso3/scripts

python3 ./redis_to_json.py $REDIS_STREAM_NAME $NUM_KEY_VAL_PAIRS $INTERVAL_SECONDS $MQTT_TOPIC > $MESSAGE_FILE
jq -s '.[0] * .[1]' $MESSAGE_FILE $METRICS_FILE > $SCRATCH_FILE && mv $SCRATCH_FILE $MESSAGE_FILE
file_size=$(wc -c $MESSAGE_FILE | awk '{print $1}')
if ((file_size > 0)); then
  mosquitto_pub -q 1 -h $MQTT_BROKER -t $MQTT_TOPIC -f "$MESSAGE_FILE"
fi
