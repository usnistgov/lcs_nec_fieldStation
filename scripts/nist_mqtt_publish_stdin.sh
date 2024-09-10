#!/bin/bash
# Script reads a single line from stdin and publishes it to a broker

# designed to call a program which outputs json with data. mosquitto_pub them publishes the data to the broker

#       History:
#               Original: T.P. Boyle 1/2022
#               Modified: T.P. Boyle 12/2022 - Revised to use jq, pull topic from packet and parsee
#               Modified: T.P. Boyle 09/2023 - added support for password-based mqtt login
#		Modified: T.P. Boyle 08/2024 - changed publishing to use local mqtt bridge for AWS, add metrics to packet
#
# Syntax
#       SENSING_PROGRAM [mqtt_topic] | mqtt_publish_singleLine.sh 

cd /home/meso3/scripts

MQTT_BROKER="127.0.0.1"

read -r line

MQTT_TOPIC=$(echo $line | jq -r '.topic')

TOPIC_PREFIX=$(echo "$MQTT_TOPIC" | cut -d'/' -f1)

# parse topic, select appropriate sensor type for metrics
if [ "$TOPIC_PREFIX" = "st" ]; then
    SENSOR_TYPE=$(echo $line | jq -r '.m_sensor_type')
elif [ "$TOPIC_PREFIX" = "cl" ]; then
    SENSOR_TYPE=$(echo $line | jq -r '.cal_type')
else
    echo "Unknown topic prefix: $TOPIC_PREFIX"
    exit 1
fi

MESSAGE_FILE="./${SENSOR_TYPE}_msg.json"
METRICS_FILE="./metrics_jsons/${SENSOR_TYPE}_metrics.json"
SCRATCH_FILE="./${SENSOR_TYPE}_scratch.json"

echo $line > $MESSAGE_FILE

jq -s '.[0] * .[1]' $MESSAGE_FILE $METRICS_FILE > $SCRATCH_FILE && mv $SCRATCH_FILE $MESSAGE_FILE

mosquitto_pub -q 1 -h $MQTT_BROKER -t $MQTT_TOPIC -f "$MESSAGE_FILE"
