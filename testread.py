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
def dowritedb():
	directory_path = '/home/pi/database/uploadconfig/'
	uploadConfig_file_path=directory_path+'uploadConfig.db'
	connPre = sqlite3.connect(uploadConfig_file_path)#/home/pi/database/test.db
	cPre=connPre.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CAMERACONFIG'")
	row1 = cPre.fetchone()
	if row1 is not None :
		print row1[0]
		cPre=connPre.execute("insert into CAMERACONFIG (serialNumber,cameraType,localShootInterval) values ('123', 88, 88)")
		connPre.commit()
	else :
		c.execute('''CREATE TABLE CAMERACONFIG(serialNumber text, cameraType integer, localShootInterval integer, uploadShootInterval integer, workingTime text, localResolution text, remoteResolution text, updateTime text, startDate text, endDate text, uploadPath text)''')
		#need commit?
		print 'table is not exists'
def printit():
	threading.Timer(1, printit).start()
	print "Hello, World!"
	dowritedb()
	#time.sleep(2)
printit()



