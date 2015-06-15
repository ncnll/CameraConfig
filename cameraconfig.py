#!/usr/bin/python
from threading import Timer
#from threading import Thread
from os import listdir
import urllib2,urllib
import os.path
import os
import json
import sqlite3
#import threading

########Get cpu serial number 
def getserial():
	cpuseiral = "0000000000000000"
	try:
		cpufile = open('/proc/cpuinfo','r')
		for line in cpufile:
			if line[0:6]=='Serial':
				cpuserial=line[10:26]
		cpufile.close()
	except:
		cpuserial="Error00000000000"
	return cpuserial

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
else :
	c.execute('''CREATE TABLE CAMERACONFIG(serialNumber text, cameraType integer, localShootInterval integer, uploadShootInterval integer, workingTime text, localResolution text, remoteResolution text, updateTime text, startDate text, endDate text, uploadPath text)''')
	#need commit?
	print 'table is not exists'

##Delete all camera not exists
#conn.execute("DELETE FROM CAMERACONFIG")
#conn.commit()

###### Update onboard camera config
def updateCameraConfig():
	conn = sqlite3.connect(uploadConfig_file_path)
	#Get all serialNumbers
	serialNumberList = []
	#Add cpu serialNumber(onboard csi camera serialId)
	serialNumberList.append(getserial())
	#Add usb camera serialNumber
	stdout = listdir("/home/pi/v4l/by-id/")
	for line in stdout:
		usbserial=line[4:22]
		serialNumberList.append(usbserial)

	for serialNumber in serialNumberList:
		#Request 
		para_dct = {}
		#Get last update time
		c=conn.execute('SELECT * FROM CAMERACONFIG WHERE serialNumber=?', (serialNumber,))
		configRow=c.fetchone()
		if configRow is not None:
			para_dct['search_gt_updateTime'] = configRow[7]
		else : 
			para_dct['search_gt_updateTime'] = "1988-08-08T08:08:08.008Z"	
		para_dct['search_eq_serialNumber'] = serialNumber

		#print para_dct
		url = """http://192.168.1.105:8091/device/camera/searchList"""
		para_data = urllib.urlencode(para_dct)
		try:
			response = urllib2.urlopen(url, para_data, timeout=15)
		except Exception, e:
			print e
			continue
		responseString = response.read()
		responseJson = json.loads(responseString)
		#if server side updatetime isn't new, do not update
		#if(responseJson[''])
		if len(responseJson['rows'])>0:
			#print responseJson['rows'][0]['serialNumber']
			#Save to database
			execSql = None
			if configRow is not None:
				execSql = "UPDATE CAMERACONFIG SET cameraType=%d, localShootInterval=%d, uploadShootInterval=%d, workingTime='%s', localResolution='%s', remoteResolution='%s', updateTime='%s', startDate='%s', endDate='%s', uploadPath='%s' where serialNumber='%s' " % (responseJson['rows'][0]['cameraType'], responseJson['rows'][0]['localShootInterval'], responseJson['rows'][0]['uploadShootInterval'], str(responseJson['rows'][0]['workingTime']), str(responseJson['rows'][0]['localResolution']), str(responseJson['rows'][0]['remoteResolution']), str(responseJson['rows'][0]['updateTime']), str(responseJson['rows'][0]['startDate']), str(responseJson['rows'][0]['endDate']), str(responseJson['rows'][0]['uploadPath']),str(responseJson['rows'][0]['serialNumber']),)
			else :
				#print str(insertSql)
				execSql = "INSERT INTO CAMERACONFIG VALUES %s" % ((str(responseJson['rows'][0]['serialNumber']), format(responseJson['rows'][0]['cameraType'], 'x'), format(responseJson['rows'][0]['localShootInterval'], 'x'),format(responseJson['rows'][0]['uploadShootInterval'], 'x'), str(responseJson['rows'][0]['workingTime']), str(responseJson['rows'][0]['localResolution']), str(responseJson['rows'][0]['remoteResolution']), str(responseJson['rows'][0]['updateTime']), str(responseJson['rows'][0]['startDate']), str(responseJson['rows'][0]['endDate']), str(responseJson['rows'][0]['uploadPath'])),)
			conn.execute(execSql)
			conn.commit()
			print execSql

###Interval function to update config
def updateCameraConfigIntervalTimer():
	#Update every 300 seconds
	Timer(300, updateCameraConfigIntervalTimer).start()
	updateCameraConfig()
#Application Start 
updateCameraConfigIntervalTimer()