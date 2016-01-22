from Tkinter import *
#import Tkinter as Tk
#from Tkinter import ttk
import sqlite3
import sys
import time
import datetime

import matplotlib
matplotlib.use('TkAgg')
#from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style

graphArray = []

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import ConfigParser
import tkFont
#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler

#style.use('ggplot')
#style.use('dark_background')
#style.use('fivethirtyeight')
#style.use('bmh')
#style.use('grayscale')
#print(plt.style.available)

#wm = pyinotify.WatchManager()

OPTIONS = [
	"Allways on",
	"Allways off",
	"1m(2m)",
	"1m(3m)",
	"1m(5m)"
]

TIME = [
	"1 day",
	"1 weak",
	"2 weaks",
	"1 month",
	"6 months",
	"all time"
]

MODES = [
	("Auto", "A"),
	("Manual", "M"),
]

isDoorOpen = True
isManual = False
manualMode = 0

datetime = '0'
tempinside = '0'
huminside = '0'
tempout = '0'
tempin2 = '0'
tempin3 = '0'
curmode = '0'

#ax1 = ""

class Data:
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()

		config = ConfigParser.RawConfigParser()
		config.read(r'/home/pi/Relay/config.ini')
		timeInterval = config.getint('Data','timeinterval')		

		self.variableTime = StringVar(master)
		self.variableTime.set(TIME[0])
		if timeInterval == 0:
			self.variableTime.set(TIME[0])
		if timeInterval == 1:
			self.variableTime.set(TIME[1])
		if timeInterval == 2:
			self.variableTime.set(TIME[2])
		if timeInterval == 3:
			self.variableTime.set(TIME[3])
		if timeInterval == 4:
			self.variableTime.set(TIME[4])
		if timeInterval == 5:
			self.variableTime.set(TIME[5])
		dbTimeList = apply(OptionMenu, (frame, self.variableTime) + tuple(TIME))
		dbTimeList.pack(side=LEFT)
		self.variableTime.trace('w', lambda *args: self.timeIntervalChanged(self.variableTime))

		self.button = Button(frame, text="Refresh", command=self.refresh)
		self.button.pack(side=LEFT)

#		self.con = sqlite3.connect("/home/pi/dht.db")
#		self.test = "1"
#		with self.con:
#			cursor = self.con.cursor()
#			for self.row in cursor.execute("SELECT * FROM meteolog ORDER BY date DESC LIMIT 1"):
#				self.test = self.row
#			self.con.commit()
#		self.con.close()
#		self.test = str(self.test).replace(')','').replace('(','').replace('u\'','').replace("'","")
#		self.splitData = self.test.split(',')
#		datetime = self.splitData[0]
#		tempinside = self.splitData[1]
#		huminside = self.splitData[2]
#		tempout = self.splitData[3]
#		tempin2 = self.splitData[4]
#		tempin3 = self.splitData[5]
#		tempinsidelabel.config(text=tempinside)
#		huminsidelabel.config(text=huminside)
#		tempoutlabel.config(text=tempout)
#		tempin2label.config(text=tempin2)
#		tempin3label.config(text=tempin3)

#		self.getFullData()
		self.coldStart()

	def timeIntervalChanged(self, var):
		config = ConfigParser.RawConfigParser()
		config.read(r'/home/pi/Relay/config.ini')
		print(var.get())

		if var.get() == "1 day":
			config.set('Data', 'timeinterval', '0')
		if var.get() == "1 weak":
			config.set('Data', 'timeinterval', '1')
		if var.get() == "2 weaks":
			config.set('Data', 'timeinterval', '2')
		if var.get() == "1 month":
			config.set('Data', 'timeinterval', '3')
		if var.get() == "6 months":
			config.set('Data', 'timeinterval', '4')
		if var.get() == "all time":
			config.set('Data', 'timeinterval', '5')

		with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
			config.write(configfile)


		

	def refresh(self):
#		self.con = sqlite3.connect("/home/pi/dht.db")
#		self.test = "1"

#		with self.con:
#			cursor = self.con.cursor()
#			for self.row in cursor.execute("SELECT * FROM meteolog ORDER BY date DESC LIMIT 1"):
#				self.test = self.row
#			self.con.commit()
#		self.con.close()

		#self.test = str(self.test).replace(')','').replace('(','').replace('u\'','').replace("'","")
