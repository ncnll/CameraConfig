#!/usr/bin/python
from os import listdir
import urllib2,urllib
import os.path
import os
import json
import sqlite3

#check whether /home/pi/database/uploadConfig.db is exists, if not, create a new one
directory_path = '/home/pi/database/uploadconfig'
uploadConfig_file_path=directory_path+'uploadConfig.db'
if not os.path.exists(directory_path):
	os.makedirs(directory_path)
if not os.path.exists(uploadConfig_file_path) :
	fp = open(uploadConfig_file_path, 'w+')
	fp.close()

#check whether sqlite config table is exists, if not , create a new one
conn = sqlite3.connect(uploadConfig_file_path)#/home/pi/database/test.db
c=conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CAMERACONFIG'")
row1 = c.fetchone()
if row1 is not None :
	print row1[0]
else :
	c.execute('''CREATE TABLE CAMERACONFIG(cameraId text, cameraType integer, localShootInterval integer, uploadShootInterval integer, workingTime text, localResolution text, remoteResolution text, updateTime text, startDate text, endDate text, uploadPath text)''')
	print 'table is not exists'

#Load config properties from server
stdout = listdir("/home/pi/v4l/by-id/")
for line in stdout:
	usbserial=line[4:22]
	#print usbserial
	para_dct = {}
	para_dct['search_eq_serialNumber'] = usbserial
	url = """http://192.168.1.105:8091/device/camera/searchList"""
	para_data = urllib.urlencode(para_dct)
	response = urllib2.urlopen(url, para_data)
#	print response.info()
#	print response.geturl()
#	print response.getcode()
	responseString = response.read()
	responseJson = json.loads(responseString)
	if len(responseJson['rows'])>0:
		print responseJson['rows'][0]['startDate']
	#Save to database
	#c.execute('SELECT * FROM CAMERACONFIG WHERE cameraId=?', t)
	#print c.fetchone()

#print stdout
