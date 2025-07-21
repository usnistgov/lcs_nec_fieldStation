#!/bin/bash

# Revision of sensor_to_redis.sh to also create a dated csv log file of measurements for debugging
#       Original: T.P. Boyle 03/2020
#       Modified T.P. Boyle 07/2023: Added Meter ID and sensor location parameters
#       Modified T.P. Boyle 02/2024: Added support for i2c address input
#       Modified T.P. Boyle 07/2024: Shortened parameter names to reduce packet size, added m_sensor_type, m_cal environment variables
#       Modified T.P. Boyle 07/2025: Added debugging log file creation

SENSING_PROGRAM=$1
REDIS_MAX_RDGS=$2
while read -ra results ; do
        REDIS_STREAM="${results[0]}"
        unset 'results[0]'
        echo "${results[@]}"
        # Write to output file
        DATE=$(date +"%Y%m%d")
        OUTPUT_FILE="/home/meso3/log/${DATE}_${REDIS_STREAM}.txt"
        echo "${results[@]}" >> "$OUTPUT_FILE"
        echo "$REDIS_STREAM"
        echo "$REDIS_MAX_RDGS"
        echo "XADD $REDIS_STREAM MAXLEN ~ $REDIS_MAX_RDGS * ${results[@]}" | redis-cli &
done < <($SENSING_PROGRAM)
