#!/bin/sh -ex

cd app

if [ "$1" == "state"]; then
  python make_state.py
fi

FLASK_APP=index.py flask run
