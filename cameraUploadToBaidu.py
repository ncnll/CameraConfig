from threading import Timer
from threading import Thread

import time
import picamera
import threading



#!/usr/bin/env python
#coding:utf8

import os
import logging
import pybcs 

#Get raspberry pi serial id
def getserial():
	# Extract serial from cpuinfo file
	cpuserial = "0000000000000000"
	try:
		f = open('/proc/cpuinfo','r')
		for line in f:
			if line[0:6]=='Serial':
				cpuserial = line[10:26]
		f.close()
	except:
	  cpuserial = "ERROR000000000"
	return cpuserial


pybcs.init_logging(logging.INFO)

AK = ''         
SK = ''    
BUCKET='charmyinbucket'

bcs = pybcs.BCS('http://bcs.duapp.com/', AK, SK, pybcs.HttplibHTTPC)  

# lst = bcs.list_buckets()
# print '---------------- list of bucket : '
# for b in lst:
    # print b
# print '---------------- list end'

#declare bucket
b = bcs.bucket(BUCKET)

print b.get_acl()['body']

#Initiate the camera
camera = picamera.PiCamera()

camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
time.sleep(2)

#Serial number
serialNumber = getserial()

#Count image shot times
shotCount = 1
#Limit count to reset shotCount
limitCount = 20/10
#currenImage
currentImage='';
#previousUploadedImage
previousUploadedImage='';

#Capture image and save in local storage
def captureImage():
	global camera
	global shotCount
	global limitCount
	global b
	global currentImage
	
	#Set a clock
	t = Timer(5.0, captureImage)
	t.start() # after 30 seconds, "hello, world" will be printed
	
	fileName = str(time.time())+'foo.jpg'
	camera.capture(fileName)
	print str(shotCount)+"-hello, world", time.time()
	#This should be record in sqlite
	currentImage = fileName


#Upload images to server
def uploadImage():
	global currenImage
	global previousUploadedImage
	#Set up a interval colck do work every 10 seconds
	t = Timer(10.0, uploadImage)
	t.start() # after 30 seconds, "hello, world" will be printed
	#If current image has not been uploaded, read from the sqlite
	if currentImage != previousUploadedImage :
		o = b.object('/'+serialNumber+'/'+currentImage)
		respon = o.put_file(currentImage)
		print "Uploading images status -- " + str(respon['status'])
		if respon['status']==200 :
			previousUploadedImage = currentImage
			print "Uploading images success -- " + "/" + serialNumber + "/" + currentImage 


t1 = Thread(target=captureImage)
t1.start()

t2 = Thread(target=uploadImage)
t2.start()
