#!/bin/bash
# Script reads a single line from stdin and routes it for local loggin

# designed to call a program which outputs json with data. mosquitto_pub them publishes the data to the broker

#       History:
#               Original: T.P. Boyle 1/2022
#               Modified: T.P. Boyle 12/2022 - Revised to use jq, pull topic from packet and parsee
#               Modified: T.P. Boyle 09/2023 - added support for password-based mqtt login
#		Modified: T.P. Boyle 08/2024 - changed publishing to use local mqtt bridge for AWS, add metrics to packet
#		Modified: T.P. Boyle 08/2025 - modified for local logging

# Syntax
#       SENSING_PROGRAM [mqtt_topic] | stdin_jdon_to_log.sh 

cd /home/meso3/scripts

read -r line

# pull mqtt topic type
MQTT_TOPIC=$(echo $line | jq -r '.topic')
TOPIC_PREFIX=$(echo "$MQTT_TOPIC" | cut -d'/' -f1)

# pull sensor type based on topic (either calibration or stats)
if [ "$TOPIC_PREFIX" = "st" ]; then
    SENSOR_TYPE=$(echo $line | jq -r '.m_sensor_type')
elif [ "$TOPIC_PREFIX" = "cl" ]; then
    SENSOR_TYPE=$(echo $line | jq -r '.cal_type')
else
    echo "Unknown topic prefix: $TOPIC_PREFIX"
    exit 1
fi

MESSAGE_FILE="./${SENSOR_TYPE}_msg.json"
echo $line > $MESSAGE_FILE		# echo to temp message file so flatten_json.py works

DATE_DIR=$(date +"%Y%m%d")
LOG_DIR="/home/meso3/stn_logs/${DATE_DIR}"
OUTPUT_FILE="${LOG_DIR}/${DATE_DIR}_${SENSOR_TYPE}.csv"
mkdir -p $LOG_DIR

python3 flatten_json.py $MESSAGE_FILE $OUTPUT_FILE