#		self.splitData = self.dbInfo.split(',')
#		datetime = self.splitInfo[0]
#		tempinside = self.splitInfo[1]
#		huminside = self.splitInfo[2]
#		tempout = self.splitInfo[3]
#		tempin2 = self.splitInfo[4]
#		tempin3 = self.splitInfo[5]
#
#		tempinsidelabel.config(text=tempinside)
#		huminsidelabel.config(text=huminside)
#		tempoutlabel.config(text=tempout)
#		tempin2label.config(text=tempin2)
#		tempin3label.config(text=tempin3)
		self.readCurrentTemp()
		self.refreshGraph()

	def getFullData(self):
		if (graphArray != []):
			del graphArray[:]
		self.con = sqlite3.connect("/home/pi/dht.db")
		
		with self.con:
			self.cursor = self.con.cursor()

			query = ""
			if (self.variableTime.get() == "1 day"):
				query = "SELECT * FROM meteotable WHERE date >= datetime('now', '-24 hours')"
			if (self.variableTime.get() == "1 weak"):
				query = "SELECT * FROM meteotable WHERE date >= datetime('now', '-7 days')"
			if (self.variableTime.get() == "2 weaks"):
				query = "SELECT * FROM meteotable WHERE date >= datetime('now', '-14 days')"
			if (self.variableTime.get() == "1 month"):
				query = "SELECT * FROM meteotable WHERE date >= datetime('now', '-1 months')"
			if (self.variableTime.get() == "6 months"):
				query = "SELECT * FROM meteotable WHERE date >= datetime('now', '-6 months')"
			if (self.variableTime.get() == "all time"):
				query = "SELECT * FROM meteotable"
			

			print "value is", self.variableTime.get()
			print query
			for self.row in self.cursor.execute(query):
				print self.row
				self.dbInfo = str(self.row).replace(')','').replace('(','').replace('u\'','').replace("'","")
				self.splitInfo = self.dbInfo.split(',')
				self.graphArrayAppend = self.splitInfo[0]+','+self.splitInfo[1]+','+self.splitInfo[2]+','+self.splitInfo[3]+','+self.splitInfo[4]+','+self.splitInfo[5] 
				print (self.splitInfo[0])
				print (self.splitInfo[1])
				print (self.splitInfo[2])
				print (self.splitInfo[3])
				print (self.splitInfo[4])
				print (self.splitInfo[5])
				graphArray.append(self.graphArrayAppend)
			self.con.commit()
		self.con.close()


	def coldStart(self):
		self.getFullData()
		self.redrawChart()

		

	def refreshGraph(self):
		
		self.getFullData()

		#self.fig.clear()
		self.ax1.cla()
		#plt.cla()
		#plt.clf()
		#self.rect.clear()
		#self.rect.get_tk_widget().delete("all")
		#self.ax1 = self.fig.add_subplot(1,1,1, axisbg='white')
		#self.rect.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		datestamp, tinside, hinside, tout, tin2, tin3 = np.loadtxt(graphArray,delimiter=',', unpack=True, converters={ 0: mdates.strpdate2num('%Y-%m-%d %H:%M:%S')})
		plt.xlabel('Date/Time', color='#2d2d2d')
		plt.ylabel('Temperature', color='#2d2d2d')
		font={'size':'9'}
		matplotlib.rc('font', **font)
	
		self.ax1.plot_date(x=datestamp, y=hinside, fmt='-', label='Hum inside', linewidth=2, color='#505bfd')
		self.ax1.plot_date(x=datestamp, y=tinside, fmt='-', label='Temp inside', linewidth=2, color='#ff6262')
		self.ax1.plot_date(x=datestamp, y=tout, fmt='-', label='Temp outside', linewidth=2, color='#62acff')
		self.ax1.plot_date(x=datestamp, y=tin2, fmt='-', label='Temp inside 2(top)', linewidth=2, color='#ff6c02')
		self.ax1.plot_date(x=datestamp, y=tin3, fmt='-', label='Temp inside 3(down)', linewidth=2, color='#ab0013')
		self.ax1.legend(loc=3, framealpha=0.5)
		plt.legend.fancybox=True
		for label in self.ax1.xaxis.get_ticklabels():
			label.set_rotation(45)
		self.ax1.grid(True)
		self.ax1.spines['right'].set_visible(False)
		self.ax1.spines['top'].set_visible(False)
		self.ax1.spines['left'].set_linewidth(2)
		self.ax1.spines['bottom'].set_linewidth(2)
		self.ax1.tick_params(axis='x', colors='#2d2d2d')
		self.ax1.tick_params(axis='y', colors='#2d2d2d')

		self.rect.draw()

	def readCurrentTemp(self):
		config = ConfigParser.RawConfigParser()
		config.read(r'/home/pi/Relay/config.ini')
		curmode = config.get('Ventilation','currentmode')
		
		self.splitData = self.dbInfo.split(',')
		datetime = self.splitInfo[0]
		tempinside = self.splitInfo[1]
		huminside = self.splitInfo[2]
		tempout = self.splitInfo[3]
		tempin2 = self.splitInfo[4]
		tempin3 = self.splitInfo[5]

		tempinsidelabel.config(text=tempinside)
		huminsidelabel.config(text=huminside)
		tempoutlabel.config(text=tempout)
		tempin2label.config(text=tempin2)
		tempin3label.config(text=tempin3)
		currentModelabel.config(text=curmode)


	def redrawChart(self):
		datestamp, tinside, hinside, tout, tin2, tin3 = np.loadtxt(graphArray,delimiter=',', unpack=True, converters={ 0: mdates.strpdate2num('%Y-%m-%d %H:%M:%S')})
		
		self.fig = plt.figure()
		self.ax1 = self.fig.add_subplot(1,1,1, axisbg='white')
		self.rect = FigureCanvasTkAgg(self.fig, master=root)
		self.rect.show()
		self.rect.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		toolbar = NavigationToolbar2TkAgg(self.rect, root)
		toolbar.update()
		self.rect._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)		

		plt.xlabel('Date/Time', color='#2d2d2d')
		plt.ylabel('Temperature', color='#2d2d2d')
		self.ax1.plot_date(x=datestamp, y=hinside, fmt='-', label='Hum inside', linewidth=2, color='#505bfd')
		self.ax1.plot_date(x=datestamp, y=tinside, fmt='-', label='Temp inside', linewidth=2, color='#ff6262')
		self.ax1.plot_date(x=datestamp, y=tout, fmt='-', label='Temp outside', linewidth=2, color='#62acff')
		self.ax1.plot_date(x=datestamp, y=tin2, fmt='-', label='Temp inside 2(top)', linewidth=2, color='#ff6c02')
		self.ax1.plot_date(x=datestamp, y=tin3, fmt='-', label='Temp inside 3(down)', linewidth=2, color='#ab0013')
		self.ax1.legend(loc=3, framealpha=0.5)
		plt.legend.fancybox=True
		for label in self.ax1.xaxis.get_ticklabels():
			label.set_rotation(45)
		self.ax1.grid(True)
		self.ax1.spines['right'].set_visible(False)
		self.ax1.spines['top'].set_visible(False)
		self.ax1.spines['left'].set_linewidth(2)
		self.ax1.spines['bottom'].set_linewidth(2)
		self.ax1.tick_params(axis='x', colors='#2d2d2d')
		self.ax1.tick_params(axis='y', colors='#2d2d2d')
		#font={'family':'normal', 'weight':'bold', 'size':'9'}
		font={'size':'9'}
		matplotlib.rc('font', **font)
		plt.subplots_adjust(left=0.07, bottom=0.15, right=0.98, top=0.97)

