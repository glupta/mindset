from flask import Flask, render_template
from flask import request, jsonify, make_response
from datetime import datetime
import json

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

@app.route('/api/timedetails')
def timedetails():
	data = {}
	data['time_current'] = datetime.now().isoformat()
	data['time_sched'] = datetime(2020,6,19,19,2).isoformat()
	return json.dumps(data)

@app.route('/api/requestroom', methods=["POST"])
def requestroom():
	req = request.get_json()
	print(req)
	res = make_response(jsonify(req), 200)
	return res

	#for each chat room
		#if chat room < 2 users
			#add user to room
			#break

	#if user not added to any chat room
		#create new chat room
		#add user to chat room
		#add boolean api calls 
		#update DB that in chat is true

#add device/client ID to active user list in db
#return when added

#volunteer continually checks until all users are true

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()