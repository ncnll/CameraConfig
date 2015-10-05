#!/usr/bin/python

from threading import Timer
from threading import Thread

import time
import picamera
import threading



#!/usr/bin/env python
#coding:utf8

import os
import logging

from datetime import datetime
#from dateutil.parser import parse
#current_milli_time = lambda: int(round(time.time() * 1000))
#print current_milli_time()
#strtest = "usb-046d_0825_99999990-video-index2"
#print strtest[-1:]

#print current_milli_time()

timeStr = "2015-08-23T15:22:41.519Z"
d=datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%fZ")
now_time = datetime.now()
totl = (now_time-d).total_seconds()
#d = parse(timeStr)
print totl

iii = {"uploadShootInterval":12}
print iii["uploadShootInterval"]

current_milli_time = lambda: int(round(time.time() * 1000))
print current_milli_time()
strtest = "usb-046d_0825_99999990-video-index2"
#print strtest[-1:]
#print current_milli_time()

epochTimeStr = time.gmtime(time.time())
#print epochTimeStr
timeStr = "2015-06-07T16:10:41.519Z"
isoTime = time.strptime(timeStr,'%Y-%m-%dT%H:%M:%S.%fZ')
# print isoTime

lastUploadRemoteTime = time.strptime("2015-06-19T10:10:42.519Z","%Y-%m-%dT%H:%M:%S.%fZ")
print type(lastUploadRemoteTime)

#print current_milli_time()/1000
#print int(round(time.mktime(lastUploadRemoteTime)))
secondsBetween = current_milli_time()/1000-int(round(time.mktime(lastUploadRemoteTime)))
print secondsBetween/60
# 04fa1b15f3953d8e880ac7aa68f1e32e922e67ea



print datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


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
print getserial()