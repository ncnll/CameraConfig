from threading import Timer
import pygame
import pygame.camera #https://www.pygame.org/docs/ref/camera.html
import pygame.image
from pygame.locals import *
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

import threading
import os

#from subprocess import Popen, PIPE

#(stdout, stderr) = Popen(["cat","foo.txt"], stdout=PIPE).communicate()

import urllib2

pygame.init()
pygame.camera.init()

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
	dict_factory = {"a":1,"b":2}
	return dict_factory

#capture onboard camera image and send to local and remote server
def captureCSIImageAndSendOut(cpuSerial):
	print cpuSerial
	configDict = getCameraConfigInfo(cpuSerial)
	print configDict

#capture usb camera image and send to local and remote server
def captureUsbImageAndSendOut(usbSerial):
	#Capture image
	try:
		devicePath = "/dev/video"+usbSerial[-1:]
		cam = pygame.camera.Camera(devicePath,(1920, 1080))
		cam.start()
		image=cam.get_image()
		pygame.image.save(image, "image.jpg")
		cam.stop()
	except Exception,e:
		print str(e)
	register_openers()
	with open("image.jpg", 'r') as f:
		cpuserial = getCpuSerial()
		datagen, headers = multipart_encode({"file":f,"deviceCpuId":cpuserial,"index":"0","productItemId":"5565d304b09f8dd00cca2ff0", "viewIndex":"0"})
		request = urllib2.Request("http://192.168.1.105:8091/index/uploadCameraPhoto", datagen, headers)
		response = urllib2.urlopen(request)
		#remote server not work storage in local server
		print response.info()
		print response.geturl()
		print response.getcode()
		print response.read()
	print usbSerial
	configDict = getCameraConfigInfo(usbSerial)
	print configDict

#Query camera config table to see whether should take a photo
def inspectCameraConfig():

	#Add cpu serialNumber(onboard csi camera serialId)
	boardCameraSerialNumber = getCpuSerial()
	captureCSIImageAndSendOut(boardCameraSerialNumber)
	#Add usb camera serialNumber
	stdout = os.listdir("/home/pi/v4l/by-id/")
	for line in stdout:
		usbserial=line[4:22]
		captureUsbImageAndSendOut(usbserial)

#Iterate the config table periodically
###Interval function to update config
def inspectCameraConfigIntervalTimer():
	#Update every 300 seconds
	Timer(3, inspectCameraConfigIntervalTimer).start()
	inspectCameraConfig()
#Application Start 
inspectCameraConfigIntervalTimer()



	