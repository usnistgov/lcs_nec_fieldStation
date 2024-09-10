#!/bin/bash

# This scriipt iterates over a REDIS stream for a specified interval and creates a json
# json message consisting of min. max and average for each of the key/value pairs
# in the stream.
#
# Syntax is:
#
#	redis_to_json [REDIS stream name] [# key value pairs in each reading] [duration of interval in seconds]
#
# The output of this script is generally piped as input to a publishing script which is run from cron at the
# same interval as the final parameter [duration of interval in seconds] in the call to the program above.

REDIS_STREAM=$1
NUM_KEY_VALUE_PAIRS=$2
INTERVAL_SECONDS=$3
MQTT_TOPIC=$4

MIN_INT=-9223372036854775808
MAX_INT=9223372036854775807
NEWLINE=$'\r\n'

# the while loop below will read output from the following redis query:
#
#	redis-cli XRANGE bme680 [unix time start] [unix time end]
#
# to see sample output for all points in the redis database execute the following query:
#
#	redis-cli XRANGE bme680 - +
#

# calculate query interval start and end time
# to do this get the current time and mod by 60
# then subtract the remainder from the current time
# to get end of last whole minute

epoch="$(date +'%s')"
secs=$((epoch%60))

# determine start and end times for redis query
# keys are in millis
# "000" needs to be appended to start
# "999" needs to be appended to end to get a full minute

epoch_end=$((epoch-secs))
epoch_start=$((epoch_end-INTERVAL_SECONDS))
epoch_end=$((epoch_end-1))
epoch_start_key=$epoch_start"000"
epoch_end_key=$epoch_end"999"

# initialize arrays

for (( i=0; i<$NUM_KEY_VALUE_PAIRS; i++))
do
  sums[$i]=0
  avgs[$i]=0
  mins[$i]=$MAX_INT
  maxs[$i]=$MIN_INT
  field[$i]=''
done

for (( i=0; i<$(( $NUM_KEY_VALUE_PAIRS*2 + 1)); i++))
do
  lines[$i]=0
done

# perform query and loop over data
# calculating min, max and average

count=0

# redis query returns all readings in the reques for the last INTERVAL_SECONDS seconds
# each 
#
# 1) 1) "1583598215562-0"
#     2)  1) "temperature"
#         2) "59"
#         3) "pressure"
#         4) "102515"
#         5) "humidity"
#         6) "4781"
#         7) "gas"
#         8) "726844"
#         9) "iaq_ac"
#        10) "1"
#        11) "iaq"
#        12) "8833"
#

# loop below calculates sum, min and max of each field
# sum is then used to calculate average

lines_per_rdg=$(( $NUM_KEY_VALUE_PAIRS*2 + 1 ))
first_loop=1
sensor_reading_count=0

linect=0
linect1=0

tline=''

while read -r tline; do 
  linect1=$((linect%lines_per_rdg))
  if ((first_loop == 0)) && ((linect1 == 0)); then
    sensor_reading_count=$((sensor_reading_count+1))
    for (( i=1; i<=$(( $NUM_KEY_VALUE_PAIRS*2 + 1)); i++)); do
      if (( ((i % 2)) == 1 )); then
        field[$(( (($i - 1)) / 2 ))]=${lines[i]}
      fi
      if (( ((i % 2)) ==  0 )); then
        tval=${lines[i]}
        key_val_pair_idx=$(( (($i - 2) / 2) % $NUM_KEY_VALUE_PAIRS))

        if [ 1 -eq "$(echo "${tval} < ${mins[$key_val_pair_idx]}" | bc)" ]; then
          mins[$key_val_pair_idx]=${tval}
        fi

        if [ 1 -eq "$(echo "${tval} > ${maxs[$key_val_pair_idx]}" | bc)" ]; then
          maxs[$key_val_pair_idx]=${tval}
        fi

        sums[$key_val_pair_idx]="$(echo "${tval} + ${sums[$key_val_pair_idx]}" | bc)"

        #echo $key_val_pair_idx' '${field[$(( (($i - 1)) / 2 ))]}' '$tval' '${mins[$key_val_pair_idx]}' '${maxs[$key_val_pair_idx]}' '${sums[$key_val_pair_idx]}
      fi

    done
  fi
  if ((first_loop == 1)); then
    first_loop=0
  fi
  lines[$(( linect % lines_per_rdg ))]=$tline
  linect=$((linect+1))
done < <(redis-cli XRANGE $REDIS_STREAM $epoch_start_key $epoch_end_key)

if ((sensor_reading_count > 0)); then

  printf "{   \"start_epoch\": $epoch_start_key,  \"end_epoch\": $epoch_end_key,  \"epoch\": $epoch_start,"
  printf "  \"count\": $sensor_reading_count,"
  printf "  \"topic\":  \"$MQTT_TOPIC \","
  for (( i=0; i<$NUM_KEY_VALUE_PAIRS; i++)); do
    avgs[i]=$(bc <<< "scale=5;(${sums[$i]} / $sensor_reading_count)")
    if ((i == $(($NUM_KEY_VALUE_PAIRS - 1)) )); then
      printf "  \""${field[$i]}"\": { \"average\": "${avgs[$i]}", \"min\": "${mins[$i]}", \"max\": "${maxs[$i]}" } "
    else
      printf "  \""${field[$i]}"\": { \"average\": "${avgs[$i]}", \"min\": "${mins[$i]}", \"max\": "${maxs[$i]}" }, "
    fi
  done
  printf "}"

fi

