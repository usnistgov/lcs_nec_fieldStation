# Script used to query BME280, utilize system environment variables

# Modified code from Adafruit (learn.adafruit.com)
# 	Original: T.P. Boyle 3/2020
# 	Modified T.p. Boyle 10/2020
# 	Modified T.P. Boyle 02/2022: Adafruit updated library, updated code
#	Modified T.P. Boyle 07/2023: Added Meter ID and sensor location parameters
#	Modified T.P. Boyle 02/2024: Added support for i2c address input
#	Modified T.P. Boyle 07/2024: Shortened parameter names to reduce packet size, added m_sensor_type
#	Modified T.P. Boyle 09/2024: Added pkt_type parameter to output for validation

# Read temperature, pressure, and humidity from BME280
#	and print rounded observations to stdout
# Must pass stream name into program

# python3 readBME.py [redis_stream] [meter_id] [sensor_location]

import board
from adafruit_bme280 import basic as adafruit_bme280
import sys

sensorName = sys.argv[1]
meterID = sys.argv[2]
sensorLoc = sys.argv[3]
addr = int(sys.argv[4])

if addr == 77:          # default address 0x77
        a = 119         # convert to int of hex aadr

else:                   # modifiable for addr 0x76
        a = 118

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,address=a)

print(sensorName, "temp", round(bme280.temperature,2), "pres", round(bme280.pressure, 2), "rh", round(bme280.humidity,0), "m_meter_id", meterID, "m_sensor_location", sensorLoc, "m_sensor_type", "bme280", "pkt_type", "bme280")
