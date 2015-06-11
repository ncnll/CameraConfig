#!/usr/bin/python
from os import listdir
import urllib2,urllib
import os.path
import os
import json
import sqlite3

#check whether /home/pi/database/uploadConfig.db is exists, if not, create a new one
directory_path = '/home/pi/database/uploadconfig/'
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
	c.execute('''CREATE TABLE CAMERACONFIG(serialNumber text, cameraType integer, localShootInterval integer, uploadShootInterval integer, workingTime text, localResolution text, remoteResolution text, updateTime text, startDate text, endDate text, uploadPath text)''')
	print 'table is not exists'

#Load config properties from server
stdout = listdir("/home/pi/v4l/by-id/")
##Delete all camera not exists
#conn.execute("DELETE FROM CAMERACONFIG")
#conn.commit()

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
		
		print responseJson['rows'][0]['serialNumber']
		#Save to database
		c=conn.execute('SELECT * FROM CAMERACONFIG WHERE serialNumber=?', (responseJson['rows'][0]['serialNumber'],))
		configRow=c.fetchone()
		insertSql = "INSERT INTO CAMERACONFIG VALUES %s" % ((str(responseJson['rows'][0]['serialNumber']), format(responseJson['rows'][0]['cameraType'], 'x'), format(responseJson['rows'][0]['localShootInterval'], 'x'),format(responseJson['rows'][0]['uploadShootInterval'], 'x'), str(responseJson['rows'][0]['workingTime']), str(responseJson['rows'][0]['localResolution']), str(responseJson['rows'][0]['remoteResolution']), str(responseJson['rows'][0]['updateTime']), str(responseJson['rows'][0]['startDate']), str(responseJson['rows'][0]['endDate']), str(responseJson['rows'][0]['uploadPath'])),)
		print insertSql
		if configRow is not None:
			print configRow
		else :
			#print str(insertSql)
			conn.execute(insertSql)
			conn.commit()