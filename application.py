from flask import Flask, render_template
from flask import request, jsonify, make_response
from datetime import datetime
import json
import requests
import sys
import os
import mysql.connector

ENDPOINT = "med-live-db2.c2kufiynjcx0.us-east-2.rds.amazonaws.com"
USR = "admin"
PWD = "meditate123"
PORT = "3306"
REGION = "us-east-2"
DBNAME = "medlivedb2"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
BEARER = '05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b'
DAILY_API = "https://api.daily.co/v1/rooms/"
SCHED_TIMES_UTC = [0,12,18]

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

@app.route('/api/timedata') ##returns time data
def timedata():
	
	data = {} #json response
	time_current = datetime.utcnow() #captures current time
	data['time_current'] = time_current.isoformat() #captures current time
	data['n_sched_times'] = len(SCHED_TIMES_UTC)

	#determine sched time from get request
	sched_query = request.args.get('sched', default = None, type = str)
	if (sched_query):
		try:
		  	sched_parse = sched_query.split("-")
		  	print(sched_parse)
		  	sched_month = int(sched_parse[0])
		  	sched_day = int(sched_parse[1])
		  	sched_year = 2000 + int(sched_parse[2])
		  	sched_hour = int(sched_parse[3])
		  	sched_min = int(sched_parse[4])
		except:
			print("could not parse sched time request")
			data['error'] = "could not parse sched request"
			return json.dumps(data)
	else: #by default, set sched as next sched time in list
		print("using default sched time")
		sched_time_bool = False
		sched_year = time_current.year
		sched_month = time_current.month
		sched_min = 0
		for t in SCHED_TIMES_UTC:
			if time_current.hour < t:
				print("next sched time:",t)
				sched_day = time_current.day
				sched_hour = t
				sched_time_bool = True
				break
		if not sched_time_bool: #set sched as next day first time
			print("sched time next day")
			sched_day = time_current.day + 1
			sched_hour = SCHED_TIMES_UTC[0]
	
	#build time sched object and add to data json
	time_sched = datetime(sched_year,sched_month,sched_day,sched_hour,sched_min)
	data['time_sched'] = time_sched.isoformat() #captures scheduled time
	data['sched_year'] = sched_year
	data['sched_month'] = sched_month
	data['sched_day'] = sched_day
	data['sched_hour'] = sched_hour
	data['sched_min'] = sched_min
	
	time_diff = (time_sched-time_current).total_seconds() #captures time difference
	data['time_diff'] = time_diff

	if time_current < time_sched: #if sched time has passed, set bool to kick out
		data['kick_out'] = False
	else:
		data['kick_out'] = True

	return json.dumps(data)

@app.route('/api/requestroom', methods=["POST"]) #returns assigned room data
def requestroom():

	#check for clientID
	req = request.get_json()
	if 'clientID' in req:
		client_id = req['clientID']

	if client_id == None:
		client_id = "dummy"

	print("client ID:",client_id)

	data = {} #data to be returned
	data['user_name'] = client_id

	#if test room, use user ID to name vid room
	if 'testRoom' in req:
		room_name = client_id

	#otherwise use DB for real rooms	
	else: 
		#connect to DB
		try:
			conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
			cur = conn.cursor(buffered=True)
			print(client_id,": passed DB credentials")
		except:
			print(client_id,": did not pass DB credentials")
			data['error'] = "unable to connect with DB"
			return json.dumps(data)


		#check if user is already in active_users table
		cmd = "SELECT * FROM active_users WHERE user_name = %s"
		try:
			cur.execute(cmd,(client_id,))
			print(client_id, ": does user exist1? ","yes" if cur.rowcount > 0 else "no")
			if cur.rowcount > 0 :
				print(client_id,": error, user already exists")
				data['error'] = "you are already assigned a room"
				return json.dumps(data)
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "failed to connect to DB on query 1"
			return json.dumps(data)

		#insert user into active_users table
		cmd = "INSERT INTO active_users(user_name) VALUES (%s)" #add to active_users table
		try:
			cur.execute(cmd,(client_id,))
			conn.commit()
			print("inserted user in table")
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			conn.rollback()
			data['error'] = "failed to connect to DB on query 2"
			return json.dumps(data)

		#get entry order for user
		cmd = "SELECT entry_order FROM active_users WHERE user_name = %s"
		try:
			cur.execute(cmd,(client_id,))
			print("does user exist2? ","yes" if cur.rowcount > 0 else "no")
			if cur.rowcount > 0 :
				entry_order = cur.fetchone()[0]
				data['entry_order'] = entry_order #captures entry order
				print("entry order:",entry_order)
			else :
				print("error, user does not exist")
				data['error'] = "you are missing from DB"
				return json.dumps(data)
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "failed to connect to DB on query 3"
			return json.dumps(data)

		conn.close() #close DB connection

		#assigns room based on entry_order
		room_number = (entry_order + 1) // 2
		room_name = "room" + str(room_number)
		print("room name:",room_name)

	#check if room exists
	data['room_name'] = room_name #captures room name
	room_url = DAILY_API + room_name
	headers = {'authorization': 'Bearer %s' % BEARER}
	response = requests.request("GET", room_url, headers=headers).json()

	if 'error' and 'info' in response :
		print(response['info']) #error handling
		
		if response['error'] == 'not-found' : #if room does not exist, create new room
			payload = "{\"properties\":{\"max_participants\":2},\"name\":\"%s\"}" % room_name
			response = requests.request("POST", DAILY_API, data=payload, headers=headers)
			print(response.json())

	return json.dumps(data)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()