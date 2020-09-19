from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_mail import Mail, Message
from datetime import datetime, timedelta, timezone
import smtplib, ssl
import json
import requests
import sys
import os
import mysql.connector
import ipaddress
import time
import random

#DATABASE CREDENTIALS
ENDPOINT = "med-live-db2.c2kufiynjcx0.us-east-2.rds.amazonaws.com"
USR = "admin"
PWD = "meditate123"
PORT = "3306"
REGION = "us-east-2"
DBNAME = "medlivedb2"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#DAILY.CO VIDEO CHAT API CREDENTIALS
BEARER = '05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b' #meditate-live
#BEARER = '430bfe053ef86e871e12cd960f51996b429fd032612926becd766becdef03963' #meditate
DAILY_API = "https://api.daily.co/v1/rooms/"

#EMAIL CREDENTIALS
#GMAIL: meditateliveorg@gmail.com
EMAIL_USR = "meditateliveorg@gmail.com"
EMAIL_PWD = "wilson@123"
EMAIL_SVR = "smtp.gmail.com"
EMAIL_PORT = 465

#AWS SES: noreply@meditatelive.org
#EMAIL_USR = "AKIAXFVDPD5FIFSCXQNZ"
#EMAIL_PWD = "BHcdWLEuyvQaSi86s1ACU7EVYF2kUmi/CSW7ffLEVQId"
#EMAIL_SVR = "email-smtp.us-east-2.amazonaws.com"
#EMAIL_PORT = 465

SCHED_TIMES = [0,12]

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'meditateliveorg@gmail.com',
	MAIL_PASSWORD = 'wilson@123'
	)
mail = Mail(app)

@app.before_request #redirects http to https
def before_request():

	if "localhost" not in request.url and request.url.startswith('http://'):
		#print("URL:",request.url)
		url = request.url.replace('http://', 'https://', 1)
		code = 301
		return redirect(url, code=code)
	else:
	 	print('URL local:',request.url)
	 	return


@app.route('/api/timedata') #returns time data
def time_data():
	
	data = {} #json response
	time_current = datetime.utcnow()
	time_sched = time_current
	id_query = request.args.get('id')
	sched_query = request.args.get('sched')

	#determine sched time from id
	if id_query :
		session_type = id_query[0]
		session_hash = id_query[1:]

		#connect to DB
		try:
			conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
			cur = conn.cursor(buffered=True)
			print("session list: passed DB credentials")
		except:
			print("session list: did not pass DB credentials")
			data['error'] = "unable to connect with DB"
			return json.dumps(data)

		#search database for hash
		result = []
		try:
			cmd = "SELECT session_id, user_id, user_email, sched_time, partner_id, partner_email FROM sessions WHERE session_hash = %s;"
			cur.execute(cmd,(session_hash,))
			if cur.rowcount > 0 :
				result = cur.fetchone()
				print("res:",result)
			else :  #if not found, kick out to error alert
				print("did not find hash")
				data['error'] = 'session confirm failed: id not found'
				return json.dumps(data)
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "failed to connect to DB"
			return json.dumps(data)
		time_sched = result[3]

	#determine sched time from get request
	elif sched_query :

		if '-' in sched_query :
			try :
			  	sched_parse = sched_query.split("-")
			  	print(sched_parse)
			  	sched_month = int(sched_parse[0])
			  	sched_day = int(sched_parse[1])
			  	sched_year = 2000 + int(sched_parse[2])
			  	sched_hour = int(sched_parse[3])
			  	sched_min = int(sched_parse[4])
			except :
				print("could not parse sched time request")
				data['error'] = "could not parse sched request"
				return json.dumps(data)

		#by default, set sched as next sched time in list
		else :
			print("using default sched time")
			sched_time_bool = False
			sched_min = 0
			for t in SCHED_TIMES: #decides next session
				if time_current.hour < t:
					print("next sched time:",t)
					sched_year = time_current.year
					sched_month = time_current.month
					sched_day = time_current.day
					sched_hour = t
					sched_time_bool = True
					break
			if not sched_time_bool: #set sched as next day first time
				print("sched time next day")
				#sched_day = time_current.day + 1
				next_day = time_current + timedelta(1)
				sched_year = next_day.year
				sched_month = next_day.month
				sched_day = next_day.day
				sched_hour = SCHED_TIMES[0]

		time_sched = datetime(sched_year,sched_month,sched_day,sched_hour,sched_min)
	
	time_diff = (time_sched-time_current).total_seconds() #captures time difference
	data['time_current'] = time_current.replace(tzinfo=timezone.utc).isoformat() #captures current time
	data['time_sched'] = time_sched.replace(tzinfo=timezone.utc).isoformat()
	data['time_diff'] = time_diff

	return json.dumps(data)

