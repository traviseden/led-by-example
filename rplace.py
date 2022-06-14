#!/usr/bin/python3
import os, sys
import random
from PIL import Image
import numpy
import subprocess
from threading import Timer
import signal
import time

#return the image size (20x20) to a file called image.info
def getInfoFile():
	path = "/home/pi/rplace/"
	files_png = path + "png/"
	choice = random.choice(os.listdir(files_png))
	if os.path.exists(path + "image.info"):
		os.remove(path + "image.info")
	os.system("file " + "/home/pi/rplace/png/" + choice + " > /home/pi/rplace/image.info")

#set the size of the image from the file to a variable
def getSize():
	with open("/home/pi/rplace/image.info", "r") as f:
		lines = f.read()
		listed = lines.split(",")
		pixels = listed[1]
		pixels = pixels.split("x")
		pixels_l = int(pixels[0])
		pixels_w = int(pixels[1])
	return(pixels_l, pixels_w)

#Random pixel starting point based on image size
#We are going to pick a pixel at random, at least 64x32 away from the edge
def ranPix(pixels_l, pixels_w):
	ran_l = random.randint(0, pixels_l - 77)
	ran_w = random.randint(0, pixels_w - 109)
	return(ran_l, ran_w)

#Crop the image and the images around it.
#Create a gif using the images and moving in patterns to scan over the image

def getDirection():
	dirs = ["North", "NE", "East", "SE", "South", "SW", "West", "NW"]
	ran_dir = random.choice(dirs)
	return(ran_dir)


def cropImages(ran_l, ran_w, ran_dir):
	global count
	count = 1
	l = ran_l
	w = ran_w
	image = Image.open("/home/pi/rplace/png/rplace.png")
	image_arr = numpy.array(image)
	while count < 10:
		image_arr2 = image_arr[l:l+32, w:w + 64]
		image = Image.fromarray(image_arr2)
		filename = "Crop{0}.png".format(count)
		count += 1
		image.save("/home/pi/rplace/jpg/" + filename, "PNG")
		#Move
		if ran_dir == "North":
			l = l - 5
		elif ran_dir == "East":
			w = w + 5
		elif ran_dir == "NE":
			l = l - 5
			w = w + 5
		elif ran_dir == "SE":
			l = l + 5
			w = w + 5
		elif ran_dir == "SW":
			l = l + 5
			w = w - 5
		elif ran_dir == "NW":
			l = l - 5
			w = w - 5
		elif ran_dir == "South":
			l = l + 5
		elif ran_dir == "West":
			w = w - 5

def delImages():
	files_jpg = "/home/pi/rplace/jpg/"
	delAllImages = os.listdir(files_jpg)
	if os.path.exists(files_jpg):
		for each in delAllImages:
			print("Deleting: " + files_jpg + each)
			os.remove(files_jpg + each)

def displayImage():
	playingImage = "sudo /home/pi/display32x64/rpi-rgb-led-matrix/utils/led-image-viewer -t0.5 --led-cols=64 /home/pi/rplace/jpg/*.png"
	try:
		proc = subprocess.run(playingImage, timeout=30, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
	finally:
		None

def playWarning():
	warning = "sudo /home/pi/display32x64/rpi-rgb-led-matrix/utils/text-scroller --led-cols=64 -l 1 -y 8 -s 8 -f /home/pi/display32x64/rpi-rgb-led-matrix/fonts/9x18.bdf Loading Images Please Wait"
	try:
		proc = subprocess.run(warning, timeout=5, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)

	finally:
		None
def main():
	try:
		plays = 1
		while plays > 0:
			choice = getInfoFile()
			pixels_l, pixels_w = getSize()
			ran_dir = getDirection()
			ran_l, ran_w = ranPix(pixels_l, pixels_w)
			cropImages(ran_l, ran_w, ran_dir)
			ran_dir = getDirection()
			displayImage()
			plays -= 1
			if plays > 1:
				delImages()
	except:
		None
		delImages()
		#main()
if __name__ == "__main__":
	main()