#class EventHandler(FileSystemEventHandler):
#
#	def on_modified(self, event):
#		#sleep(1)
#		isDoorOpen, isManual, manualMode =readConfig()
#		if isManual == True:
#			rb2.select()
#			print("Man")
#		else:
#			rb1.select()
#			print("Auto")
#		if manualMode == 0:
#			variable.set(OPTIONS[2])
#		if manualMode == 1:
#			variable.set(OPTIONS[3])
#		if manualMode == 2:
#			variable.set(OPTIONS[4])
#		if manualMode == 3:
#			variable.set(OPTIONS[1])
#		if manualMode == 4:
#			variable.set(OPTIONS[0])
		
def readConfig():
	config = ConfigParser.RawConfigParser()
	config.read(r'/home/pi/Relay/config.ini')
	#print(config.sections())
	#print( config.get('Ventilation','isDoorOpen'))
	
	isDoorOpen = config.get('Ventilation','isDoorOpen')
	isManual = config.getboolean('Ventilation','isManual')
	manualMode = config.getint('Ventilation','manualMode')
	print isDoorOpen
	print isManual
	print manualMode
	return isDoorOpen, isManual, manualMode

def ventModeChanged(*args):

	config = ConfigParser.RawConfigParser()
	config.read(r'/home/pi/Relay/config.ini')
	#config.set('Ventilation', 'isManual', 'True')

	if variable.get() == "Allways on":
		config.set('Ventilation', 'manualMode', '4')
	if variable.get() == "Allways off":
		config.set('Ventilation', 'manualMode', '3')
	if variable.get() == "1m(2m)":
		config.set('Ventilation', 'manualMode', '0')
	if variable.get() == "1m(3m)":
		config.set('Ventilation', 'manualMode', '1')
	if variable.get() == "1m(5m)":
		config.set('Ventilation', 'manualMode', '2')

	with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
		config.write(configfile)

