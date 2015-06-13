#!/usr/bin/python
from threading import Timer
from threading import Thread
from os import listdir
import urllib2,urllib
import os.path
import os
import json
import sqlite3
import threading

########Get cpu serial number 
def doreaddb():
	#check whether /home/pi/database/uploadConfig.db is exists, if not, create a new one
	directory_path = '/home/pi/database/uploadconfig/'
	uploadConfig_file_path=directory_path+'uploadConfig.db'
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)
	if not os.path.exists(uploadConfig_file_path) :
		fp = open(uploadConfig_file_path, 'w+')
		fp.close()

	#check whether sqlite config table is exists, if not , create a new one
	connPre = sqlite3.connect(uploadConfig_file_path)#/home/pi/database/test.db
	cPre=connPre.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CAMERACONFIG'")
	row1 = cPre.fetchone()
	if row1 is not None :
		print row1[0]
		cPre=connPre.execute("SELECT * FROM CAMERACONFIG")
		row1 = cPre.fetchone()
		print row1[0]
	else :
		c.execute('''CREATE TABLE CAMERACONFIG(serialNumber text, cameraType integer, localShootInterval integer, uploadShootInterval integer, workingTime text, localResolution text, remoteResolution text, updateTime text, startDate text, endDate text, uploadPath text)''')
		#need commit?
		print 'table is not exists'
def printit():
	threading.Timer(0.1, printit).start()
	print "Hello, World!"
	doreaddb()
	#time.sleep(2)
printit()




