from flask import Flask, request
from bbio import *
import modules 
import inspect

import atexit
atexit.register(bbio.bbio_cleanup)

bbio.bbio_init()
app = Flask(__name__)

@app.route("/")
def index():
	return "Welcome to BBIO Server"


#TODO : replace all the "0" in 404 errors with a better error response


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
		

@app.route("/pwm/<module>", methods = ['GET'])
def pwm(module):
	'''
	The function to handle PWM requests. as of now pwm to work with default configuration.
	i.e. freq = 10KHz and resolution = 8 bit

	pin to pwm mapping :-
	P8.13 - PWM2B
	P8.19 - PWM2A
	P9.14 - PWM1A
	P9.16 - PWM1B

	GET /pwm/1A?value=10
	'''
	value = request.args.get("value", None)

	if (module not in ['1A','1B','2A','2B']) or (not value):
		#error in url
		return "0", 404

	module = "PWM" + module
	print "writing value :", value, "to module :", module
	analogWrite(module, max(value, 255))
	return '1'

@app.route("/adc/<channel>")
def adc(channel):
	'''
	function to handle ADC read requests. 
	Input can be from 0 - 1.8V, o/p of 12 bit resolution

	P9.33 - AIN4
	P9.35 - AIN6
	P9.36 - AIN5
	P9.37 - AIN2
	P9.38 - AIN3
	P9.39 - AIN0

	GET /adc/AIN0 => returns the analog input at channel 0
	'''
	if channel not in ['AIN'+str(ch) for ch in range(7)]:
		#url error
		return "0", 404
	
	else :
		return str(analogRead(channel))
	

all_routes = inspect.getmembers(modules, inspect.isfunction)

for i in all_routes:
	app.add_url_rule("/custom/"+ i[1].__doc__, i[0], i[1])

if __name__ == "__main__":	
	app.run("0.0.0.0")


