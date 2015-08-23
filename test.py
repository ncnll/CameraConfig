#!/usr/bin/python
import time
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

print int("0x"+iii["uploadShootInterval"], 0)