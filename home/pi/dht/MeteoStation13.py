#!/usr/bin/env python
# Meteostation script v1.3
# Components: DHT22, USB flashdrive, Light diode, SQLite database
#             Supervisord, dhtScript2.py, dhtSleepScript-stderr.log,
#             dhtSleepScript-stdout.log, google docs, google oauth,
#             pigpio lib, gspread lib, DHT22 lib, DS18B20, RFID RC522, 8-ch relay.
import pigpio
import DHT22
import json
import gspread
import time
import datetime
import os
import sqlite3
import glob
from oauth2client.client import SignedJwtAssertionCredentials
from time import sleep

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sleepTime = 900

baseDir = '/sys/bus/w1/devices/'
#deviceFolder = glob.glob(baseDir + '28-000006c8044b')[0]
deviceFolderOut = glob.glob(baseDir + '28-000006c8044b')[0]
deviceFolderIn2 = glob.glob(baseDir + '28-041591ae04ff')[0]
deviceFolderIn3 = glob.glob(baseDir + '28-01159110bcff')[0]
deviceFileOut = deviceFolderOut + '/w1_slave'
deviceFileIn2 = deviceFolderIn2 + '/w1_slave'
deviceFileIn3 = deviceFolderIn3 + '/w1_slave'

pi = pigpio.pi()
dht22 = DHT22.sensor(pi,4,17)
dht22.trigger()

json_key = json.load(open('/home/pi/zend_dht/credentials.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gspCred = False
worksheet = False

dbconn = sqlite3.connect('/home/pi/dht.db')
dbcurs = dbconn.cursor()
print("Meteo station v1.3")

def readTempRaw(deviceFile):
        f = open(deviceFile, 'r')
        lines = f.readlines()
        f.close()
        return lines

def readTemp(devFile):
	lines = readTempRaw(devFile)
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = readTempRaw(devFile)
        equalsPos = lines[1].find('t=')
        if equalsPos != -1:
                tempString = lines[1][equalsPos+2:]
                tempC = '%.1f' % (float(tempString) / 1000.0)
                return tempC

def openDbConnection():
	try:
		dbconn = sqlite3.connect('/home/pi/dht.db')
		dbcurs = dbconn.cursor()
	except Exception, e:
		print("[openDbConnection] Error: %s" % str(e))

def addRecordToDb(temp, hum, tempOut, tempin2, tempin3):
	try:
		dbcurs.execute("INSERT INTO meteotable values(datetime('now'), "+temp+", "+hum+", "+str(tempOut)+", "+str(tempin2)+", "+str(tempin3)+")")
		dbconn.commit()
	except Exception, e:
		print("[addRecordToDb] Error: %s" % str(e))
		
def selectRecordsByDate(tableName, mode):
	try:
		for row in dbcurs.execute("SELECT * FROM (?) WHERE tdate>=date('now', '-1 day')"):
			print row
	except Exception, e:
		print("[selectRecordByDate] Error: %s" % str(e))

def tryToConnect():
	try:
		gspCred = gspread.authorize(credentials)
		worksheet = gspCred.open("meteo_tbl").sheet1
		return worksheet
	except Exception, e:
		print("[tryToConnect] Error: %s" % str(e))
		print("Waiting 60s.")
		sleep(60)
		print("Retrying...")
		gspCred = gspread.authorize(credentials)
		worksheet = gspCred.open("meteo_tbl").sheet1
		return worksheet
	
def readDHT22():
	dht22.trigger()
	humidity = '%.f' % (dht22.humidity())
	temp = '%.1f' % (dht22.temperature())
	return (humidity, temp)

def printInFile(datetime, temp, hum, tempOut, tempin2, tempin3):
	try:
		fh = open("/media/pi/Backup/meteoOut.txt", "a")
		fh.write(datetime +" "+temp+"C "+hum+" "+tempOut+"C"+ " " +tempin2+"C"+ " " +tempin3+"C"+ "%\n")
		fh.close()
	except Exception, e:
		print("[printInFile method] Error: %s</p>" % str(e))
		print("Trying to write in /media/Backup/meteoOut.txt")
		try:
			fh = open("/media/Backup/meteoOut.txt", "a")
			fh.write(datetime +" "+temp+"C "+hum+" "+tempOut+"C"+" " +tempin2+"C"+ " " +tempin3+"C"+"%\n")
			fh.close()
			print("Done")
		except Exception, x:
			print("[printInFile method] Error: %s</p>" % str(x))
			print("Print in file failed.")
		
		
def printInConsole(datetime, temp, hum, tempOut, tempin2, tempin3):
	print("Humidity is: " + hum + "%")
	print("Temperature 1(mid) is: " + temp+ "C")
	print("Temperature 2(up) is: " + temp2+ "C")
	print("Temperature 3(down) is: " + temp3+ "C")
	print("Temperature outside is: " + str(tempOut) + "C")
	print(datetime);
	
while True:
	try:
		humidity, temperature = readDHT22()
		tempOut = readTemp(deviceFileOut)
		temp2 = readTemp(deviceFileIn2)
		temp3 = readTemp(deviceFileIn3)
		dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
		if (worksheet == False):
			worksheet = tryToConnect()
		if (worksheet != False):
			try:
				rowToAdd = [dt, temperature + " C", humidity, tempOut + " C", temp2 + "C", temp3 + "C"]
				worksheet.append_row(rowToAdd)
			except Exception, e:
				print("[append_row(Session ended)] Error: %s" % str(e))
				print("Starting new session...")
				worksheet = tryToConnect()
				rowToAdd = [dt, temperature + " C", humidity, tempOut + " C", temp2 + "C", temp3 + "C"]
				worksheet.append_row(rowToAdd)
		else:
			tryToConnect()
		addRecordToDb(temperature, humidity, tempOut, temp2, temp3)
		printInConsole(dt, temperature, humidity, tempOut, temp2, temp3)
		printInFile(dt, temperature, humidity, tempOut, temp2, temp3)
		sleep(sleepTime)
	except Exception, e:
		print("[while True cycle] Error: %s" % str(e))
		humidity, temperature = readDHT22()
		tempOut = readTemp(deviceFileOut)
		temp2 = readTemp(deviceFileIn2)
		temp3 = readTemp(deviceFileIn3)
		dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
		printInConsole(dt, temperature, humidity, tempOut, temp2, temp3)
		addRecordToDb(temperature, humidity, tempOut, temp2, temp3)
		printInFile(dt, temperature, humidity, tempOut, temp2, temp3)
		sleep(sleepTime)
		
