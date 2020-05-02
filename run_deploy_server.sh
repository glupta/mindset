#!/bin/bash

. venv/bin/activate
FLASK_APP=deploy.py FLASK_ENV=development flask run -p 5050