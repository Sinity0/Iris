import sys
from time import sleep
import RPi.GPIO as GPIO
import ConfigParser
import datetime

print("Motion sensor script. v1.0")

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def motionSensor(channel):
	if GPIO.input(21):
		global counter
		counter += 1
		print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " Hostile entities detected!")
		config = ConfigParser.RawConfigParser()
		config.read(r'/home/pi/Relay/config.ini')

		config.set('Ventilation', 'isDoorOpen', 'True')

		with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
			config.write(configfile)

GPIO.add_event_detect(21, GPIO.RISING, callback=motionSensor, bouncetime=300)
counter = 0

try:
	while True:
		sleep(1)
finally:
	GPIO.cleanup()
	print (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + " Powering doww...")
