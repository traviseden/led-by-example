#Command line communications
import os

#time(sleep)
import time

#random numbers
import random

#Creates a shell to run program in parallel with python
import subprocess

#Used for sys.exit()
import sys

from threading import Timer

#Signal checks on the running program
import signal

image = ""
quote = ""
lyric = ""

#Loads a random image file in the paths location
def imgSettings():
	path = '/home/pi/images/'
	files = os.listdir(path)
	choice = random.choice(files)
	return path + choice

#Loads a random quote from a random file in paths location
def quoteSettings():
	path = '/home/pi/quotes/'
	files = os.listdir(path)
	choice = random.choice(files)
	with open(path + choice) as f:
		lines = f.readlines()
		quote = random.choice(lines)
		return quote

#Loads all the lyrics from a file in the paths location
def lyricSettings():
	path = '/home/pi/lyrics/'
	files = os.listdir(path)
	#print(files)
	choice = random.choice(files)
	#print(choice)
	with open(path + choice, 'r') as f:
		lines = f.read().replace('\n', ' ')
		lyric = lines.replace("\'", "")
		return lyric

def movieSettings():
	path = '/home/pi/movies/'
	files = os.listdir(path)
	choice = random.choice(files)
	return path + choice

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

#Change to folder
def apiFolder():
	os.chdir("/home/pi/display32x64/rpi-rgb-led-matrix/examples-api-use/")

#Change to folder
def utilFolder():
	os.chdir("/home/pi/display32x64/rpi-rgb-led-matrix/utils/")

#Pick a random color
def ran_color():
	choice = random.choice(colors)
	chosen = colors_id[choice]
	return chosen

#Pick a random image
def images():
	#utilFolder()
	image = imgSettings()
	return image

#Pick a random quote
def quotes():
	apiFolder()
	setColor = ran_color()
	quote = quoteSettings()
	os.system("sudo ./scrolling-text-example --led-cols=64 -s 10 -y 8 -l 1 -f ../fonts/9x18B.bdf -C " + setColor + quote)

#Pick random lyrics
def lyrics():
	apiFolder()
	setColor = ran_color()
	lyric = str(lyricSettings())
	os.system("""sudo ./scrolling-text-example --led-cols=64 -s 15 -y 8 -l 1 -f ../fonts/9x18B.bdf -C """ + setColor + lyric)

#runs and kills a subprocess after timeout
def playImage():
	image = images()
	#ranImgScroll = ['normal', 'forward','backward']
	ranImgScroll = ['normal']
	ranImgScrollChoice = random.choice(ranImgScroll)
	try:
		if ranImgScrollChoice == 'normal':
			utilFolder()
			img = "sudo ./led-image-viewer --led-cols=64 " + image
			proc = subprocess.run(img, timeout=5, shell=True)
			time.sleep(5)
		#PPM FILES ONLY not PNG
		#elif ranImgScrollChoice == 'forward':
		#	apiFolder()
		#	img = "sudo ./demo -D 1 " + image + " --led-cols=64 "
		#	proc = subprocess.run(img, timeout=5, shell=True)
		#elif ranImgScrollChoice == 'backward':
		#	apiFolder()
		#	img = "sudo ./demo -D 2 " + image + " --led-cols=64 "
		#	proc = subprocess.run(img, timeout=5, shell=True)
		#else:
		#	print("Failed Trying")
		#	img = "sudo ./led-image-viewer --led-cols=64 " + image
		#	proc = subprocess.run(img, timeout=5, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
	finally:
		#sys.exit()
		main()

#Select which demo and settings to run
def demo():
	apiFolder()
	demos = ['0','4','6','7','8','9','10','11']
	chosen = random.choice(demos)
	cmd = "sudo ./demo -D " + chosen + " --led-cols=64 "
	try:
		if chosen == '0':
			proc = subprocess.run(cmd, timeout=60, shell=True)
			time.sleep(60)
		elif chosen == '4':
			cmd = cmd + "--led-brightness=50 "
			proc = subprocess.run(cmd, timeout=20, shell=True)
			time.sleep(20)
		elif chosen == '6':
			cmd = cmd + "--led-brightness=70 "
			proc = subprocess.run(cmd, timeout=180, shell=True)
			time.sleep(180)
		elif chosen == "7":
			cmd = cmd + "--led-brightness=70 -m 500 "
			proc = subprocess.run(cmd, timeout=150, shell=True)
			time.sleep(150)
		elif chosen == "8":
			cmd = cmd + "--led-brightness=70 "
			proc = subprocess.run(cmd, timeout=120, shell=True)
			time.sleep(120)
		elif chosen == "9":
			cmd = cmd + "--led-brightness=70 "
			proc = subprocess.run(cmd, timeout=15, shell=True)
			time.sleep(15)
		elif chosen == "10":
			cmd = cmd + "--led-brightness=70 -m 250 "
			proc = subprocess.run(cmd, timeout=10, shell=True)
			time.sleep(10)
		elif chosen == "11":
			proc = subprocess.run(cmd, timeout=10, shell=True)
			time.sleep(10)
		else:
			proc = subprocess.run(cmd, timeout=10, shell=True)
			time.sleep(10)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
	finally:
		#sys.exit()
		main()

def playMovie():
	movie = movieSettings()
	utilFolder()
	cmd = "sudo ./video-viewer --led-cols=64 " + movie
	try:
		proc = subprocess.run(cmd, timeout=60, shell=True)
	except subprocess.TimeoutExpired:
		pgid = os.getpgid(os.getpid())
		if pgid == 1:
			os.kill(os.getpid(), signal.CTRL_C_EVENT)
		else:
			os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
	finally:
		main()


#ToDO
#def btcPrice():
#def currenttime():
#def news()
#def customMovies()

#Pick which types of media will run. Used to isolate and troubleshoot.
def randomize():
	#cmd = ['demo()']
	cmd = ['demo()', 'playImage()', 'quotes()', 'lyrics()']
	choice = random.choice(cmd)
	eval(choice)

#Main program should run always, on boot.
def main():
	try:
		while True:
			randomize()
	except:
		randomize()
		#sys.exit()

if __name__ == "__main__":
	main()
