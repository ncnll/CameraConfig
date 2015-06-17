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

#from subprocess import Popen, PIPE

#(stdout, stderr) = Popen(["cat","foo.txt"], stdout=PIPE).communicate()

import urllib2

pygame.init()
pygame.camera.init()

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

#Change row to dict
def dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

#Get config table info
def getCameraConfigInfo(serialNumber):
	#if db is not exist
	directory_path = '/home/pi/database/uploadconfig/'
	uploadConfig_file_path=directory_path+'uploadConfig.db'
	if not os.path.exists(uploadConfig_file_path) :
		return None
	connPre = sqlite3.connect(uploadConfig_file_path)#/home/pi/database/test.db
	cPre=connPre.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CAMERACONFIG'")
	row1 = cPre.fetchone()
	if row1 is None :
		return None
	else : 
		print row1[0]
		cPre=connPre.execute("SELECT * FROM CAMERACONFIG")
		row1 = cPre.fetchone()
		print row1[0]
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
	#Compare time
	#Send to remote server
	register_openers()#How to use this?
	with open(uploadImageName, 'r') as f:
		datagen, headers = multipart_encode({"file":f,"serialNumber":configDict["serialNumber"],"index":"0", "viewIndex":"0"})
		request = urllib2.Request("http://192.168.1.105:8091/index/uploadCameraPhoto", datagen, headers)
		try:
			response = urllib2.urlopen(request,timeout=30)
			#print response.read()
		except Exception, e:
			print e
			#Record failure
	os.remove(uploadImageName)

#capture onboard camera image and send to local and remote server
def captureCSIImageAndSendOut(cpuSerial):
	#print cpuSerial
	configDict = getCameraConfigInfo(cpuSerial)
	#print configDict

#capture usb camera image and send to local and remote server
def captureUsbImageAndSendOut(usbSerial, usbIndex):
	#Image name
	imageName = str(current_milli_time())+".jpg"
	#Capture image
	try:
		devicePath = "/dev/video"+usbIndex
		cam = pygame.camera.Camera(devicePath,(1920, 1080))
		cam.start()
		image=cam.get_image()
		pygame.image.save(image, imageName)
		cam.stop()
	except Exception,e:
		print str(e)
	sendImageToLocalAndRemoteServer(usbSerial, imageName)

#Query camera config table to see whether should take a photo
def inspectCameraConfig():
	#Add cpu serialNumber(onboard csi camera serialId)
	boardCameraSerialNumber = getCpuSerial()
	captureCSIImageAndSendOut(boardCameraSerialNumber)
	#Add usb camera serialNumber
	stdout = os.listdir("/home/pi/v4l/by-id/")
	for line in stdout:
		usbserial=line[4:22]
		usbIndex=line[-1:]
		captureUsbImageAndSendOut(usbserial, usbIndex)

#Iterate the config table periodically
###Interval function to update config
def inspectCameraConfigIntervalTimer():
	#Update every 300 seconds
	Timer(10, inspectCameraConfigIntervalTimer).start()
	inspectCameraConfig()
#Application Start 
inspectCameraConfigIntervalTimer()



	