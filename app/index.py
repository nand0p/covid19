from flask import Flask, send_from_directory
from utils import load_json
import requests
import json
import os


app = Flask(__name__)
api_endpoint = 'https://covid-api.com/api'
dates_file = 'dates.json'
states_file = 'states.json'
reports_file = 'reports.json'
reports_dir = 'reports/'
header = '<link rel="icon" type="image/x-icon" href="favicon.ico" />' + \
         '<b>Covid 19 Statistics</b><p>'


@app.route('/favicon.ico')
def favicon():
    static_path = os.path.join(app.root_path, 'static')
    return send_from_directory(static_path, 'favicon.ico', mimetype='image/xicon')


@app.route('/')
def home(path='/reports'):
  html = header + api_endpoint + path
  states = load_json(states_file)
  reports = load_json(reports_file)
  dates = load_json(dates_file)
  for state in states:
    html += '<table border=4>' + get_state_html(state, dates, reports) + '</table>'
  return html


def get_state_html(state, dates, reports):
  html = get_state_info_rows(state, dates, reports)
  html += get_growth_rate_rows(state, reports)
  html += get_growth_chart_rows(state, dates, reports)
  return html


def get_state_info_rows(state, dates, reports):
  html = ''
  for record in reports:
    if state == record['state']:
      counter = 0
      for deaths in record['deaths']:
        if counter == 0 or counter == len(dates)-1 or counter == len(dates)-2 or counter == len(dates)-3:
          html += '<tr><td>' + state + '</td><td>' + str(dates[counter]) + '</td><td>' + str(deaths) + '</td></tr>'
        counter = counter + 1
  return html


def get_growth_rate_rows(state, reports):
  html = ''
  for record in reports:
    if state == record['state']:
      if record['rate'][-1] > record['rate'][-2]:
        html += get_growth_html('red', record['deaths'], record['rate'])
      else:
        html += get_growth_html('green', record['deaths'], record['rate'])
  return html


def get_growth_chart_rows(state, dates, reports):
  html = ''
  for record in reports:
    if state == record['state']:
      html += '<tr><td colspan=3>' + str(record['rate']) + '<br>' + str(dates) + '</td></tr>'
  return html


def get_growth_html(color, deaths, growth_rate):
  return '<tr><td bgcolor=' + color + '>last growth rate</td>' + \
         '<td bgcolor=' + color + '>first:' + str(deaths[0]) + ' last:' + str(deaths[-2]) + ' len:' + str(len(deaths)-1) + '</td>' + \
         '<td bgcolor=' + color + '>' + str(growth_rate[-2]) + '</td></tr>' + \
         '<td bgcolor=' + color + '>current growth rate</td>' + \
         '<td bgcolor=' + color + '>first:' + str(deaths[0]) + ' last:' + str(deaths[-1]) + ' len:' + str(len(deaths)) + '</td>' + \
         '<td bgcolor=' + color + '>' + str(growth_rate[-1]) + '</td></tr><tr>'


def get_reports_list(day):
  with open(reports_dir + day + '_reports.json', 'r') as reports_in:
    reports_list = json.load(reports_in)['data']
  return reports_list
  

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
