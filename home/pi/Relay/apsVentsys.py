import RPi.GPIO as GPIO
import time
import threading
import sqlite3
import sys
import datetime
import os
#from apscheduler.scheduler import Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
import ConfigParser

print("Ventilation system. Relay script. v1.0")

GPIO.setmode(GPIO.BCM)
pinList = [5, 6, 12, 13, 16, 19, 20, 26]

for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)

isDoorOpen = False
isManual = False
manualMode = 0
	

def getLastData():
	con = sqlite3.connect("/home/pi/dht.db")
	data = []
		
	with con:
		cursor = con.cursor()
		for row in cursor.execute("SELECT * FROM meteolog ORDER BY date"):
			dbInfo = str(row).replace(')','').replace('(','').replace('u\'','').replace("'","")
			splitInfo = dbInfo.split(',')
			data = splitInfo
			#data = splitInfo[0]+','+splitInfo[1]+','+splitInfo[2]+','+splitInfo[3]
			#graphArrayAppend = splitInfo[0]+','+splitInfo[1]+','+splitInfo[2]+','+splitInfo[3]
			#graphArray.append(graphArrayAppend)
		con.commit()
	con.close()
	print("database query")
	return data

def mon():
	GPIO.output(5, GPIO.LOW)
	GPIO.output(6, GPIO.LOW)
	i = 1
	while (i < 60):
		i = i+1
		time.sleep(1)
	GPIO.output(5, GPIO.HIGH)
	GPIO.output(6, GPIO.HIGH)

def cd0():
	mon()
	print ('cd0')

def cd1():
	mon()
	print ('cd1')

def cd2():
	mon()
	print ('cd2')

def cd3(): #unused
	GPIO.output(5, GPIO.LOW)
	i = 1
	while (i < 15):
		i = i+1
		time.sleep(1)
	GPIO.output(5, GPIO.HIGH)
	print ('cd3')

def cd4():
	i = 1
	while (i < 60):
		i = i+1
		time.sleep(1)
	print ('cd4')

def od02():
	mon()
	print ('od02')

def od12():
	mon()
	print ('od12')

def od11():
	i = 1
	while (i < 30):
		i = i+1
		time.sleep(1)
	print ('od11')

def od01():
	mon()
	print ('od01')

def m0():
	mon()
	print ('m0')

def m1():
	mon()
	print ('m1')

def m2():
	mon()
	print ('m2')

def m3():
	i = 1
	while (i < 60):
		i = i+1
		time.sleep(1)
	print ('m3')

def m4():
	mon()
	print ('m4')

def readConfig():
	config = ConfigParser.RawConfigParser()
	config.read(r'/home/pi/Relay/config.ini')
		
	isDoorOpen = config.getboolean('Ventilation','isDoorOpen')
	isManual = config.getboolean('Ventilation','isManual')
	manualMode = config.getint('Ventilation','manualMode')
	print isDoorOpen
	print isManual
	print manualMode
	return isDoorOpen, isManual, manualMode

def writeConfigCurmode(curmode):
	config = ConfigParser.RawConfigParser()
	config.read(r'/home/pi/Relay/config.ini')
	config.set('Ventilation', 'currentmode', curmode)
	with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
		config.write(configfile)

