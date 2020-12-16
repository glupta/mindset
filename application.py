from flask import Flask, render_template, request, jsonify, make_response, redirect, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
from flask_mail import Mail, Message
from datetime import datetime, timedelta, timezone
from decouple import config
from flask_api import status
import smtplib, ssl
import json
import requests
import sys
import os
import mysql.connector
import ipaddress
import time
import random
import boto3
import re

#DATABASE CREDENTIALS
ENDPOINT = config('AWS_RDB_ENDPOINT')
USR = config('AWS_RDB_USR')
PWD = config('AWS_RDB_PWD')
DBNAME = config('AWS_RDB_NAME')
PORT = "3306"
REGION = "us-east-2"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'


#EMAIL CREDENTIALS
#GMAIL: meditateliveorg@gmail.com
EMAIL_USR = config('MDS_EMAIL_USR')
EMAIL_PWD = config('MDS_EMAIL_PWD')
EMAIL_SVR = "smtp.gmail.com"
EMAIL_PORT = 465

#AWS credentials
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

#Twilio credentials
TWI_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWI_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

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

@app.route("/api/sendreminder")
def send_reminder():

	data = {} #json response
	sms_message = str(request.args.get('m'))
	if not sms_message :
		data['error'] = "num error"
		print(data['error'])
		return json.dumps(data)


	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("send reminder: passed DB credentials")
	except:
		print("send reminder: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for phone number
	try :
		cmd = "SELECT full_name, phone_num FROM users2 WHERE partner_num IS NOT NULL;"
		#cmd = "SELECT full_name, phone_num FROM users2 WHERE send_reminder = '1';"
		cur.execute(cmd)
		if cur.rowcount == 0 :
			data['error'] = "Empty list."
			print(data['error'])
			return json.dumps(data)
		else :
			results = cur.fetchall()
			print(results)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#url in text
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000'
	elif "://t" in request.url :
		confirm_url = 'http://t.mindset.ooo'
	else :
		confirm_url = 'http://mindset.ooo'

	#sms_message += confirm_url
	#sms_message = "MINDSET:\nWe hope you've had a great start to the week " + row[0] + ", keep up the momentum! Remember to complete your habit: http://mindset.ooo"

	gsm_regex = "^[A-Za-z0-9 \\r\\n@£$¥èéùìòÇØøÅå\u0394_\u03A6\u0393\u039B\u03A9\u03A0\u03A8\u03A3\u0398\u039EÆæßÉ!\"#$%&'()*+,\\-./:;<=>?¡ÄÖÑÜ§¿äöñüà^{}\\\\\\[~\\]|\u20AC]*$"
	# result = re.match(gsm_regex, sms_message)
	# if result:
	# 	print("Search successful.",len(sms_message))
	# else:
	# 	print("Search unsuccessful.")

	for row in results:
		# sms_message = "MINDSET:\nWe hope you've had a great start to the week " + row[0] + ", keep up the momentum! Remember to complete your habit: http://mindset.ooo"
		# result = re.match(gsm_regex, sms_message)
		# if result:
		# 	print("Search successful.",len(sms_message))
		# else:
		# 	print("Search unsuccessful.")

		client = Client(TWI_ACCOUNT_SID, TWI_AUTH_TOKEN)
		message = client.messages.create(
			body=sms_message,
			from_='+13158205380',
			to="+1" + row[1]
		)

	#add to sms_messages table
	try :
		time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		sms_count = len(results)
		cmd = "INSERT INTO sms_reminders(sms_time,sms_count,sms_message) VALUES (%s,%s,%s)"
		cur.execute(cmd,(time_current,sms_count,sms_message,))
		conn.commit()
		data['success'] = True
	except Exception as e :
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "Oops! Something went wrong. The user was not added to the database."
		return data['error'],status.HTTP_500_INTERNAL_SERVER_ERROR

	return sms_message

@app.route("/api/incomingtwilio", methods=['GET', 'POST'])
def sms_reply():

	# Get the message the user sent our Twilio number
	sms_sender = request.values.get('From', None)[2:]
	sms_body = request.values.get('Body', None)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("incoming sms: passed DB credentials")
	except:
		print("incoming sms: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return data['error'],status.HTTP_500_INTERNAL_SERVER_ERROR


	#search database for phone number
	try :
		cmd = "SELECT full_name, partner_num FROM users2 WHERE phone_num = %s;"
		cur.execute(cmd,(sms_sender,))
		if cur.rowcount == 0 :
			print("The phone number was not found.")
			data['error'] = 'Oops! Something went wrong. The phone number was not found.'
			return data['error'],status.HTTP_500_INTERNAL_SERVER_ERROR
		else :
			result = cur.fetchone()
			user_name = result[0]
			partner_num = result[1]
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return data['error'],status.HTTP_500_INTERNAL_SERVER_ERROR

	#verification link
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000'
	elif "://t." in request.url :
		confirm_url = 'http://t.mindset.ooo'
	else :
		confirm_url = 'http://mindset.ooo'

	#sms_message = "MINDSET:\nHey " + full_name + "! Please click here to verify your number: " + confirm_url
	sms_message = user_name + ":\n" + sms_body
	gsm_regex = "^[A-Za-z0-9 \\r\\n@£$¥èéùìòÇØøÅå\u0394_\u03A6\u0393\u039B\u03A9\u03A0\u03A8\u03A3\u0398\u039EÆæßÉ!\"#$%&'()*+,\\-./:;<=>?¡ÄÖÑÜ§¿äöñüà^{}\\\\\\[~\\]|\u20AC]*$"
	result = re.match(gsm_regex, sms_message)
	if result:
		print("Search successful.")
	else:
		print("Search unsuccessful.")

	client = Client(TWI_ACCOUNT_SID, TWI_AUTH_TOKEN)
	message = client.messages.create(
		body=sms_message,
		from_='+13158205380',
		to="+1" + partner_num
	)

	#add to sms_messages table
	try :
		cmd = "INSERT INTO sms_messages(incoming_num,outgoing_num,sms_message) VALUES (%s,%s,%s)"
		cur.execute(cmd,(sms_sender,partner_num,sms_body,))
		conn.commit()
		data['success'] = True
	except Exception as e :
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "Oops! Something went wrong. The user was not added to the database."
		return data['error'],status.HTTP_500_INTERNAL_SERVER_ERROR

	#response = MessagingResponse()
	#return Response(status=200)
	#return status.HTTP_200_OK
	return ('Thank you!', 200)

@app.route('/api/checkhash') #check if hash is in DB, return name & phone
def check_hash():

	data = {}
	hash_query = str(request.args.get('h'))
	date_query = request.args.get('d')
	# tz_query = request.args.get('tz')
	# if not hash_query or date_query or not tz_query :
	# 	data['error'] = "data missing"
	# 	return json.dumps(data)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("check hash: passed DB credentials")
	except:
		print("check hash: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for hash
	try :
		cmd = "SELECT * FROM users2 WHERE session_hash = %s;"
		cur.execute(cmd,(hash_query,))
		if cur.rowcount == 0 :
			print("The session hash was not found.")
			data['error'] = 'Oops! Something went wrong. The session hash was not found.'
			return json.dumps(data)
		else :
			result = cur.fetchone()
			data['phone_num'] = result[0]
			data['full_name'] = result[1]
			data['habit_name'] = result[5]
			data['partner_hash'] = result[6]
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)


	#if d query provided, then also get habit data
	if date_query :
		sched_obj = datetime.strptime(date_query,'%Y-%m-%dT%H:%M:%S.%fZ')
		sched_obj = sched_obj.replace(hour=0, minute=0, second=0, microsecond=0)
		# tz_min = int(tz_query)
		# sched_time_local = sched_obj - timedelta(hours=0, minutes=tz_min)
		# print("offset:",tz_min,"max:",sched_time_max,"min:",sched_time_min)
		habit_name = data['habit_name']
		try :
			cmd = "SELECT * FROM habit_data WHERE habit_id = %s AND user_hash = %s AND date_actual = %s;"
			cur.execute(cmd,(habit_name,hash_query,sched_obj,))
			if cur.rowcount == 0 :
				data['count']= 0
			else :
				data['count']= 1
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "Oops! Something went wrong. The database connection failed."
			return json.dumps(data)

	return json.dumps(data)

@app.route('/api/weekcount') #check if hash is in DB, return weekly habit count
def week_count():

	data = {}
	hash_query = str(request.args.get('h'))
	date_query = request.args.get('d')
	# tz_query = request.args.get('tz')
	# if not hash_query or date_query or not tz_query :
	# 	data['error'] = "data missing"
	# 	return json.dumps(data)

	sched_obj = datetime.strptime(date_query,'%Y-%m-%dT%H:%M:%S.%fZ')
	sched_obj = sched_obj.replace(hour=0, minute=0, second=0, microsecond=0)
	week_day = sched_obj.weekday()
	if week_day < 6:
		week_day += 1
		week_start = sched_obj - timedelta(days=week_day)
	else:
		week_start = sched_obj
	print(hash_query,"ws:",week_start)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("check hash: passed DB credentials")
	except:
		print("check hash: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#get count of weekly habit count
	try :
		cmd = "SELECT * FROM habit_data WHERE user_hash = %s AND date_actual >= %s;"
		cur.execute(cmd,(hash_query,week_start,))
		data['week_count'] = len(cur.fetchall())
		print("wc:",data['week_count'])
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	return json.dumps(data)

@app.route('/api/completehabit') #update habit data table
def complete_habit():

	data = {}
	hash_query = str(request.args.get('h'))
	date_query = request.args.get('d')
	if not hash_query or not date_query :
		data['error'] = "data missing"
		return json.dumps(data)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("complete habit: passed DB credentials")
	except:
		print("complete habit: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for hash
	try :
		cmd = "SELECT phone_num,full_name,habit_id,partner_num FROM users2 WHERE session_hash = %s;"
		cur.execute(cmd,(hash_query,))
		if cur.rowcount == 0 :
			print("The session hash was not found.")
			data['error'] = 'Oops! Something went wrong. The session hash was not found.'
			return json.dumps(data)
		else :
			result = cur.fetchone()
			phone_num = result[0]
			full_name = result[1]
			habit_name = result[2]
			partner_num = result[3]
			data['phone_num'] = phone_num
			data['full_name'] = full_name
			data['habit_name'] = habit_name
			data['partner_num'] = partner_num
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#add to habit data
	time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	sched_obj = datetime.strptime(date_query,'%Y-%m-%dT%H:%M:%S.%fZ')
	sched_obj = sched_obj.replace(hour=0, minute=0, second=0, microsecond=0)
	try :
		cmd = "INSERT INTO habit_data(habit_id,user_hash,date_actual,time_current) VALUES (%s,%s,%s,%s)"
		cur.execute(cmd,(habit_name,hash_query,sched_obj,time_current,))
		conn.commit()
		data["success"] = True
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. Habit data not captured."
		return json.dumps(data)

	#url in text
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000'
	elif "://t." in request.url :
		confirm_url = 'http://t.mindset.ooo'
	else :
		confirm_url = 'http://mindset.ooo'

	sms_message = "MINDSET:\n" + full_name + " completed their habit for today. Send some words of support! Don't forget to complete yours: " + confirm_url
	gsm_regex = "^[A-Za-z0-9 \\r\\n@£$¥èéùìòÇØøÅå\u0394_\u03A6\u0393\u039B\u03A9\u03A0\u03A8\u03A3\u0398\u039EÆæßÉ!\"#$%&'()*+,\\-./:;<=>?¡ÄÖÑÜ§¿äöñüà^{}\\\\\\[~\\]|\u20AC]*$"
	result = re.match(gsm_regex, sms_message)
	if result:
		print("Search successful.")
	else:
		print("Search unsuccessful.")

	client = Client(TWI_ACCOUNT_SID, TWI_AUTH_TOKEN)
	message = client.messages.create(
		body=sms_message,
		from_='+13158205380',
		to="+1" + partner_num
	)

	return json.dumps(data)

@app.route('/api/signup', methods=["POST"])
def signup():
	
	data = {} #json response
	req = request.get_json()
	print(req)

	phone_num = str(req['phone_num'])
	full_name = str(req['full_name'])
	#password = str(req['password'])

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("phone intake: passed DB credentials")
	except:
		print("phone intake: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for phone number
	try :
		cmd = "SELECT * FROM users2 WHERE phone_num = %s;"
		cur.execute(cmd,(phone_num,))
		if cur.rowcount > 0 :
			print("Phone number was already entered.")
			data['error'] = 'Oops! Something went wrong. The phone number was already entered.'
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for session hash
	hash_exist = True;
	while hash_exist:
		session_hash =  hex(random.getrandbits(128))[2:7]
		try :
			cmd = "SELECT * FROM users2 WHERE session_hash = %s;"
			cur.execute(cmd,(session_hash,))
			if cur.rowcount == 0 :
				hash_exist = False
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "Oops! Something went wrong. The database connection failed."
			return json.dumps(data)

	#add to users2 table if new phone number (removed password)
	try :
		cmd = "INSERT INTO users2(phone_num,full_name,session_hash) VALUES (%s,%s,%s)"
		cur.execute(cmd,(phone_num,full_name,session_hash,))
		conn.commit()
	except Exception as e :
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "Oops! Something went wrong. The user was not added to the database."
		return json.dumps(data)


	#verification link
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000?i=' + session_hash
	elif "://t." in request.url :
		confirm_url = 'http://t.mindset.ooo?i=' + session_hash
	else :
		confirm_url = 'http://mindset.ooo?i=' + session_hash

	# # Create an SNS client
	# client = boto3.client(
	# 	"sns",
	# 	aws_access_key_id=AWS_ACCESS_KEY_ID,
	# 	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
	# 	region_name="us-east-1"
	# )

	# # Send your sms message.
	# sms_response = client.publish(
 #    	PhoneNumber="+1" + phone_num,
 #    	Message="Hey " + full_name + "! Mindset here 🎈\n\nPlease click here to verify your number: " + confirm_url
 #    )

	# #check on response and return error message to client for alert
	# print("sms response:",sms_response)
	# data['response'] = sms_response

	sms_message = "MINDSET:\nHey " + full_name + "! Please click here to verify your number: " + confirm_url
	gsm_regex = "^[A-Za-z0-9 \\r\\n@£$¥èéùìòÇØøÅå\u0394_\u03A6\u0393\u039B\u03A9\u03A0\u03A8\u03A3\u0398\u039EÆæßÉ!\"#$%&'()*+,\\-./:;<=>?¡ÄÖÑÜ§¿äöñüà^{}\\\\\\[~\\]|\u20AC]*$"
	result = re.match(gsm_regex, sms_message)
	if result:
		print("Search successful.")
	else:
		print("Search unsuccessful.")

	client = Client(TWI_ACCOUNT_SID, TWI_AUTH_TOKEN)
	message = client.messages.create(
		body=sms_message,
		from_='+13158205380',
		to="+1" + phone_num
	)

	#add to sms_log table
	#time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	# try :
	# 	cmd = "INSERT INTO sms_log(phone_num,message) VALUES (%s,%s)"
	# 	cur.execute(cmd,(phone_num,str(sms_response),))
	# 	conn.commit()
	# 	data['success'] = True
	# except Exception as e :
	# 	print("Database connection failed due to {}".format(e))
	# 	conn.rollback()
	# 	data['error'] = "Oops! Something went wrong. The sms log did not update."
	# 	return json.dumps(data)

	return json.dumps(data)

@app.route('/api/login', methods=["POST"])
def login():
	
	data = {} #json response
	req = request.get_json()
	print(req)

	phone_num = str(req['phone_num'])
	#password = str(req['password'])

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("login: passed DB credentials")
	except:
		print("login: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for phone number (remove password)
	try :
		cmd = "SELECT full_name, session_hash FROM users2 WHERE phone_num = %s;"
		cur.execute(cmd,(phone_num,))
		if cur.rowcount == 0 :
			print("Login failed.")
			data['error'] = 'Oops! We did not find your number. Please try again or sign up.'
			return json.dumps(data)
		else :
			result = cur.fetchone()
			full_name = result[0]
			session_hash = result[1]
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#verification link
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000?l=' + session_hash
	elif "://t." in request.url :
		confirm_url = 'http://t.mindset.ooo?l=' + session_hash
	else :
		confirm_url = 'http://mindset.ooo?l=' + session_hash

	# # Create an SNS client
	# client = boto3.client(
	# 	"sns",
	# 	aws_access_key_id=AWS_ACCESS_KEY_ID,
	# 	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
	# 	region_name="us-east-1"
	# )

	# # Send your sms message.
	# sms_response = client.publish(
 #    	PhoneNumber="+1" + phone_num,
 #    	Message="Hey " + full_name + "! Mindset here 🎈\n\nPlease click here to log in: " + confirm_url
 #    )

	sms_message = "MINDSET:\nHey " + full_name + "! Please click here to log in: " + confirm_url
	gsm_regex = "^[A-Za-z0-9 \\r\\n@£$¥èéùìòÇØøÅå\u0394_\u03A6\u0393\u039B\u03A9\u03A0\u03A8\u03A3\u0398\u039EÆæßÉ!\"#$%&'()*+,\\-./:;<=>?¡ÄÖÑÜ§¿äöñüà^{}\\\\\\[~\\]|\u20AC]*$"
	result = re.match(gsm_regex, sms_message)
	if result:
		print("Search successful.")
	else:
		print("Search unsuccessful.")

	client = Client(TWI_ACCOUNT_SID, TWI_AUTH_TOKEN)
	message = client.messages.create(
		body=sms_message,
		from_='+13158205380',
		to="+1" + phone_num
	)

	return json.dumps(data)

@app.route('/api/incomingsms', methods=["POST"])
def incoming_sms():

	data = {} #json response
	user_email = "akshay@mindset.ooo"
	req = request.get_json(force=True)
	sms_message = json.loads(req['Message']) 
	sms_sender = sms_message.get("originationNumber")[2:]
	sms_body = sms_message.get("messageBody")

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("incoming sms: passed DB credentials")
	except:
		print("incoming sms: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)


	#search database for phone number
	try :
		cmd = "SELECT full_name, partner_num FROM users2 WHERE phone_num = %s;"
		cur.execute(cmd,(sms_sender,))
		if cur.rowcount == 0 :
			print("The phone number was not found.")
			data['error'] = 'Oops! Something went wrong. The phone number was not found.'
			return json.dumps(data)
		else :
			result = cur.fetchone()
			user_name = result[0]
			partner_num = result[1]
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#add to users2 table if new phone number
	try :
		cmd = "INSERT INTO sms_messages(incoming_num,outgoing_num,sms_message) VALUES (%s,%s,%s)"
		cur.execute(cmd,(sms_sender,partner_num,sms_body,))
		conn.commit()
		data['success'] = True
	except Exception as e :
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "Oops! Something went wrong. The user was not added to the database."
		return json.dumps(data)

	# #get partner's nickname
	# try :
	# 	cmd = "SELECT full_name FROM users2 WHERE phone_num = %s;"
	# 	cur.execute(cmd,(partner_num,))
	# 	if cur.rowcount == 0 :
	# 		print("The phone number was not found.")
	# 		data['error'] = 'Oops! Something went wrong. The phone number was not found.'
	# 		return json.dumps(data)
	# 	else :
	# 		partner_name = cur.fetchone()[0]
	# except Exception as e:
	# 	print("Database connection failed due to {}".format(e))
	# 	data['error'] = "Oops! Something went wrong. The database connection failed."
	# 	return json.dumps(data)

	#verification link
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000'
	elif "://t." in request.url :
		confirm_url = 'http://t.mindset.ooo'
	else :
		confirm_url = 'http://mindset.ooo'

	# Create an SNS client
	client = boto3.client(
		"sns",
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
		region_name="us-east-1"
	)

	# Send your sms message.
	client.publish(
    	PhoneNumber="+1" + partner_num,
    	Message=user_name + ": " + sms_body + "\n\n" + confirm_url
    )


	#message
	message = """From: MINDSET <mindset.social2020@gmail.com>
To: <%s>
Subject: Test

Sent by: %s

Sent to: %s

Message sent: %s
""" % (user_email,sms_sender,partner_num,sms_body)

	# Create a secure SSL context
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(EMAIL_SVR,EMAIL_PORT,context=context) as server:
		server.login(EMAIL_USR,EMAIL_PWD)
		server.sendmail(EMAIL_USR,[user_email],message)

	return user_email

@app.route('/api/pairingalert')
def pairing_alert():

	data = {} #json response
	phone_query = str(request.args.get('n'))
	if not phone_query :
		print("num error")
		return json.dumps(data)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("pairing alert: passed DB credentials")
	except:
		print("pairing alert: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for phone number
	try :
		cmd = "SELECT full_name, partner_num FROM users2 WHERE phone_num = %s;"
		cur.execute(cmd,(phone_query,))
		if cur.rowcount == 0 :
			print("Phone number not found.")
			return json.dumps(data)
		else :
			result = cur.fetchone()
			user_name = result[0]
			partner_num = result[1]
			if not partner_num :
				print("User is not paired yet.")
				return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#get partner's nickname
	try :
		cmd = "SELECT full_name FROM users2 WHERE phone_num = %s;"
		cur.execute(cmd,(partner_num,))
		if cur.rowcount == 0 :
			print("The phone number was not found.")
			data['error'] = 'Oops! Something went wrong. The phone number was not found.'
			return json.dumps(data)
		else :
			partner_name = cur.fetchone()[0]
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#url in text
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000'
	elif "://t." in request.url :
		confirm_url = 'http://t.mindset.ooo'
	else :
		confirm_url = 'http://mindset.ooo'

	#sms_message = "Hey " + user_name + "! Mindset here\n\nGreat news, you’ve been paired with " + partner_name + "!\n\nText back to start the conversation.\n\n" + confirm_url
	sms_message = "MINDSET:\nGreat news! We've paired you with " + partner_name + ". Reply to say hello and track your habits here: " + confirm_url
	gsm_regex = "^[A-Za-z0-9 \\r\\n@£$¥èéùìòÇØøÅå\u0394_\u03A6\u0393\u039B\u03A9\u03A0\u03A8\u03A3\u0398\u039EÆæßÉ!\"#$%&'()*+,\\-./:;<=>?¡ÄÖÑÜ§¿äöñüà^{}\\\\\\[~\\]|\u20AC]*$"
	result = re.match(gsm_regex, sms_message)
	if result:
		print("Search successful.")
	else:
		print("Search unsuccessful.")

	# # Create an SNS client
	# client = boto3.client(
	# 	"sns",
	# 	aws_access_key_id=AWS_ACCESS_KEY_ID,
	# 	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
	# 	region_name="us-east-1"
	# )

	# response = client.set_sms_attributes(
	# 	attributes={
	# 	'DefaultSMSType': 'Transactional'
 #    	}
	# )

	# print(response)

	# # Send your sms message.
	# sms_response = client.publish(
 #    	PhoneNumber="+1" + phone_query,
 #    	Message=message
 #    )

	client = Client(TWI_ACCOUNT_SID, TWI_AUTH_TOKEN)
	message = client.messages.create(
		body=sms_message,
		from_='+13158205380',
		to="+1" + phone_query
	)

	# try :
	# 	cmd = "INSERT INTO sms_log(phone_num,message) VALUES (%s,%s)"
	# 	cur.execute(cmd,(phone_query,str(sms_response),))
	# 	conn.commit()
	# except Exception as e :
	# 	print("Database connection failed due to {}".format(e))
	# 	conn.rollback()
	# 	data['error'] = "Oops! Something went wrong. The sms log did not update."
	# 	return json.dumps(data)

	#update confirm timestamp for user or partner
	time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	try:
		cmd = "UPDATE users2 SET pairing_time = %s WHERE phone_num = %s;"
		print("updated user confirm timestamp")
		cur.execute(cmd,(time_current,phone_query,))
		conn.commit()
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	return phone_query

@app.route('/api/phoneintake') #adds user from waiting list
def phone_intake():
	
	data = {} #json response
	phone_query = str(request.args.get('p'))
	name_query = str(request.args.get('n'))
	if not phone_query or not name_query :
		data['error'] = "data missing"
		return json.dumps(data)
	print("phone:",phone_query,"name:",name_query)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("phone intake: passed DB credentials")
	except:
		print("phone intake: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)


	#search database for phone number
	try :
		cmd = "SELECT * FROM users2 WHERE phone_num = %s;"
		cur.execute(cmd,(phone_query,))
		if cur.rowcount > 0 :
			print("Phone number was already entered.")
			data['error'] = 'Oops! Something went wrong. The phone number was already entered.'
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#search database for session hash
	hash_exist = True;
	while hash_exist:
		session_hash =  hex(random.getrandbits(128))[2:7]
		try :
			cmd = "SELECT * FROM users2 WHERE session_hash = %s;"
			cur.execute(cmd,(session_hash,))
			if cur.rowcount == 0 :
				hash_exist = False
		except Exception as e:
			print("Database connection failed due to {}".format(e))
			data['error'] = "Oops! Something went wrong. The database connection failed."
			return json.dumps(data)


	#add to users2 table if new phone number
	try :
		cmd = "INSERT INTO users2(phone_num,full_name,session_hash) VALUES (%s,%s,%s)"
		cur.execute(cmd,(phone_query,name_query,session_hash,))
		conn.commit()
		data['success'] = True
	except Exception as e :
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "Oops! Something went wrong. The user was not added to the database."
		return json.dumps(data)


	#verification link
	if "localhost" in request.url :
		confirm_url = 'http://localhost:5000?i=' + session_hash
	elif "://t." in request.url :
		confirm_url = 'http://t.mindset.ooo?i=' + session_hash
	else :
		confirm_url = 'http://mindset.ooo?i=' + session_hash

	# Create an SNS client
	client = boto3.client(
		"sns",
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
		region_name="us-east-2"
	)

	# Send your sms message.
	client.publish(
    	PhoneNumber="+1" + phone_query,
    	Message="Hey " + name_query + "! Mindset here 🎈\n\nPlease click here to verify your number: " + confirm_url
    )

	data['success'] = True
	return json.dumps(data)

@app.route('/api/verifyphone') #verifies user in when clicks sign up link
def verify_phone():
	
	data = {} #json response
	hash_query = str(request.args.get('i'))
	if not hash_query:
		data['error'] = "data missing"
		return json.dumps(data)
	print("hash:",hash_query)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("phone intake: passed DB credentials")
	except:
		print("phone intake: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#check if hash exists and not verified in DB 
	try :
		cmd = "SELECT habit_id FROM users2 WHERE session_hash = %s AND verify_num IS NULL"
		cur.execute(cmd,(hash_query,))
		if cur.rowcount == 0 :
			data['error'] = "Hmm... This verification link is not valid."
			return json.dumps(data)
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#update confirm timestamp for user or partner
	time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	try:
		cmd = "UPDATE users2 SET verify_num = %s WHERE session_hash = %s"
		print("updated user confirm timestamp")
		cur.execute(cmd,(time_current,hash_query,))
		conn.commit()
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	data['success'] = True
	return json.dumps(data)

@app.route('/api/verifylogin') #verifies user in when clicks login link
def verify_login():
	
	data = {} #json response
	hash_query = str(request.args.get('l'))
	if not hash_query:
		data['error'] = "data missing"
		return json.dumps(data)
	print("hash:",hash_query)

	#connect to DB
	try :
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("phone intake: passed DB credentials")
	except:
		print("phone intake: did not pass DB credentials")
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	#check if hash exists
	try :
		cmd = "SELECT habit_id FROM users2 WHERE session_hash = %s"
		cur.execute(cmd,(hash_query,))
		if cur.rowcount == 0 :
			data['error'] = "Hmm... This verification link is not valid."
			return json.dumps(data)
		else :
			data['habit_name'] = cur.fetchone()[0]
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		data['error'] = "Oops! Something went wrong. The database connection failed."
		return json.dumps(data)

	# #update confirm timestamp for user or partner
	# time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	# try:
	# 	cmd = "UPDATE users2 SET verify_num = %s WHERE session_hash = %s"
	# 	print("updated user confirm timestamp")
	# 	cur.execute(cmd,(time_current,hash_query,))
	# 	conn.commit()
	# except Exception as e:
	# 	print("Database connection failed due to {}".format(e))
	# 	conn.rollback()
	# 	data['error'] = "Oops! Something went wrong. The database connection failed."
	# 	return json.dumps(data)

	data['success'] = True
	return json.dumps(data)


@app.route('/api/newhabit', methods=["POST"]) #adds new habit to DB
def new_habit():

	data = {} #json response
	req = request.get_json()
	print(req)

	session_hash = str(req['session_hash'])
	habit_name = str(req['habit_name'])
	if not session_hash or not habit_name:
		data['error'] = "data missing"
		return json.dumps(data)

	#connect to DB
	try:
		conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=PWD, port=PORT, database=DBNAME)
		cur = conn.cursor(buffered=True)
		print("session list: passed DB credentials")
	except:
		print("session list: did not pass DB credentials")
		data['error'] = "unable to connect with DB"
		return json.dumps(data)

	#create new habit_id
	# add habit to habit table

	#update habit_id for user
	try:
		cmd = "UPDATE users2 SET habit_id = %s WHERE session_hash = %s"
		print("updated habit_ud")
		cur.execute(cmd,(habit_name,session_hash,))
		conn.commit()
	except Exception as e:
		print("Database connection failed due to {}".format(e))
		conn.rollback()
		data['error'] = "failed to connect to users table"
		return json.dumps(data)

	data['success'] = True
	return json.dumps(data)


@app.route('/api/timedata') #returns time data
def time_data():
	
	data = {} #json response
	time_current = datetime.utcnow()
	data['time_current'] = time_current.replace(tzinfo=timezone.utc).isoformat()
	return json.dumps(data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()