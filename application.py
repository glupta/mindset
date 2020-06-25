from flask import Flask, render_template
from flask import request, jsonify, make_response
from datetime import datetime
import json
import mysql.connector
import sys
import boto3
import os
import requests

ENDPOINT = "med-live-db2.c2kufiynjcx0.us-east-2.rds.amazonaws.com"
USR="admin"
PWD= "meditate123"
PORT="3306"
REGION="us-east-2"
DBNAME="medlivedb2"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

@app.route('/api/timedetails')
def timedetails():

	data = {}
	data['time_current'] = datetime.now().isoformat() #captures current time
	data['time_sched'] = datetime(2020,6,25,2,52).isoformat() #captures scheduled time
	return json.dumps(data)

@app.route('/api/requestroom', methods=["POST"])
def requestroom():

	data = {} #data to be returned

	#check for clientID
	req = request.get_json()
	if 'clientID' in req:
		client_id = req['clientID']

	if client_id == None:
		client_id = "dummy"
	print("client ID:",client_id)

	#connect to DB & run cmd
	#gets the credentials from .aws/credentials
	session = boto3.Session(profile_name='default')
	client = boto3.client('rds')
	conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
	cur = conn.cursor(buffered=True)
	print(client_id,": passed DB credentials")

	#check if user is already in active_users table
	cmd = "SELECT * FROM active_users WHERE user_name = %s"
	try:
		cur.execute(cmd,(client_id,))
		print("does user exist1? ","yes" if cur.rowcount > 0 else "no")
		if cur.rowcount > 0 :
			print("error, user already exists")
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
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
		return json.dumps(data)

	#get entry order
	cmd = "SELECT entry_order FROM active_users WHERE user_name = %s"
	try:
		cur.execute(cmd,(client_id,))
		print("does user exist2? ","yes" if cur.rowcount > 0 else "no")
		if cur.rowcount > 0 :
			entry_order = cur.fetchone()[0]
			print("entry order:",entry_order)
		else :
			print("error, user does not exist")
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		return json.dumps(data)

	conn.close() #close DB connection

	# #dummy users
	# if client_id == "User1" or client_id == "User2" :
	# 	room_name = "room1"

	# elif client_id == "User3" or client_id == "User4" :
	# 	room_name = "room2"

	#assigns room based on entry_order
	room_number = (entry_order + 1) // 2
	room_name = "room" + str(room_number)
	print("room name:",room_name)

	#check if room exists
	url = "https://api.daily.co/v1/rooms/"
	room_url = url + room_name
	headers = {'authorization': 'Bearer 05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b'}
	response = requests.request("GET", room_url, headers=headers).json()

	if 'error' and 'info' in response :
		print(response['info']) #error handling
		
		if response['error'] == 'not-found' : #if room does not exist, create new room
			payload = "{\"properties\":{\"max_participants\":2},\"name\":\"%s\"}" % room_name
			response = requests.request("POST", url, data=payload, headers=headers)
			print(response.json())

	data['entry_order'] = entry_order #captures entry order
	data['room_name'] = room_name #captures room name
	return json.dumps(data)

	#get json for all rooms
	# headers = {
	# 	'content-type': "application/json",
	# 	'authorization': "Bearer 05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b"
	# 	}
	# response = requests.request("POST", url, headers=headers)
	#print(response.json())



#@app.route('/api/joinroom', methods=["POST"])
#def joinroom():
	#req = request.get_json()
	#get assigned room ID from DB for user
	#if chat room does not exist
		#create chat room
	#add user to chat room


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()