
# Script used to turn on K96 sensors using GPIO with current board toggle pin in GPIO26

# Original: T.P. Boyle 07/2021

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(26,GPIO.OUT) 

GPIO.output(26,GPIO.HIGH)
