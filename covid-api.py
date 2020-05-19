from flask import Flask
import requests
import json


app = Flask(__name__)
api_endpoint = 'https://covid-api.com/api'
header = '<b>Covid 19 Statistics</b><p>'
dates_file = 'dates.json'
states_file = 'states.json'


@app.route('/')
def home(path='/reports'):
  html = header + api_endpoint + path
  states = load_json(states_file)
  for state in states:
    html += '<table border=4>' + get_state_html(state) + '</table>'
  return html


def get_state_html(state):
  html = ''
  reports_list = []
  first_day = ''
  second_day = ''
  last_day = ''
  dates = load_json(dates_file)
  for day in dates:
    if day == dates[0]:
      reports_list += get_reports_list(day)
    elif day == dates[-1]:
      reports_list += get_reports_list(day)
    elif day == dates[-2]:
      reports_list += get_reports_list(day)
  for record in reports_list:
    if record['region']['iso'] == 'USA':
      state_html, f_day, l_day, s_day = get_state_info(state, record, dates)
      if f_day:
        first_day = f_day
      if l_day:
        last_day = l_day
      if s_day:
        second_day = s_day
      html += state_html
  html += get_growth_rate(first_day, last_day, second_day, len(dates))
  return html


def get_state_info(state, record, dates):
  state_html = ''
  first_day = ''
  last_day = ''
  second_day = ''
  if record['region']['province'] == state:
    if record['date'] == dates[0]:
      if record['deaths']:
        first_day = record['deaths']
    elif record['date'] == dates[-1]:
      if record['deaths']:
        last_day = record['deaths']
    elif record['date'] == dates[-2]:
      if record['deaths']:
        second_day = record['deaths']
    state_html += '<tr><td>' + record['region']['province'] + '</td><td>' + record['date'] + '</td><td>' + str(record['deaths']) + '</td></tr>'
  return state_html, first_day, last_day, second_day


def get_growth_rate(first_day, last_day, second_day, length):
  if not first_day:
    first_day = -1
  if not last_day:
    last_day = -1
  if not second_day:
    second_day = -1
  growth_rate = (last_day/first_day)**(1/length)-1
  growth_rate_last = (second_day/first_day)**(1/(length-1))-1
  growth_html = '<tr><td>current growth rate</td><td>first:' + str(first_day) + ' last:' + str(last_day) + ' len:' + str(length) + '</td><td>' + str(growth_rate) + '</td></tr>'
  growth_html += '<tr><td>last growth rate</td><td>first:' + str(first_day) + ' last:' + str(second_day) + ' len:' + str(length-1) + '</td>'
  if growth_rate_last < growth_rate:
    growth_html += '<td bgcolor=red>' + str(growth_rate_last) + '</td>'
  else:
    growth_html += '<td bgcolor=green>' + str(growth_rate_last) + '</td>'
  growth_html += '</tr>'
  return growth_html


@app.route('/totals')
def totals(path='/reports/total'):
  html = header + api_endpoint + path
  totals_json = call_api(api_endpoint + path)
  html += parse_totals(totals_json)
  return html


@app.route('/regions')
def regions(path='/regions'):
  html = header + api_endpoint + path
  regions_json = call_api(api_endpoint + path)
  html += get_html(regions_json)
  return html
  

@app.route('/provinces')  
def provinces(path='/provinces/USA'):
  html = header + api_endpoint + path
  provinces_json = call_api(api_endpoint + path)
  html += get_html(provinces_json)
  return html


@app.route('/reports')
def reports(path='/reports'):
  html = header + api_endpoint + path
  reports_json = call_api(api_endpoint + path)
  html += get_html(reports_json)
  return html


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
  

def get_reports_list(day):
  with open(day + '_reports.json', 'r') as reports_in:
    reports_list = json.load(reports_in)['data']
  return reports_list
  

if __name__ == '__main++':
  app.run(debug=True,host='0.0.0.0',port=5000)
