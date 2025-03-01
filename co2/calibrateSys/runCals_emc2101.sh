#!/bin/bash
source /etc/environment

# Script designed to run a station calibration procedures, stamp all output params to a cal. Sequence json
# 
# 	Original: T.P. Boyle 07/2024

cd /home/meso3/co2/calibrateSys

# reduce fan speed for calibration
python3 /home/meso3/emc2101/json_adjFanSpeed.py 15 st/raw/$STN_OWNER/$STN_LOC/$STN_NAME/emc2101/dutyCycle > temp_fan_reduce.json
sleep 5

# run calibration, valve 1, 400ppm cylinder
python3 /home/meso3/co2/calibrateSys/run_calibration_switcher.py 1 $CAL_TIME cl/raw/$STN_OWNER/$STN_LOC/$STN_NAME/cal_val1 $TANK_CONC_400 $TANK_NUM_400 $ACTIVE_SENSOR_CAL > temp_cal_400.json
sleep 5

# run calibration, valve 2, 600ppm cylinder
python3 /home/meso3/co2/calibrateSys/run_calibration_switcher.py 2 $CAL_TIME cl/raw/$STN_OWNER/$STN_LOC/$STN_NAME/cal_val2 $TANK_CONC_600 $TANK_NUM_600 $ACTIVE_SENSOR_CAL > temp_cal_600.json
sleep 5
python3 /home/meso3/emc2101/json_adjFanSpeed.py 30 st/raw/$STN_OWNER/$STN_LOC/$STN_NAME/emc2101/dutyCycle > temp_fan_increase.json

output=$(python3 combineJsons.py temp_cal_400.json temp_cal_600.json temp_fan_reduce.json temp_fan_increase.json cl/raw/$STN_OWNER/$STN_LOC/$STN_NAME/co2_cal)

# Print the final combined JSON output
echo $output

