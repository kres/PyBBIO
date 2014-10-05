from flask import Flask
from bbio import *

bbio.bbio_init()

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
	#get the pin 
	pin = "GPIO" + bank + "_" + pin

	if request.method == 'GET':
		task = request.args.get("task", None)
		
		if task == "config":
			#TODO :: is this a valid useable pin?
			pin_mode = request.args.get("mode", None)
			if not pin_mode:
				return "0", 404
			pin_mode = pin_mode.upper()
			pinMode(pin, pin_mode)
			return "1"

		elif task == "read":
			#TODO :: make sure pin is readable?
			return str(digitalRead(pin))

		elif task == "write":
			pin_state = request.args.get("output", None)
			if not pin_state:
				#error in url
				return "0", 404
			
			#make sure pin_state is only capitals
			pin_state = pin_state.upper()

			#TODO :: should I make sure that this pin is writable
				#or does PyBBIO handle it for me?
			digitalWrite(pin, pin_state)
			
			#everything ok
			return "1"
		
		else :
			#error in url
			return "0", 404

	else :
		#have an allowance for POST, PUT later on
		#nice way to send json objects
		pass
		

if __name__ == "__main__":
	app.run()
	bbio.bbio_cleanup()
