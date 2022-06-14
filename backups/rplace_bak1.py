#!/usr/bin/python3
import os, sys
import random
from PIL import Image
import numpy
import subprocess
from threading import Timer
import signal
import time

path = "/home/pi/rplace/"
files_png = path + "png/"
files_jpg = path + "jpg/"
files_gif = path + "gif/"

#return the image size (20x20) to a file called image.info
def getInfoFile():
	choice = random.choice(os.listdir(files_png))
	#print(choice)
	if os.path.exists(path + "image.info"):
		os.remove(path + "image.info")
		#print("Removed image.info file.")
	os.system("file " + "/home/pi/rplace/png/" + choice + " > /home/pi/rplace/image.info")
	return(choice)

def getSize():
	with open(path + 'image.info', "r") as f:
		lines = f.read()
		listed = lines.split(",")
		pixels = listed[1]
	return(pixels)

os.chdir(path)

#filename as string
choice = str(getInfoFile())

#pixel size
pixels = getSize()
pixels_split = pixels.split('x')
pixels_l = int(pixels_split[0])
pixels_w = int(pixels_split[1])
print("Pixels: " + pixels)
print("Width: " + str(pixels_w))
print("Length: " + str(pixels_l))
width = 62
length = 32

#Random pixel starting point based on image size
#We are going to pick a pixel at random, at least 64x32 away from the edge
def ranPix(pixels_w, pixels_l):
	ran_w = random.randint(0, pixels_w - 64)
	ran_l = random.randint(0, pixels_l - 32)
	return(ran_w, ran_l)

w,l = ranPix(pixels_w, pixels_l)
print(w,l)

#Crop the image and the images around it.

#how many times can we pan w or l
#image multiplier i_w_m i_l_m
i_w_m = pixels_w // 64
i_l_m = pixels_l // 32
print(i_w_m)
print(i_l_m)

#Create a gif using the images and moving in patterns to scan over the image
count = 1
def cropImages():
	image = Image.open("/home/pi/rplace/png/rplace.png")
	image_arr = numpy.array(image)
	image_arr = image_arr[l:l+32, w:w + 64]
	image = Image.fromarray(image_arr)
	#filename = "Crop.png"
	filename = "Crop{0}.png".format(count)
	image.save(files_jpg + filename, "PNG")
	return(filename)

def delImages():
	delAllImages = os.listdir(files_jpg)
	for each in delAllImages:
		print("Deleting: " + files_jpg + each)
		os.remove(files_jpg + each)

def displayImage():
	filename = cropImages()
	playingImage = "sudo /home/pi/display32x64/rpi-rgb-led-matrix/utils/led-image-viewer --led-cols=64 ~/rplace/jpg/" + filename
	try:
		proc = subprocess.run(playingImage, timeout=3, shell=True)
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
		count = 1
		directions = ["North", "East", "South", "West"]
		north = l - 1
		east = w + 1
		south = l + 1
		west = w - 1

		direction_choice = random.choice(directions)
		print(direction_choice)

		while count < 5:
			displayImage()
		count += 1
		print(w,l, north, east, south, west)
		if direction_choice == "North":
			w = north
		elif direction_choice == "East":
			l = east
		elif direction_choic == "South":
			w = south
		elif direction_choice == "West":
			l = west
		print(w,l)
	except:
		delImages()
		displayImage()
if __name__ == "__main__":
	main()

