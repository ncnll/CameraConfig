from threading import Timer
import pygame
import pygame.camera #https://www.pygame.org/docs/ref/camera.html
import pygame.image
from pygame.locals import *
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import time
import threading
import os
import json
import sqlite3
import picamera
from datetime import datetime

#from subprocess import Popen, PIPE

#(stdout, stderr) = Popen(["cat","foo.txt"], stdout=PIPE).communicate()

import urllib2
#init usb camera
pygame.init()
pygame.camera.init()

##file local storage path
local_storage_path = '/home/pi/storage/charmyin_uploaded_images/'

localResolution="1920*1080"

#init picamera
camera = picamera.PiCamera()
camera.resolution = (1920, 1080)

#check whether /home/pi/database/uploadConfig.db is exists, if not, create a new one
def get_storage_path(parent_dir_name):
	directory_path = local_storage_path+parent_dir_name+"/"
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)
	return directory_path

###Get current milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

########Get cpu serial number
def getCpuSerial():
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
#Set cpu serial to global
cpu_serial = getCpuSerial()
#Current cameraConfigDict 
cameraConfigDict = None #getCameraConfigInfo(cpuSerial)

#Change row to dict
def dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def getSqliteDBConnection():
	#if db is not exist
	directory_path = '/home/pi/database/uploadconfig/'
	uploadConfig_file_path=directory_path+'uploadConfig.db'
	if not os.path.exists(uploadConfig_file_path) :
		return None
	connPre = sqlite3.connect(uploadConfig_file_path)#/home/pi/database/test.db
	return connPre

#Get config table info
def getCameraConfigInfo(serialNumber):
	connPre = getSqliteDBConnection()
	cPre=connPre.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CAMERACONFIG'")
	row1 = cPre.fetchone()
	if row1 is None :
		return None
	else : 
		print row1[0]
		exec_sql = "SELECT * FROM CAMERACONFIG where serialNumber='%s'" % (str(serialNumber) ,)
		print exec_sql
		cPre=connPre.execute(exec_sql)
		row1 = cPre.fetchone()
		print row1
		rowDict = dict_factory(cPre, row1)
		return rowDict

#Get config param by serialNumber then send to server
def sendImageToLocalAndRemoteServer(serialNumber, uploadImageName):
	#Get config param
	configDict = getCameraConfigInfo(serialNumber)
	print configDict
	if configDict is None : 
		return None
	#Send to local server
	register_openers()#Why to use this?
	with open(uploadImageName, 'r') as f:
		datagen, headers = multipart_encode({"file":f,"serialNumber":configDict["serialNumber"],"index":"0", "viewIndex":"0", "cameraBoardUploadTime":str(current_milli_time())})
		#request = urllib2.Request("http://192.168.1.105:3000/index/uploadCameraPhoto", datagen, headers)
		#url should load from server, or changed by hand
		#request = urllib2.Request("http://192.168.1.105:3000/upload/single", datagen, headers)
		headers["User-agent"] = "Mozilla/5.0"
		print headers
		request = urllib2.Request("http://192.168.1.105:3000/upload/single", datagen, headers)
		try:
			response = urllib2.urlopen(request,timeout=30)
			#print response.read()
			print "local is ok"
		except Exception, e:
			print e
			#Record failure
		#Compare time
		#Send to remote server
		is_remote_on = isRemoteTakePhotoOn()
		if is_remote_on:
			datagen, headers = multipart_encode({"file":f,"serialNumber":configDict["serialNumber"],"index":"0", "viewIndex":"0", "cameraBoardUploadTime":str(current_milli_time())})
			print f
			#request = urllib2.Request("http://192.168.1.105:3000/index/uploadCameraPhoto", datagen, headers)
			#url should load from server, or changed by hand
			#request = urllib2.Request("http://192.168.1.105:3000/upload/single", datagen, headers)
			headers["User-agent"] = "Mozilla/5.0"
			print headers
			request = urllib2.Request("http://www.ncnll.com:3000/upload/single", datagen, headers)
			try:
				response = urllib2.urlopen(request,timeout=30)
				#print response.read()
				print "remote is ok"
			except Exception, e:
				print e
	os.remove(uploadImageName)

