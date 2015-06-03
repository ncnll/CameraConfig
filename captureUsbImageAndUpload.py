import pygame
import pygame.camera
import pygame.image
from pygame.locals import *
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

import urllib2

pygame.init()
pygame.camera.init()

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


cam = pygame.camera.Camera("/dev/video0",(1920, 1080))
cam.start()
image=cam.get_image()
pygame.image.save(image, "image.jpg")

register_openers()

with open("image.jpg", 'r') as f:
	cpuserial = getserial()
	datagen, headers = multipart_encode({"file":f,"deviceCpuId":cpuserial,"index":"0","productItemId":"5565d304b09f8dd00cca2ff0", "viewIndex":"0"})
	request = urllib2.Request("http://192.168.1.101:8091/index/uploadCameraPhoto",datagen, headers)
	response = urllib2.urlopen(request)
	print response.info()
	print response.geturl()
	print response.getcode()
	print response.read()
