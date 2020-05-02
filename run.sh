#!/bin/bash

. venv/bin/activate
if [ $# -gt 0 ]; then
    FLASK_APP=server.py FLASK_ENV=development flask run -p $1
else
    FLASK_APP=server.py FLASK_ENV=development flask run -p 5000
fi