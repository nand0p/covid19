import requests
import json


def load_json(json_file):
  with open(json_file, 'r') as infile:
    jsonout = json.load(infile)
  return jsonout 


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
