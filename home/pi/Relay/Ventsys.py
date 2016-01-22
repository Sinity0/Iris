import RPi.GPIO as GPIO
import time
import threading
import sqlite3
import sys
import datetime

GPIO.setmode(GPIO.BCM)
pinList = [5, 6, 12, 13, 16, 19, 20, 26]

for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)

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

timeToSwitchMode = False

class Task(threading.Thread):
	def __init__(self, action, loopdelay, initdelay):
		self._action = action
		self._loopdelay = loopdelay
		self._initdelay = initdelay
		self._running = 1
		threading.Thread.__init__(self)
	
	def __repr__(self):
		return '%s %s %s' % (self._action, self._loopdelay, self._initdelay)
		
	def run(self):
		if self._initdelay:
			time.sleep(self._initdelay)
		self._runtime = time.time()
		while self._running:
			start = time.time()
			self._action()
			self._runtime += self._loopdelay
			time.sleep(self._runtime - start)

	def stop(self):
		self._running = 0

class Scheduler:
	def __init__(self):
		self._tasks = []

	def __repr__(self):
		rep = ''
		for task in self._tasks:
			rep += '%s\n' % 'task'
		return rep

	def AddTask(self, action, loopdelay, initdelay = 0):
		task = Task(action, loopdelay, initdelay)
		self._tasks.append(task)
	
	def PopTask(self):
		if (self._tasks.count() != 0):
			task = self._tasks.pop()
	
	def StartAllTasks(self):
		for task in self._tasks:
			task.start()
	
	def StopAllTasks(self):
		for task in self._tasks:
			print 'Stopping task', task
			task.stop()
			task.join()
			print 'Stopped'

	def StopTask(self):
		for task in self.tasks:
			print task

if __name__ == '__main__':
	
	def timestamp(s):
		print '%.2f : %s' % (time.time(), s)
	
	def cd0():
		timestamp('\tcd0')
		#data = getLastData()
		#datestamp = data[0]
		#tinside = data[1]
		#hinside = data[2]
		#tout = data[3]
		#start_time = time.time()
		#runTime = round(time.time() - start_time, 2)
		GPIO.output(5, GPIO.LOW)
		i = 1
		while (i < 11):
			i = i+1
			time.sleep(1)
		GPIO.output(5, GPIO.HIGH)
		#if (timeToSwitchMode == True)
			#timeToSwitchMode = False
			#s.StopAllTasks()
			
	
	def cd1():
		timestamp('\tcd1')
	
	def Task3():
		timestamp('\tTask3')
	
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

	def autoClosed():
		timestamp('\tautoClosed')

	s = Scheduler()
	
	while True:
		print("cycle started")
		data = getLastData()
		datestamp = data[0]
		tinside = data[1]
		hinside = data[2]
		tout = data[3]
		s.StopAllTasks() 
			
		if (float(tout) > 1 and float(tout) < 37 ):
			s.AddTask(cd0, 60.0, 0 )

		print s
		s.StartAllTasks()
		time.sleep(fivem)
		timeToSwitchMode = True
	

	#	  task      loopdelay   initdelay
	#-----------------------------------------------
	#s.AddTask(cd0,    10.0,         0       )
	#s.AddTask(Task2,    15.5,         0.25    )
	#s.AddTask(Task3,    12.1,         0.05    )
	#s.AddTask(autoClosed,    15.0,         0.05    )

	print s
	s.StartAllTasks()
	raw_input()
	s.StopAllTasks() 

