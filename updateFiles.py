#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Update file, once per day check for updates

#import requests
#import json
import sys
import os
#import time

def update():
	#local(Testnet/Lan)
	os.system("rsync -az pi@192.168.1.114:/var/www/html/remote/pi_celeste/ /home/pi")
	#remote(internet)
	#os.system("rsync -az -e 'ssh -p 2233' pi@24.60.131.10:/var/www/html/remote/pi_celeste/ /home/pi")

count = 3

try:
	update()
except:
	while count > 0:
		count -= 1
		sleep(30)
		update()


