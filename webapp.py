import os
import subprocess
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
quotes_file = os.path.join(basedir, 'quotes/quotes.txt')

# simplest example
# layout for ALL PAGES is in templates/base.html
# this route is in hello.html
@app.route("/", methods=["GET"])
def hello_world():
    return render_template("hello.html")

# this is an API route
# NOT a page, like above, which uses render_template()
# does NOT use base.html
# returns json instead with jsonify(DATA)
# it gets called by page using JavaScript
# not sure if this True/False actually does anything?
# should return {error: true} or {error:false}
# and then only remove quote from ui when true
@app.route("/quotes/<line>", methods=["POST"])
def delete_quote(line=None):
	if line != None:
		cmd = "sed -i '" + line + "d' " + quotes_file
		# should use subprocess instead?
		os.system(cmd)
		return jsonify(error=False)
	return jsonify(error=True)

# multiple actions on one route (GET, POST)
# sometimes you want them separate but these show the same data
@app.route("/quotes", methods=["GET", "POST"])
def read_quotes():
	# echoing in the new quote only happens on a post
	if request.method == "POST":
		os.system("echo \"" + request.form["quote"]  + "\" >> " + quotes_file)

	# reading the file happens with every request
	# so on a POST the file is edited and then read
	# keeps code simple and data fresh
	quotes = []
	with open(quotes_file, "r") as file:
		for line in file.readlines():
			quotes.append(line.rstrip())
	return render_template("quotes.html", quotes=quotes)

# just a list for now
@app.route("/wifi")
def list_wifi():
	b_networks = subprocess.check_output("sudo iw dev wlan0 scan | grep SSID | grep -v \"List\" | cut -c8- | sed '/^$/d'", shell=True).splitlines()
	# b_networks is a list of binary strings
	# map applies the function to each element in the list
	# and returns a new list
	networks = map(lambda x: x.decode('UTF-8'), b_networks)
	return render_template("wifi.html", networks=networks)

