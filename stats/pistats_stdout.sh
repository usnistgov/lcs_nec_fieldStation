#!/usr/bin/env bash
# pistats_stdout.sh

# Script to check  operating stats from a Raspberry Pi

# Necessary installed packages:
#	sysstat

#	History
#	Original: T.P. Boyle 02/2020
#	Modified: T.P. Boyle 12/2022 - Added more output paramaters
#	Modified: T.P. Boyle 07/2024 - added "m_sensor_type", "stn_id", and "stn_loc" parameters to everything
#	Modified: T.P. Boyle 09/2024 - added pkt_type for AWS validation

# Syntax
#	bash pistats_stdout.sh [topic]

source /etc/environment

MQTT_TOPIC=$1

cpuidl="$(mpstat | grep all | awk '{print $12}')"
cpu="$(mpstat | grep all | awk '{print $3}')"
cpusys="$(mpstat | grep all | awk '{print $5}')"
cpuio="$(mpstat | grep all | awk '{print $6}')"
totmem="$(free | grep Mem | awk '{print $2}')"
usemem="$(free | grep Mem | awk '{print $3}')"
freemem="$(free | grep Mem | awk '{print $4}')"
cputemp="$(vcgencmd measure_temp | awk -F "[=']" '{print $2}')"
epoch="$(date +'%s')"
netsig="$(iwconfig wlan0 | grep Link | awk '{print $4}' | awk -F'level=' '{print $2}' | awk -F'/' '{print $1}')"
stats="$epoch $cpu $cpuidl $totmem $usemem $freemem $netsig"
json="{\"epoch\": $epoch, \"topic\": \"$MQTT_TOPIC\", \"cpu\": { \"user\": $cpu, \"idle\": $cpuidl, \"iowait\": $cpuio, \"sys\": $cpusys}, \"memory\": { \"total\": $totmem, \"used\": $usemem, \"free\": $freemem }, \"cputemp\": $cputemp, \"m_sensor_type\":\"system\", \"stn_id\":\"$STN_NAME\", \"stn_loc\":\"$STN_LOC\", \"pkt_type\":\"pistats\"}"

echo $json 