if __name__ == "__main__":
	sched = BackgroundScheduler()
	
	sched.start()

	graphArray = []

	tens = 10
	thirtys = 30
	onem = 60
	twom = 120
	fourm = 240
	fivem = 300
	oneh = 3600
	fifteenm = 900

	datestamp = ""
	tinside = ""
	hinside = ""
	tout = ""


	try:
		while True:
			isDoorOpen, isManual,manualMode = readConfig()

			data = getLastData()
			datestamp = data[0]
			tinside = data[1]
			hinside = data[2]
			tout = data[3]
			print(datestamp)
			print(tinside)
			print(hinside)
			print(tout)
			
			print(int( float(tout) ))
			if(isManual == False):
				print("ido: " + str(isDoorOpen))
				if(isDoorOpen == False):
					if (int(float(tout)) <= -5):
						job = sched.add_job(cd4, 'interval' ,seconds=840)
						writeConfigCurmode('Allways_off(cd4)')
						print("(<-5) added cd4 (allways off)")
					
					if (int(float(tout)) >= -4 and int(float(tout)) <= -1 ):
						job = sched.add_job(cd2, 'interval' ,seconds=840)
						writeConfigCurmode('1m(14m)(cd2)')
						print("(-9 - 0) added cd2 ( 1m(14m) )")

					if (int(float(tout)) >= 0 and int(float(tout)) <= 10 ):
						job = sched.add_job(cd1, 'interval' ,seconds=240)
						writeConfigCurmode('1m(4m)(cd1)')
						print("(0-10) added cd1 ( 1m(4m) )")
		
					if (int(float(tout)) >= 11 and int(float(tout)) <= 17 ):
						job = sched.add_job(cd0, 'interval' ,seconds=120)
						writeConfigCurmode('1m(2m)(cd0)')
						print("(11-17) added cd0 ( 1m(2m) )")
		
					if (int(float(tout)) >= 18 and int(float(tout)) <= 25 ):
						job = sched.add_job(cd1, 'interval' ,seconds=240)
						writeConfigCurmode('1m(4m)(cd1)')
						print("(18-25) added cd1 ( 1m(4m) )")
		
					if (int(float(tout)) >= 26 and int(float(tout)) <= 29 ):
						job = sched.add_job(cd2, 'interval' ,seconds=840)
						writeConfigCurmode('1m(14m)(cd2)')
						print("(26-29) added cd2 ( 1m(14m) )")
		
					if (int(float(tout)) >= 30 ):
						job = sched.add_job(cd4, 'interval' ,seconds=840)
						writeConfigCurmode('Allways_off(cd4)')
						print("(>30) added cd4 (allways off)")
	
				else:
					if (int(float(tout)) <= -5):
						job = sched.add_job(od11, 'interval' ,seconds=90)

						config = ConfigParser.RawConfigParser()
						config.read(r'/home/pi/Relay/config.ini')
						config.set('Ventilation', 'isDoorOpen', 'False')
						config.set('Ventilation', 'currentmode', 'Allways_off(od11)')
						with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
							config.write(configfile)

						isDoorOpen = False
						print("*door opened* (<-5) added od11 ( Allways off ) )")						

					if (int(float(tout)) >= -4 and int(float(tout)) <= -1 ):
						job = sched.add_job(od01, 'interval' ,seconds=840)

						config = ConfigParser.RawConfigParser()
						config.read(r'/home/pi/Relay/config.ini')
						config.set('Ventilation', 'isDoorOpen', 'False')
						config.set('Ventilation', 'currentmode', '1m(2m)(od01)')
						with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
							config.write(configfile)

						isDoorOpen = False
						print("*door opened* (-4 - -1) added od01 ( 1m(14m) )")

					if (int(float(tout)) >= 0 and int(float(tout)) <= 19 ):
						job = sched.add_job(od02, 'interval' ,seconds=60)

						config = ConfigParser.RawConfigParser()
						config.read(r'/home/pi/Relay/config.ini')
						config.set('Ventilation', 'isDoorOpen', 'False')
						config.set('Ventilation', 'currentmode', 'Allways_on(od02)')
						with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
							config.write(configfile)

						isDoorOpen = False
						print("*door opened* (0-19) added od02 (allways on)")
	
					if (int(float(tout)) >= 20 ):
						job = sched.add_job(od12, 'interval' ,seconds=300)

						config = ConfigParser.RawConfigParser()
						config.read(r'/home/pi/Relay/config.ini')
						config.set('Ventilation', 'isDoorOpen', 'False')
						config.set('Ventilation', 'currentmode', '1m(5m)(od12)')
						with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
							config.write(configfile)

						isDoorOpen = False
						print("*door opened* (>20) added od12 ( 1m(5m) )")
			else:
				print(manualMode)
				if(manualMode == 0):
					job = sched.add_job(m0, 'interval' ,seconds=120)

					config = ConfigParser.RawConfigParser()
					config.read(r'/home/pi/Relay/config.ini')
					config.set('Ventilation', 'currentmode', '1m(2m)(m0)')
					with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
						config.write(configfile)

					print("*manual* added m0 ( 1m(2m) )")
				if(manualMode == 1):
					job = sched.add_job(m1, 'interval' ,seconds=180)

					config = ConfigParser.RawConfigParser()
					config.read(r'/home/pi/Relay/config.ini')
					config.set('Ventilation', 'currentmode', '1m(3m)(m1)')
					with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
						config.write(configfile)

					print("*manual* added m1 ( 1m(3m) )")
				if(manualMode == 2):
					job = sched.add_job(m2, 'interval' ,seconds=300)

					config = ConfigParser.RawConfigParser()
					config.read(r'/home/pi/Relay/config.ini')
					config.set('Ventilation', 'currentmode', '1m(5m)(m2)')
					with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
						config.write(configfile)

					print("*manual* added m2 ( 1m(5m) )")
				if(manualMode == 3):
					job = sched.add_job(m3, 'interval' ,seconds=60)

					config = ConfigParser.RawConfigParser()
					config.read(r'/home/pi/Relay/config.ini')
					config.set('Ventilation', 'currentmode', 'Allways_off(m3)')
					with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
						config.write(configfile)

					print("*manual* added m3 (allways off)")
				if(manualMode == 4):
					job = sched.add_job(m4, 'interval' ,seconds=60)

					config = ConfigParser.RawConfigParser()
					config.read(r'/home/pi/Relay/config.ini')
					config.set('Ventilation', 'currentmode', 'Allways_on(m4)')
					with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
						config.write(configfile)

					print("*manual* added m4 (allways on)")

			time.sleep(fifteenm)
			#sched.unschedule_job(job)
			job.remove()
			print("removed")
			time.sleep(thirtys)
	except (KeyboardInterrupt, SystemExit):
		sched.shutdown()
		GPIO.cleanup()
		