import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def redeploy():
    subprocess.run(["git", "fetch", "origin"])
    subprocess.run(["git", "rebase", "origin/master"])
    subprocess.run(["npm", "run", "build"], cwd="frontend")
    return jsonify(status=200)

app.run(processes=1)