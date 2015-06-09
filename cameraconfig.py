#!/usr/bin/python
from os import listdir
import urllib2,urllib

stdout = listdir("/home/pi/v4l/by-id/")
for line in stdout:
	usbserial=line[4:22]
	print usbserial
	para_dct = {}
	para_dct['search_eq_serialNumber'] = usbserial
	url = """http://192.168.1.105:8091/device/camera/searchList"""
	para_data = urllib.urlencode(para_dct)
	response = urllib2.urlopen(url, para_data)
	print response.info()
	print response.geturl()
	print response.getcode()
	print response.read()

print stdout
