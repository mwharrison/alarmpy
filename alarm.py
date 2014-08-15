#!/usr/bin/python
import urllib2
import piface.pfio as pfio

from datetime import datetime
from time import sleep

#connect to mysql
#db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                     user="root", # your username
#                      passwd="", # your password
#                      db="delano") # name of the database

# Cursor object for using mysql.
# cur = db.cursor() 

def notify(sensor, status):
#	cur = db.cursor()
#	now = datetime.now()
	print sensor + ' ' + status
#	try:
#		cur.execute("""INSERT INTO alarm (time, sensor, status) VALUES (%s, %s, %s)""", (now, sensor, status))
#		db.commit()
#	except:
#		print "DB WRITE ERROR"
#		db.rollback()
	
	## We used to send to a web service, leving this here for reference later - if we want to do away with mysql
	script_path = "http://10.0.2.2:8001/alarm/update/%s/%s/" % (str(sensor), str(status))
	try:
		rt=urllib2.urlopen(script_path)
	except urllib2.HTTPError:
		print "HTTP Error"
		return False
#	cur.close()

pfio.init()
prev_patio=None
prev_entry=None
prev_motion=None

while(1):                
	patio=pfio.digital_read(4)
	data=[patio]
	if patio != prev_patio:
		if data[0]==0:
			notify('patio','open')
		if data[0]==1:
			notify('patio','closed')
		prev_patio = patio
		
	entry=pfio.digital_read(5)
	data=[entry]
	if entry != prev_entry:
		if data[0]==0:
			notify('entry','open')
		if data[0]==1:
			notify('entry','closed')
		prev_entry = entry
		
	motion=pfio.digital_read(6)
	data=[motion]
	if motion != prev_motion:
		if data[0]==0:
			notify('motion','detected')
		if data[0]==1:
			notify('motion','none')
		prev_motion = motion
		
	sleep(.2)