#Check is take photo time is arrived
#Check is take photo is closed
def isLocalTakePhotoOn():
	latestUploadTime=datetime.strptime(cameraConfigDict["latestLocalUploadTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
	currentTime = datetime.now()
	totalDiff = (currentTime-latestUploadTime).total_seconds()
	uploadShootInterval = cameraConfigDict["localShootInterval"]
	#print cameraConfigDict
	#print '------------------------'
	#print uploadShootInterval
	#print totalDiff
	if uploadShootInterval<=totalDiff :
		connPre = getSqliteDBConnection()
		execsql = "UPDATE CAMERACONFIG SET latestLocalUploadTime='%s' where serialNumber='%s' " % (str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")), str(cameraConfigDict["serialNumber"]),)
		connPre.execute(execsql)
		connPre.commit()
		return True
	else : 
		return False
	#execSql = "UPDATE CAMERACONFIG SET cameraType=%d, localShootInterval=%d, uploadShootInterval=%d, workingTime='%s', localResolution='%s', remoteResolution='%s', updateTime='%s', startDate='%s', endDate='%s', uploadPath='%s' where serialNumber='%s' " % (responseJson['rows'][0]['cameraType'], responseJson['rows'][0]['localShootInterval'], responseJson['rows'][0]['uploadShootInterval'], str(responseJson['rows'][0]['workingTime']), str(responseJson['rows'][0]['localResolution']), str(responseJson['rows'][0]['remoteResolution']), str(responseJson['rows'][0]['updateTime']), str(responseJson['rows'][0]['startDate']), str(responseJson['rows'][0]['endDate']), str(responseJson['rows'][0]['uploadPath']),str(responseJson['rows'][0]['serialNumber']),)

#Check is take photo time is arrived
#Check is take photo is closed
def isRemoteTakePhotoOn():
	latestUploadTime=datetime.strptime(cameraConfigDict["latestUploadTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
	currentTime = datetime.now()
	totalDiff = (currentTime-latestUploadTime).total_seconds()
	uploadShootInterval = cameraConfigDict["uploadShootInterval"]
	#print cameraConfigDict
	#print '------------------------'
	#print uploadShootInterval
	#print totalDiff
	if uploadShootInterval<=totalDiff :
		connPre = getSqliteDBConnection()
		execsql = "UPDATE CAMERACONFIG SET latestUploadTime='%s' where serialNumber='%s' " % (str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")), str(cameraConfigDict["serialNumber"]),)
		connPre.execute(execsql)
		connPre.commit()
		return True
	else : 
		return False
	#execSql = "UPDATE CAMERACONFIG SET cameraType=%d, localShootInterval=%d, uploadShootInterval=%d, workingTime='%s', localResolution='%s', remoteResolution='%s', updateTime='%s', startDate='%s', endDate='%s', uploadPath='%s' where serialNumber='%s' " % (responseJson['rows'][0]['cameraType'], responseJson['rows'][0]['localShootInterval'], responseJson['rows'][0]['uploadShootInterval'], str(responseJson['rows'][0]['workingTime']), str(responseJson['rows'][0]['localResolution']), str(responseJson['rows'][0]['remoteResolution']), str(responseJson['rows'][0]['updateTime']), str(responseJson['rows'][0]['startDate']), str(responseJson['rows'][0]['endDate']), str(responseJson['rows'][0]['uploadPath']),str(responseJson['rows'][0]['serialNumber']),)



#capture onboard camera image and send to local and remote server
def captureCSIImage():
	isOn = isLocalTakePhotoOn()
	if isOn:
		try:
			
			#camera.start_preview()
			# Camera warm-up time
			#time.sleep(1)
			#Get storage path
			onboard_storage_path = get_storage_path(cpu_serial)
			#Image name
			fileName = onboard_storage_path+str(current_milli_time())+".jpg"
			camera.capture(fileName)
			#camera.close()
			#camera.stop_preview()
			print "SHOOOOOTTTTTing CSI image"
			#sendImageToLocalAndRemoteServer(cpu_serial, fileName)
		except Exception,e:
			print str(e)


#capture usb camera image and send to local and remote server
def captureUsbImage(usbSerial, usbIndex):
	isOn = isLocalTakePhotoOn()
	if isOn:
		print "SHOOOOOTTTTTing USB image"
		#Get storage path
		onboard_storage_path = get_storage_path(usbSerial)
		#Image name
		imageName = onboard_storage_path+str(current_milli_time())+".jpg"
		#Capture image
		try:
			devicePath = "/dev/video"+usbIndex
			cam = pygame.camera.Camera(devicePath,(1920, 1080))
			cam.start()
			image=cam.get_image()
			#checkImagePath(cpu_serial, fileName)
			pygame.image.save(image, imageName)
			cam.stop()
			#sendImageToLocalAndRemoteServer(usbSerial, imageName)
		except Exception,e:
			print str(e)
	else:
		print "Usb send time is not arrived!--"+usbSerial

#Query camera config table to see whether should take a photo
def inspectCameraConfig():
	global cameraConfigDict
	#Add cpu serialNumber(onboard csi camera serialId)
	#boardCameraSerialNumber = getCpuSerial()
	#CSI camera
	cameraConfigDict = getCameraConfigInfo(cpu_serial)
	#if solution has been changed
	global localResolution
	global camera
	if localResolution != cameraConfigDict["localResolution"]:
		print 'not eauql haha---------------------'+cameraConfigDict["localResolution"]
		localResolution = cameraConfigDict["localResolution"]
		#restart camera
		camera.close()
		#init picamera
		camera = picamera.PiCamera()
		camera.resolution = (int(cameraConfigDict["localResolution"].split("*")[0]), int(cameraConfigDict["localResolution"].split("*")[1]))
	else:
		print localResolution
	captureCSIImage()

#Iterate the config table periodically
###Interval function to update config
def inspectCameraConfigIntervalTimer():
	inspectCameraConfig()
	#Update every 300 seconds
	Timer(1, inspectCameraConfigIntervalTimer).start()
#Application Start 
inspectCameraConfigIntervalTimer()
