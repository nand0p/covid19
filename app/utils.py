from datetime import datetime, timedelta

import requests
import hashlib
import random
import pandas
import json


def load_json(json_file):
  with open(json_file, 'r') as infile:
    jsonout = json.load(infile)
  return jsonout 


def dump_json(jsonfile, structure):
  with open(jsonfile, 'w') as fileout:
    json.dump(structure, fileout)


def call_api(call):
  return requests.get(call).json()


def get_html(json):
  html = '<table border=4>'
  for item in json['data']:
    html += '<tr><td>' + str(item) + '</td></tr>'
  html += '</table'
  return html


def parse_totals(json):
  html = '<table border=5>'
  for key, value in json['data'].items():
    html += '<tr><td>' + key + '</td><td>' + str(value) + '</td></tr>'
  html += '</table>'
  return html


def get_dates_hash(dates_file):
  with open(dates_file, 'rb') as f:
    bytes = f.read()
    dates_hash = hashlib.sha256(bytes).hexdigest()
  return dates_hash


def spacer(chars):
  spacer = '.'
  for space in range(chars):
    spacer += '.'
  return spacer


def get_dates(first_date):
  yesterday = datetime.today() - timedelta(days = 1)
  return pandas.date_range(start=first_date,end=yesterday).strftime(date_format='%Y-%m-%d').to_list()


def get_states():
  return ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


def check_danger(r1, r2, r3):
  if len(r1) > 1 and len(r2) > 1 and len(r3) > 1:
    if r1[-1] > r1[-2] or r2[-1] > r2[-2] or r3[-1] > r3[-2]:
      return True
    elif r1[-1] == r1[-2] or r2[-1] == r2[-2] or r3[-1] == r3[-2]:
      return random.choice([True, False])
  return False
