# Script used to query TMP117, utilize system environment variables
#
# Modified Code from Adafruit (learn.adafruit.com)
#
# 	Original: T.P. Boyle 07/2020
#	Modified: T.P. Boyle 07/2023: Added meter ID and sensor location parameters
#	Modified: T.P. Boyle 02/2024: Added support for i2c address input
#	Modified: T.P. Boyle 07/2024: Shortened parameter names for smaller packet sizes, added m_sensor_type
#	Modified: T.P. Boyle 09/2024: Added pkt_type parameter for AWS validation
#
# Read temperature from a TMP117 and print measurement to stdout
#
# python3 readTMP.py [redis_stream] [meter_id] [sensor_location] [i2c_address]

import time
import board
import adafruit_tmp117
import sys

m_sensorName = sys.argv[1]
m_meterID = sys.argv[2]
m_sensorLoc = sys.argv[3]
addr = int(sys.argv[4])

if addr == 48:          # default addr is 0x48
        a = 72          # pass hex addr as int
else:                   # alternative addr is 0x49 via solderpads
        a = 73


i2c = board.I2C()  # uses board.SCL and board.SDA
tmp117 = adafruit_tmp117.TMP117(i2c, address=a)

print(m_sensorName, "temp", round(tmp117.temperature,2), "m_meter_id", m_meterID, "m_sensor_location", m_sensorLoc, "m_sensor_type","tmp117", "pkt_type","tmp117")

