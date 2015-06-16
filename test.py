#!/usr/bin/python
import time
current_milli_time = lambda: int(round(time.time() * 1000))
print current_milli_time()
strtest = "usb-046d_0825_99999990-video-index2"
print strtest[-1:]

print current_milli_time()