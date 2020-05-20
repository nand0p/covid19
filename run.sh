#!/bin/sh -ex

cd app

python make_state.py

FLASK_APP=index.py flask run
