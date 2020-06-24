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
	data['time_sched'] = datetime(2020,6,25,0,15).isoformat() #captures scheduled time
	return json.dumps(data)

@app.route('/api/requestroom', methods=["POST"])
def requestroom():

	#check for clientID
	req = request.get_json()
	if 'clientID' not in req:
		print('missing client ID')

	#dummy users
	room_name = ""
	if req['clientID'] == "User1" or req['clientID'] == "User2" :
		room_name = "room1"

	elif req['clientID'] == "User3" or req['clientID'] == "User4" :
		room_name = "room2"

	#update user in DB with current session ID & time stamp
	#count active users with current session ID & timestamp <= user's timestamp
	#assign chat room = count // 2
	#update DB with assigned room

	#gets the credentials from .aws/credentials
	# session = boto3.Session(profile_name='default')
	# client = boto3.client('rds')
	# #token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)

	# try:
	# 	conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
	# 	cur = conn.cursor()
	# 	cur.execute("""SELECT now()""")
	# 	query_results = cur.fetchall()
	# 	print("success!",query_results)
	# except Exception as e:
	# 	print("Database connection failed due to {}".format(e))


	#check if room exists
	url = "https://api.daily.co/v1/rooms/" #+ room_name
	room_url = url + room_name
	headers = {'authorization': 'Bearer 05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b'}
	response = requests.request("GET", room_url, headers=headers).json()

	
	if 'error' and 'info' in response :
		print(response['info']) #error handling
		
		if response['error'] == 'not-found' : #if room does not exist, create new room
			payload = "{\"properties\":{\"max_participants\":2},\"name\":\"%s\"}" % room_name
			response = requests.request("POST", url, data=payload, headers=headers)
			print(response.json())

	data = {}
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