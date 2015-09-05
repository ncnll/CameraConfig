from threading import Timer
import pygame
import pygame.camera #https://www.pygame.org/docs/ref/camera.html
import pygame.image
import time
import picamera
from datetime import datetime

#from subprocess import Popen, PIPE

#(stdout, stderr) = Popen(["cat","foo.txt"], stdout=PIPE).communicate()

import urllib2

current_milli_time = lambda: int(round(time.time() * 1000))



#Initiate the camera


try:
	camera = picamera.PiCamera()
	camera.resolution = (1024, 768)
	#camera.start_preview()
	# Camera warm-up time
	print "first sleep started"
	time.sleep(2)
	print "first sleep ended"
	#Image name
	fileName = str(current_milli_time())+".jpg"
	camera.capture(fileName)
	print "first captured ended"
	#camera.stop_preview()
	camera.close()
	print "first closed"
	print "1  SHOOOOOTTTTTing CSI image"
	time.sleep(2)
	#Again
	#camera.start_preview()
	camera = picamera.PiCamera()
	camera.resolution = (1024, 768)
	fileName = str(current_milli_time())+".jpg"
	camera.capture(fileName)
	#camera.stop_preview()
	camera.close()
	print "2 SHOOOOOTTTTTing CSI image"
	time.sleep(2)
except Exception,e:
	print str(e)

 