import os
import random
import time
import subprocess
import sys
import multiprocessing
import shlex
from threading import Timer
import signal

image = ""
quote = ""
lyric = ""

def imgSettings():
	path = '/home/pi/images/'
	files = os.listdir(path)
	choice = random.choice(files)
	return path + choice

def quoteSettings():
	path = '/home/pi/quotes/'
	files = os.listdir(path)
	choice = random.choice(files)
	with open(path + choice) as f:
		lines = f.readlines()
		quote = random.choice(lines)
		return quote

def lyricSettings():
	path = '/home/pi/lyrics/'
	files = os.listdir(path)
	print(files)
	choice = random.choice(files)
	print(choice)
	with open(path + choice, 'r') as f:
		lines = f.read().replace('\n', ' ')
		lyric = lines.replace("\'", "")
		return lyric

colors = ["red", "green", "blue", "yellow", "orange", "purple", "indigo", "white"]


#add a space after the color
colors_id = {
	"red" : "255,0,0 ",
	"green" : "128,255,0 ",
	"blue" : "0,0,255 ",
	"yellow" : "255,255,0 ",
	"orange" : "255,128,0 ",
	"purple" : "127,0,255 ",
	"indigo" : "0,255,255 ",
	"white" : "255,255,255 "
	}

def apiFolder():
	os.chdir("/home/pi/display32x64/rpi-rgb-led-matrix/examples-api-use/")

def utilFolder():
	os.chdir("/home/pi/display32x64/rpi-rgb-led-matrix/utils/")

def ran_color():
	choice = random.choice(colors)
	chosen = colors_id[choice]
	return chosen

def images():
	utilFolder()
	image = imgSettings()
	return image

def quotes():
	apiFolder()
	setColor = ran_color()
	quote = quoteSettings()
	os.system("sudo ./scrolling-text-example --led-cols=64 -y 8 -l 1 -f ../fonts/9x18B.bdf -C " + setColor + quote)

def lyrics():
	apiFolder()
	setColor = ran_color()
	lyric = str(lyricSettings())
	os.system("""sudo ./scrolling-text-example --led-cols=64 -y 8 -l 1 -f ../fonts/9x18B.bdf -C """ + setColor + lyric)

#runs and kills a subprocess after timeout
def playImage():
	image = images()
	img = "sudo ./led-image-viewer --led-cols=64 " + image
	try:
		proc = subprocess.run(img, timeout=5, shell=True)
		#proc.wait(timeout=5)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
		#proc.send_signal(signal.CTRL-C-EVENT)
	finally:
		main()
def demo():
	try:
		cmd = "sudo ./demo -D 0 --led-cols=64"
		os.system(cmd)
	except:
		sys.exit()

def randomize():
	cmd = ['playImage()', 'quotes()', 'lyrics()']
	#cmd = ['lyrics()']
	choice = random.choice(cmd)
	eval(choice)

def main():
	try:
		while True:
			randomize()
	except:
		sys.exit()

if __name__ == "__main__":
	main()
