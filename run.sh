#!/bin/sh -ex

cd app

python make_state.py
#python freshen_reports.py

FLASK_APP=index.py flask run
