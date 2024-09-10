#!/bin/bash
#
# This script creates a json message and then sends it to an mqtt broker.
# In this case it creates the message from the bme680 REDIS stream and then publishes
# to the "dt/meso3/love/crawl/bme680" topic.
#
# It has benn added to CRON with a 2 minute interval.
#
# Syntax is:
#
#	json_to_mqtt [redis stream] [# key/val pairs] [interval] [mqtt topic]
#
# CRON entry is:
#
#	*/5 * * * * bash /home/meso3/scripts/json_to_mqtt.sh bme680 6 300 10.8.0.6 mosquitto_pub bup_ottiuqsom dt/meso3/love/crawl/bme680 > /dev/null 2>&1
#


REDIS_STREAM_NAME=$1
NUM_KEY_VAL_PAIRS=$2
INTERVAL_SECONDS=$3
MQTT_BROKER=$4
MQTT_USER=$5
MQTT_PASS=$6
MQTT_TOPIC=$7

#MQTT_ID="${HOSTNAME}-${USER}"
MQTT_ID=$8
MESSAGE_FILE="./${REDIS_STREAM_NAME}_msg.json"

cd /home/meso3/scripts

python3 ./redis_to_json.py $REDIS_STREAM_NAME $NUM_KEY_VAL_PAIRS $INTERVAL_SECONDS $MQTT_TOPIC > $MESSAGE_FILE
file_size=$(wc -c $MESSAGE_FILE | awk '{print $1}')
if ((file_size > 0)); then
  mosquitto_pub -u $MQTT_USER -P $MQTT_PASS -h $MQTT_BROKER -p 1883 -i $MQTT_ID -d -q 1 -t $MQTT_TOPIC -f $MESSAGE_FILE
fi