@app.route('/api/sessionlist') #return list of all sessions
def session_list():

	data = {} #data to be returned
	output = [] #table to be in output

	date_query = request.args.get('date')
	print(date_query)
	sched_obj = datetime.strptime(date_query,'%Y-%m-%dT%H:%M:%S.%fZ')
	sched_date = sched_obj.strftime('%Y-%m-%d')

	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("session list: passed DB credentials")
	except:
		print("session list: did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#get all sessions
	try:
		time_current = datetime.utcnow() #.strftime('%Y-%m-%d %H:%M:%S')
		cmd = "SELECT session_id, user_id, user_email, sched_time, session_hash, duration FROM sessions WHERE sched_date = %s AND sched_time > %s AND user_confirm IS NOT NULL AND partner_confirm IS NULL AND private_bool = 0 ORDER BY sched_time, duration ASC;"
		cur.execute(cmd,(sched_date,time_current,))
		result = cur.fetchall()
		print("res:",result)
		print("Cur:",time_current)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "failed to connect to DB on query 1"
		return json.dumps(data)

	#clean data from sessions list
	date_indices = [3] #columns with dates
	for row in result :
		output_row = []
		for i in range(0,6) :
			if i in date_indices :
				output_sched = row[i].replace(tzinfo=timezone.utc).isoformat()
				output_row.append(output_sched)
				#print("row:",output_sched)
			else :
				output_row.append(row[i])
		output.append(output_row)

	#print(output)
	return json.dumps(output)

@app.route('/api/schednew', methods=["POST"]) #add to session table
def sched_new():

	data = {} #data to be returned
	req = request.get_json()
	print(req)
	data_params = ['user_id','user_email','sched_time','sched_time_local','session_hash','invite_email','duration','private_bool']
	for item in data_params :
		if item not in req :
			print(item)
			data['error'] = "sched session data missing"
			return json.dumps(data)

	user_id = str(req['user_id'])
	user_email = str(req['user_email'])
	invite_email = str(req['invite_email'])
	duration = int(req['duration'])
	private_bool = int(req['private_bool'])
	#sched_time = str(req['sched_time']) 
	sched_obj = datetime.strptime(req['sched_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
	sched_date = sched_obj.strftime('%Y-%m-%d')
	sched_time = sched_obj.strftime('%Y-%m-%d %H:%M:%S')
	#sched_time_UTC = sched_obj.replace(tzinfo=timezone('UTC'))
	sched_time_local = str(req['sched_time_local'])

	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("sched: passed DB credentials")
	except:
		print("sched: did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	session_hash =  hex(random.getrandbits(128))[2:10]
	print(session_hash)
	
	#add to users table if new email ID
	try:
		cmd = "SELECT * FROM users WHERE user_email = %s"
		cur.execute(cmd,(user_email,))
		print(user_email, ": does user exist (sched)? ","yes" if cur.rowcount > 0 else "no")
		if cur.rowcount == 0 :
			cmd = "INSERT INTO users(user_id,user_email) VALUES (%s,%s)"
			cur.execute(cmd,(user_id,user_email))
			conn.commit()
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "failed to add to users table"
		return json.dumps(data)


	#check DB if same request added to sessions table
	if private_bool == 0 :
		try: 
			cmd = "SELECT * FROM sessions WHERE sched_time = %s AND duration = %s AND private_bool = 0 AND user_confirm IS NOT NULL"
			cur.execute(cmd,(sched_time,duration))
			if cur.rowcount > 0 :
				data['error'] = "this session is publicly scheduled already"
				return json.dumps(data)
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "failed to connect to DB"
			return json.dumps(data)

	#insert into sessions table
	try:
		cmd = "INSERT INTO sessions(user_id,user_email,sched_date,sched_time,session_hash,duration,private_bool,invite_email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
		cur.execute(cmd,(user_id,user_email,sched_date,sched_time,session_hash,duration,private_bool,invite_email))
		conn.commit()
		print("inserted in sessions table")
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "failed to connect to sessions table"
		return json.dumps(data)

	#send confirmation emails
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000/schedule'
	elif "test" in request.url :
		confirm_url = 'test.meditatelive.org/schedule'
	else :
		confirm_url = 'meditatelive.org/schedule'

	message = """From: Meditate Live <meditateliveorg@gmail.com>
To: %s <%s>
Subject: Please confirm your meditation session request

Thank you for creating the following session request:

Time: %s

Duration: %s min.

Please click here to confirm the session:
%s?id=u%s
""" % (user_id,user_email,sched_time_local,duration,confirm_url,session_hash)

	# Create a secure SSL context
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(EMAIL_SVR,EMAIL_PORT, context=context) as server :
		server.login(EMAIL_USR,EMAIL_PWD)
		server.sendmail(EMAIL_USR,[user_email],message)

	print(message)
	data['success'] = True
	return json.dumps(data)

@app.route('/api/schedpublic') #add to session table
def sched_public():

	data = {} #data to be returned
	session_hash = str(request.args.get('hash'))
	user_email = str(request.args.get('email'))
	user_id = str(request.args.get('id'))
	if not session_hash or not user_email or not user_id :
		print("query data missing")
		data['error'] = 'query data missing'
		return json.dumps(data)

	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("sched: passed DB credentials")
	except:
		print("sched: did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#add to users table if new email ID
	try:
		cmd = "SELECT * FROM users WHERE user_email = %s"
		cur.execute(cmd,(user_email,))
		print(user_email, ": does user exist (sched)? ","yes" if cur.rowcount > 0 else "no")
		if cur.rowcount == 0 :
			cmd = "INSERT INTO users(user_id,user_email) VALUES (%s,%s)"
			cur.execute(cmd,(user_id,user_email))
			conn.commit()
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "failed to add to users table"
		return json.dumps(data)

		
	try: #check if partner_confirm null for session_hash
		cmd = "SELECT user_email FROM sessions WHERE session_hash = %s AND partner_confirm IS NULL"
		cur.execute(cmd,(session_hash,))
		result = cur.fetchone()
		print("user email:",result[0])
		if cur.rowcount == 0 :
			data['error'] = "session already claimed"
			return json.dumps(data)
		elif result[0] == user_email :
			data['error'] = "both users have the same email"
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "failed to connect to DB"
		return json.dumps(data)

	try : #update partner id and email for session in DB
		cmd = "UPDATE sessions SET partner_id = %s, partner_email = %s WHERE session_hash = %s"
		cur.execute(cmd,(user_id,user_email,session_hash))
		conn.commit()
		print("inserted in sessions table")
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "failed to connect to sessions table"
		return json.dumps(data)

	try: #get sched time and duration details
		cmd = "SELECT sched_time,duration FROM sessions WHERE session_hash = %s"
		cur.execute(cmd,(session_hash,))
		if cur.rowcount > 0 :
			result = cur.fetchone()
			data['sched_time'] = result[0].replace(tzinfo=timezone.utc).isoformat()
			data['duration'] = result[1]
		else :
			data['error'] = "session hash not found"
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "failed to connect to DB"
		return json.dumps(data)


	#send confirmation emails
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000/schedule'
	elif "test" in request.url :
		confirm_url = 'test.meditatelive.org/schedule'
	else :
		confirm_url = 'meditatelive.org/schedule'

	message = """From: Meditate Live <meditateliveorg@gmail.com>
To: %s <%s>
Subject: Please confirm your meditation session

Thank you for claiming a public meditation session at the following time:

Time: %s

Duration: %s min.

Please click here to confirm the session:
%s?id=p%s
""" % (user_id,user_email,result[0],result[1],confirm_url,session_hash)

	# Create a secure SSL context
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(EMAIL_SVR,EMAIL_PORT, context=context) as server:
		server.login(EMAIL_USR,EMAIL_PWD)
		server.sendmail(EMAIL_USR,[user_email],message)

	print(message)
	data['success'] = True
	return json.dumps(data)

@app.route('/api/schedemail') #confirms email URL
def sched_email():

	data = {}
	confirm_query = request.args.get('id')
	tz_query = request.args.get('tz')
	if not confirm_query or not tz_query:
		print("query data missing")
		data['error'] = 'id or tz data missing'
		return json.dumps(data)

	session_type = confirm_query[0] #user type is first letter of URL
	session_hash = confirm_query[1:]
	print("sesh hash:",session_hash)

	if session_type != 'u' and session_type != 'p' :
		print("did not find user type")
		data['error'] = 'user type data missing'
		return json.dumps(data)

	#search database for hash
	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("sched email: passed DB credentials")
	except:
		print("sched email: did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#search database for hash
	result = []
	try:
		cmd = "SELECT session_id, user_id, user_email, sched_time, partner_id, partner_email, invite_email, user_confirm, partner_confirm, duration FROM sessions WHERE session_hash = %s;"
		cur.execute(cmd,(session_hash,))
		if cur.rowcount > 0 :
			result = cur.fetchone()
			print("res:",result)
		else :  #if not found, kick out to error alert
			print("did not find hash")
			data['error'] = 'session confirm failed: id not found'
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "failed to connect to DB"
		return json.dumps(data)

	#check result to see if already confirmed
	if session_type == 'u' :
		confirm_time = result[7]
	elif session_type == 'p' :
		confirm_time = result[8]
	print(confirm_time)
	if confirm_time != None :
		data['error'] = 'session is already confirmed'
		return json.dumps(data)

	#update confirm timestamp for user or partner
	time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	try:
		if session_type == 'u' :
			cmd = "UPDATE sessions SET user_confirm = %s WHERE session_hash = %s"
			print("updated user confirm timestamp")
		elif session_type == 'p' :
			cmd = "UPDATE sessions SET partner_confirm = %s WHERE session_hash = %s"
			print("updated partner confirm timestamp")
		cur.execute(cmd,(time_current,session_hash))
		conn.commit()
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "failed to connect to sessions table"
		return json.dumps(data)

	#send confirmation email with link to waiting room
	user_id = result[1]
	user_email = result[2]
	sched_time = result[3]
	partner_id = result[4]
	partner_email = result[5] 
	invite_email = result[6]
	duration = result[9]

	tz_min = int(tz_query)
	sched_time_local = sched_time - timedelta(hours=0, minutes=tz_min)

	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000/schedule'
	elif "test" in request.url :
		confirm_url = 'test.meditatelive.org/schedule'
	else :
		confirm_url = 'meditatelive.org/schedule'

	# Create a secure SSL context
	context = ssl.create_default_context()

	#email creator notification of confirmation
	if session_type == 'u' :
		message = """From: Meditate Live <meditateliveorg@gmail.com>
To: %s <%s>
Subject: Your session request is confirmed

Thank you for scheduling the following meditation session:

Time: %s

Duration: %s

We will let you know when someone claims your session request.
""" % (user_id,user_email,sched_time_local,duration)

		if invite_email:
			message = """From: Meditate Live <meditateliveorg@gmail.com>
To: %s
Subject: Your friend invited you to a meditation session

Your friend (%s) invited you for the following session:

Time: %s

Duration: %s min.

Please click here to confirm the session:
%s?id=p%s
""" % (invite_email,user_email,sched_time_local,duration,confirm_url,session_hash)
			print(message)
			with smtplib.SMTP_SSL(EMAIL_SVR,EMAIL_PORT,context=context) as server:
				server.login(EMAIL_USR,EMAIL_PWD)
				server.sendmail(EMAIL_USR,[invite_email],message)

	#email waiting room links to user and partner
	elif session_type == 'p' :

		#email user waiting room link
		message = """From: Meditate Live <meditateliveorg@gmail.com>
To: %s <%s>
Subject: Your public session was claimed

The following session request was accepted by %s:

Time: %s

Duration: %s min.

Please click here to join the session at the scheduled time:
%s?id=wu%s
""" % (user_id,user_email,partner_email,sched_time_local,duration,confirm_url,session_hash)
		print(message)
		with smtplib.SMTP_SSL(EMAIL_SVR,EMAIL_PORT,context=context) as server:
			server.login(EMAIL_USR,EMAIL_PWD)
			server.sendmail(EMAIL_USR,[user_email],message)

		#email partner waiting room link
		message = """From: Meditate Live <meditateliveorg@gmail.com>
To: %s <%s>
Subject: Your session is confirmed

Thank you for claiming the following meditation session:

Time: %s

Duration: %s min.

We have notifed %s as well.

Please click here to join the session at the scheduled time:
%s?id=wp%s
""" % (partner_id,partner_email,sched_time_local,duration,user_email,confirm_url,session_hash)
		print(message)
		with smtplib.SMTP_SSL(EMAIL_SVR,EMAIL_PORT,context=context) as server:
			server.login(EMAIL_USR,EMAIL_PWD)
			server.sendmail(EMAIL_USR,[partner_email],message)

 #    //set up reminder with link for waiting room 5 min before session
 #    //set up text reminder

	data['success'] = True
	return json.dumps(data)

#
@app.route('/api/joinroom') #joins video chat room based on hash
def join_room():

	data = {}
	join_query = request.args.get('id')
	if not join_query:
		print("query data missing")
		data['error'] = 'id data missing'
		return json.dumps(data)

	session_type = join_query[1] #user type is first letter of URL
	session_hash = join_query[2:]
	print("sesh hash:",session_hash)

	if session_type != 'u' and session_type != 'p' :
		print("did not find user type")
		data['error'] = 'user type data missing'
		return json.dumps(data)

	#search database for hash
	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("sched email: passed DB credentials")
	except:
		print("sched email: did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#search database for hash
	result = []
	try:
		cmd = "SELECT sched_time, duration FROM sessions WHERE session_hash = %s;"
		cur.execute(cmd,(session_hash,))
		if cur.rowcount > 0 :
			result = cur.fetchone()
			print("res:",result)
		else :  #if not found, kick out to error alert
			print("did not find hash")
			data['error'] = 'session confirm failed: id not found'
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "failed to connect to DB"
		return json.dumps(data)

	time_current = datetime.utcnow()
	time_diff = (result[0] - time_current).total_seconds()
	print("current:",time_current,"sched:",result[0],"diff:",time_diff)
	data['time_current'] = datetime.utcnow().isoformat()
	data['time_sched'] = result[0].isoformat()
	data['time_diff'] = time_diff
	data['duration'] = int(result[1])
	print("duration:",data['duration'])
	return json.dumps(data)
	

@app.route('/api/flushactiveusersdb') #delete all active users in DB
def flush_active_users():

	data = {} #data to be returned

	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("flush: passed DB credentials")
	except:
		print("flush: did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#delete all entries from active users DB
	try:
		cur.execute("DELETE FROM active;")
		cur.execute("ALTER TABLE active AUTO_INCREMENT = 1;")
		#cur.execute("DELETE FROM users;") #temporary until user table is fleshed out
		conn.commit()
		print("flushed active users")
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "failed to connect to DB on flush"
		return json.dumps(data)

	data['flush'] = True
	return json.dumps(data)

@app.route('/api/roomtoken', methods=["POST"]) #generate room token
def room_token():

	data = {} #data to be returned

	#check for room name
	req = request.get_json()
	if 'room_name' not in req :
		data['error'] = "room name missing"
		return json.dumps(data)

	#generate token
	url = "https://api.daily.co/v1/meeting-tokens"
	payload = "{\"properties\":{\"room_name\":\"%s\"}}" % req['room_name']
	headers = {'authorization': 'Bearer %s' % BEARER}
	response = requests.request("POST", url, data=payload, headers=headers).json()

	if 'token' in response :
		print(response['token'])
		data['token'] = response['token']
	else:
		data['error'] = "generating token failed"
		return json.dumps(data)

	return json.dumps(data)

@app.route('/api/requestroom') #returns assigned room data for active
def request_room():

	client_id = str(request.args.get('clientID'))

	if client_id == None:
		print("client_id missing")
		data['error'] = "client_id missing"
		return json.dumps(data)

	print("client ID:",client_id)

	data = {} #data to be returned
	data['user_name'] = client_id

	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print(client_id,": passed DB credentials")
	except:
		print(client_id,": did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)


	#check if user is already in active table
	cmd = "SELECT * FROM active WHERE user_id = %s"
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

	#check if user is already in users table
	new_user = False
	cmd = "SELECT * FROM users WHERE user_id = %s"
	try:
		cur.execute(cmd,(client_id,))
		print(client_id, ": new user in users? ","yes" if cur.rowcount == 0 else "no")
		if cur.rowcount == 0 :
			new_user = True
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "failed to connect to DB on query 1"
		return json.dumps(data)

	#insert new user into users table
	if new_user :
		cmd = "INSERT INTO users(user_id) VALUES (%s)" #add to active_users table
		try:
			cur.execute(cmd,(client_id,))
			conn.commit()
			print("inserted in user table")
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			conn.rollback()
			data['error'] = "failed to connect to user table"
			return json.dumps(data)

	#insert user into active table
	cmd = "INSERT INTO active(user_id) VALUES (%s)" #add to active_users table
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
	cmd = "SELECT entry_order FROM active WHERE user_id = %s"
	try:
		cur.execute(cmd,(client_id,))
		print("does user exist2? ","yes" if cur.rowcount > 0 else "no")
		if cur.rowcount > 0 :
			entry_order = cur.fetchone()[0]
			data['entry_order'] = entry_order #captures entry order
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

	#check if room exists
	data['room_name'] = room_name #captures room name
	room_url = DAILY_API + room_name
	headers = {'authorization': 'Bearer %s' % BEARER}
	response = requests.request("GET", room_url, headers=headers).json()

	if 'error' and 'info' in response :
		print(response['info']) #error handling
		
		if response['error'] == 'not-found' : #if room does not exist, create new room
			payload = "{\"properties\":{\"enable_screenshare\":false,\"max_participants\":2,\"start_audio_off\":false,\"start_video_off\":false},\"name\":\"%s\",\"privacy\":\"private\"}" % room_name
			response = requests.request("POST", DAILY_API, data=payload, headers=headers)
			print(response.json())

	return json.dumps(data)

@app.route('/api/createroom') #create room if does not exist
def create_room():

	data = {} #data to be returned

	#check for room name
	room_name = request.args.get('room')
	if not room_name:
		data['error'] = "room name missing"
		return json.dumps(data)

	#check if room exists
	data['room_name'] = room_name #captures room name
	room_url = DAILY_API + room_name
	headers = {'authorization': 'Bearer %s' % BEARER}
	response = requests.request("GET", room_url, headers=headers).json()

	if 'error' and 'info' in response :
		print(response['info']) #error handling
		
		if response['error'] == 'not-found' : #if room does not exist, create new room
			payload = "{\"properties\":{\"enable_screenshare\":false,\"max_participants\":2,\"start_audio_off\":false,\"start_video_off\":false},\"name\":\"%s\",\"privacy\":\"private\"}" % room_name
			response = requests.request("POST", DAILY_API, data=payload, headers=headers)
			print("created",response.json())

	return json.dumps(data)

@app.route('/api/checkroom') #finds video chat room based on client ID
def check_room():

	data = {} #data to be returned

	#check for clientID
	client_id = request.args.get('clientID')
	if client_id == None:
		print("client_id missing")
		data['error'] = "client_id missing"
		return json.dumps(data)

	try: #connect to DB
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print(client_id,": passed DB credentials")
	except:
		print(client_id,": did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)


	#check if user is already in active_users table
	cmd = "SELECT * FROM active WHERE user_id = %s"
	try:
		cur.execute(cmd,(client_id,))
		print(client_id, ": does user exist? ","yes" if cur.rowcount > 0 else "no")
		if cur.rowcount > 0 :
			record = cur.fetchone()
			print("client ID:",record[1],", order:",record[0])
			
			room_number = (record[0] + 1) // 2 #assigns room based on entry_order
			room_name = "room" + str(room_number)
			print("room name:",room_name)
			data['room_name'] = room_name
		# else :
		# 	data['room_name'] = client_id #otherwise room name is client ID
	except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "failed to connect to DB on query"
			return json.dumps(data)

	conn.close() #close DB connection
	return json.dumps(data)

@app.route('/api/checkstartrandom') #checks if both in room pressed START
def check_start_random():

	data = {} #data to be returned

	#check for clientID
	client_id = request.args.get('clientID')
	if client_id == None:
		print("client_id missing")
		data['error'] = "client_id missing"
		return json.dumps(data)

	try: #connect to DB
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print(client_id,": passed DB credentials")
	except:
		print(client_id,": did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#update start_ready to true in DB
	if request.args.get('start') == '1':
		cmd = "UPDATE active SET start_ready = 1 WHERE user_id = %s"
		try:
			cur.execute(cmd,(client_id,))
			conn.commit()
			print("updated user start ready")
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			conn.rollback()
			data['error'] = "failed to update user start ready"
			return json.dumps(data)

	#get user entry order
	if request.args.get('order') == None:
		cmd = "SELECT * FROM active WHERE user_id = %s"
		try:
			cur.execute(cmd,(client_id,))
			print(client_id, ": does user exist? ","yes" if cur.rowcount > 0 else "no")
			if cur.rowcount > 0 :
				record = cur.fetchone()
				print("client ID:",record[1],", order:",record[0])			
				entry_order = int(record[0])
				data['entry_order'] = entry_order
		except Exception as e:
				print("Database connection failed due to {}".format(e))
				data['error'] = "failed to check active users"
				return json.dumps(data)
	else:
		entry_order = int(request.args.get('order'))

	#figure out partner entry order
	if entry_order % 2 == 0:
		partner_order = entry_order - 1
	else:
		partner_order = entry_order + 1

	#check if partner is ready
	cmd = "SELECT * FROM active WHERE entry_order = %s"
	try:
		cur.execute(cmd,(partner_order,))
		print(client_id, ": does partner exist? ","yes" if cur.rowcount > 0 else "no")
		if cur.rowcount > 0 :
			record = cur.fetchone()
			print("partner ID:",record[1],", order:",record[0])			
			data['partner_start'] = record[3]
	except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "failed to check active users"
			return json.dumps(data)

	conn.close() #close DB connection
	return json.dumps(data)

@app.route('/api/checkstartcal') #checks session hash if both in room pressed START
def check_start_cal():

	data = {}
	confirm_query = request.args.get('id')
	if not confirm_query :
		print("did not find confirm query")
		data['error'] = 'id data missing'
		return json.dumps(data)

	session_type = confirm_query[0] #user type is first letter of URL
	session_hash = confirm_query[1:]
	print("sesh hash:",session_hash)

	if session_type != 'u' and session_type != 'p' :
 		print("did not find user type")
 		data['error'] = 'user type data missing'
 		return json.dumps(data)

	try: #connect to DB
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("passed DB credentials")
	except:
		print("did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#update start_ready to true in DB
	if request.args.get('start') == '1':
		time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		if session_type == 'u' :
			cmd = "UPDATE sessions SET user_start = %s WHERE session_hash = %s"
		elif session_type == 'p' :
 			cmd = "UPDATE sessions SET partner_start = %s WHERE session_hash = %s"
		try:
			cur.execute(cmd,(time_current,session_hash))
			conn.commit()
			print("updated user start ready")
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			conn.rollback()
			data['error'] = "failed to update user start ready"
			return json.dumps(data)

	#get session to check start timestamps
	cmd = "SELECT user_start, partner_start FROM sessions WHERE session_hash = %s"
	try:
		cur.execute(cmd,(session_hash,))
		record = cur.fetchone()
		print("user:",record[0],"partner:",record[1])
		if record[0] is None or record[1] is None :
			data['ready'] = 'no'
		else :
			data['user_start'] = record[0].replace(tzinfo=timezone.utc).isoformat()
			data['partner_start'] = record[1].replace(tzinfo=timezone.utc).isoformat()
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "failed to check active users"
		return json.dumps(data)

	conn.close() #close DB connection
	return json.dumps(data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()