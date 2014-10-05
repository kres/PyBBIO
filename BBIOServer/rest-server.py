from flask import Flask, request
from bbio import *

import atexit
atexit.register(bbio.bbio_cleanup)

bbio.bbio_init()
app = Flask(__name__)

@app.route("/")
def index():
	return "Welcome to BBIO Server"

@app.route("/gpio/<int:bank>/<int:pin>", methods = ['GET','POST'])
def gpio(bank, pin):
	'''
	This is the handler for GPIO actions. to setup/read/write to GPIO
	eg: GET	/gpio/1/16?task=write&state=HIGH	:: sets pin GPIO1_16 high
	    GET	/gpio/1/16?task=config&mode=INPUT	:: sets pin to input mode
	    GET /gpio/1/16?task=read			:: reads pin, returns status
	'''
	print "In GPIO handler"
	bank = str(bank)
	pin = str(pin)
	#get the pin 
	pin = "GPIO" + bank + "_" + pin

	pin_map = {
			'GPIO1_22' : 'USR1'
			#TODO :: add other entries
		}

	pin = pin_map.get(pin, pin)

	if request.method == 'GET':
		task = request.args.get("task", None)
		print "GET request"		
		if task == "config":
			#TODO :: is this a valid useable pin?
			pin_mode = request.args.get("mode", None)
			if not pin_mode:
				return "0", 404
			pin_mode = pin_mode.upper()
			pin_mode = 1 if pin_mode == 'HIGH' else 0

			print "CONFIG : ", pin, pin_mode
			try:
				pinMode(pin, pin_mode)
				print "pin-mode success"

			except Exception as e:
				print "unsuccessful"
				return "0"
			return "1"

		elif task == "read":
			#TODO :: make sure pin is readable?
			return str(digitalRead(pin))

		elif task == "write":
			pin_state = request.args.get("state", None)
			if not pin_state:
				#error in url
				return "0", 404
			
			#make sure pin_state is only capitals
			pin_state = pin_state.upper()
			pin_state = 1 if pin_state == 'HIGH' else 0

			#TODO :: should I make sure that this pin is writable
				#or does PyBBIO handle it for me?
			try:
				digitalWrite(pin, pin_state)
			except Exception as e:
				print "problem with digital write"
				return "0"
			
			#everything ok
			print "digitalWrite success"
			return "1"
		
		else :
			#error in url
			return "0", 404

	else :
		#have an allowance for POST, PUT later on
		#nice way to send json objects
		pass
		

if __name__ == "__main__":
	app.run("0.0.0.0")
