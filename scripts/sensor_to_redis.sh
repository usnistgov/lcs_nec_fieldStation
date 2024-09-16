#!/bin/bash
#
# This script creates a json message, appends the proper metrics file to it, and then sends it to an mqtt broker.
#
# 	Original: T.P. Boyle 04/2020
#
# Syntax
# 	bash /home/meso3/scripts/sensor_to_redis.sh <sensor_program> <max # readings to save> 


SENSING_PROGRAM=$1
REDIS_MAX_RDGS=$2

while read -ra results ; do
        REDIS_STREAM="${results[0]}"
	unset 'results[0]'
	echo ${results[@]}
	echo $REDIS_STREAM
	echo $REDIS_MAX_RDGS
	echo 'XADD '$REDIS_STREAM' MAXLEN ~ '$REDIS_MAX_RDGS' * '${results[@]} | redis-cli &
done < <($SENSING_PROGRAM)

