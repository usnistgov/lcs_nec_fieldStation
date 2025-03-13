import time
import board
import adafruit_sht31d
import sys

i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

m_sensorName = sys.argv[1]
m_meterID = sys.argv[2]
m_sensorLoc = sys.argv[3]

temp = round(sensor.temperature, 2)
rh = round(sensor.relative_humidity, 2)

print(
	m_sensorName,
	"temp",
	temp,
	"relative_humidity",
	rh,
	"m_meter_id",
	m_meterID,
	"m_sensor_location",
	m_sensorLoc,
	"m_sensor_type",
	"sht30",
	"pkt_type",
	"sht30"
)
