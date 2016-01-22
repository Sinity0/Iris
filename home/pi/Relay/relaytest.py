#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sqlite3
import sys
import datetime

GPIO.setmode(GPIO.BCM)

pinList = [5, 6, 12, 13, 16, 19, 20, 26]

for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)

class ventControl:
	def __init__(self):
		#self.test()
		self.prevResult = "1"
		self.lastResult = "2"

	def test(self):
		sleepTime = 2
		try:
			GPIO.output(5, GPIO.LOW)
			print "ONE"
			time.sleep(sleepTime)
			GPIO.output(6, GPIO.LOW)
			print "TWO"
			time.sleep(sleepTime)
			GPIO.output(12, GPIO.LOW)
			print "THREE"
			time.sleep(sleepTime)
			GPIO.output(13, GPIO.LOW)
			print "FOUR"
			time.sleep(sleepTime)
			GPIO.output(16, GPIO.LOW)
			print "FIVE"
			time.sleep(sleepTime)
			GPIO.output(19, GPIO.LOW)
			print "SIX"
			time.sleep(sleepTime)
			GPIO.output(20, GPIO.LOW)
			print "SEVEN"
			time.sleep(sleepTime)
			GPIO.output(26, GPIO.LOW)
			print "EIGHT"
			time.sleep(sleepTime)
			GPIO.cleanup()
			print "bye"
		except KeyboardInterrupt:
			print " Quit"

	def getLastRecord(self):
		self.con = sqlite3.connect("/home/pi/dht.db")
		self.data = "1"

		with self.con:
			cursor = self.con.cursor()
			for self.row in cursor.execute("SELECT * FROM meteolog ORDER BY date DESC LIMIT 1"):
				self.data = self.row
			self.con.commit()
		self.con.close()
		self.data = str(self.data).replace(')','').replace('(','').replace('u\'','').replace("'","")
		self.lastResult=self.data
 		return self.data

main = ventControl()
rec = main.getLastRecord()
print(rec)
GPIO.cleanup()