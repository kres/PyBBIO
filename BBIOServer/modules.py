#all these functions should be executed on a different thread
	#otherwise bye bye server!!

def n_blinks(n):
	'''n_blinks/<int:n>'''
	from bbio import *
	#blink pin USR1 at 1hz for n seconds
	pinMode('USR1', OUTPUT)
	for i in range(n*2):
		toggle(USR1)
		print "toggleing USR1"
		delay(500)
	return "done"
