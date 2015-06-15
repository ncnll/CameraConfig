#!/usr/bin/python
from threading import Timer
from threading import Thread
from os import listdir
import urllib2,urllib
import os.path
import os
import json
import sqlite3
import threading

strtest = "usb-046d_0825_99999990-video-index2"
print strtest[-1:]