def manAutoSwitch():
	config = ConfigParser.RawConfigParser()
	config.read(r'/home/pi/Relay/config.ini')
	if v.get() == 1:
		config.set('Ventilation', 'isManual', 'False')
	if v.get() == 2:
		config.set('Ventilation', 'isManual', 'True')
	with open(r'/home/pi/Relay/config.ini', 'wb') as configfile:
		config.write(configfile)

root = Tk()
#root.iconbitmap(root, default='@/home/pi/Tkinter/icon/DataMonitor.ico')
app = Data(root)
root.title("Data monitor")
root.minsize(width = 1000, height = 300)

#observer = Observer()
#observer.schedule(EventHandler(), path='/home/pi/Relay', recursive=True)
#observer.start()

isDoorOpen, isManual, manualMode =readConfig()

lf = LabelFrame(root, text="Ventilation")
lf.pack()
group = Entry(lf)
group.pack(side=LEFT)

v = IntVar()
rb1 = Radiobutton(group, text="Auto", variable=v, value=1, command=manAutoSwitch)
rb2 = Radiobutton(group, text="Manual", variable=v, value=2, command=manAutoSwitch)
rb1.pack(anchor=W)
rb2.pack(anchor=W)

if isManual == True:
	rb2.select()
	print("Man")
else:
	rb1.select()
	print("Auto")


variable = StringVar(lf)
if manualMode == 0:
	variable.set(OPTIONS[2])
if manualMode == 1:
	variable.set(OPTIONS[3])
if manualMode == 2:
	variable.set(OPTIONS[4])
if manualMode == 3:
	variable.set(OPTIONS[1])
if manualMode == 4:
	variable.set(OPTIONS[0])
w = apply(OptionMenu, (group, variable) + tuple(OPTIONS))
w.pack()

variable.trace('w', ventModeChanged)
customFont = tkFont.Font(family="Helvetica", size=14)

tinlbl = Label(root, text=" t inside: ")
tinlbl.pack(side=LEFT)
tempinsidelabel = Label(root, text=tempinside, font=customFont)
tempinsidelabel.pack(side=LEFT)
hinlbl = Label(root, text=" | h inside: ")
hinlbl.pack(side=LEFT)
huminsidelabel = Label(root, text=huminside, font=customFont)
huminsidelabel.pack(side=LEFT)
toutlbl = Label(root, text=" | t outside: ")
toutlbl.pack(side=LEFT)
tempoutlabel = Label(root, text=tempout, font=customFont)
tempoutlabel.pack(side=LEFT)
tin2lbl = Label(root, text=" | t in2: ")
tin2lbl.pack(side=LEFT)
tempin2label = Label(root, text=tempin2, font=customFont)
tempin2label.pack(side=LEFT)
tin3lbl = Label(root, text=" | t in3: ")
tin3lbl.pack(side=LEFT)
tempin3label = Label(root, text=tempin3, font=customFont)
tempin3label.pack(side=LEFT)

curModelbl = Label(root, text=" | current mode: ")
curModelbl.pack(side=LEFT)
currentModelabel = Label(root, text=curmode, font=customFont)
currentModelabel.pack(side=LEFT)

app.readCurrentTemp()

root.mainloop()
root.destroy()