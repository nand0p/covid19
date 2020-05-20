from flask import Flask, send_from_directory
from utils import load_json
import urllib.parse
import requests
import json
import os


app = Flask(__name__, static_url_path='/static')
api_endpoint = 'https://covid-api.com/api'
dates_file = 'dates.json'
states_file = 'states.json'
reports_file = 'reports.json'
reports_dir = 'reports/'
header = '<link rel="icon" type="image/x-icon" href="favicon.ico" />' + \
         '<h1>Covid-19 US Statistics</h1><p>'


@app.route('/favicon.ico')
def favicon():
    static_path = os.path.join(app.root_path, 'static')
    return send_from_directory(static_path, 'favicon.ico', mimetype='image/xicon')


@app.route('/')
def home():
  states = load_json(states_file)
  reports = load_json(reports_file)
  dates = load_json(dates_file)
  html = header + get_warnings(states, reports)
  for state in states:
    html += '<table border=30 width=100%>' + \
            get_state_info_rows(state, dates, reports) + \
            get_growth_rate_rows(state, reports) + '</table>'
  return html


def get_warnings(states, reports):
  danger = []
  for state in states:
    for record in reports:
      if state == record['state']:
        if record['danger'] == True:
          danger.append(state)
  return '<p>Total US deaths: <font color=red>' + str(death_total(reports)) + \
         '</font><p>There are <font color=red>' + str(len(list(set(danger)))) + \
         '</font> states with an <font color=red>increasing</font> growth rate: ' + str(list(set(danger))) + \
         '<p>COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University'


def death_total(reports):
  total = 0
  for record in reports:
    total = total + record['deaths'][-1]
  return total


def get_state_info_rows(state, dates, reports):
  html = ''
  for record in reports:
    if state == record['state']:
      counter = 0
      for deaths in record['deaths']:
        if counter == 0:
          html += '<tr><td><h1><center>' + state + '</center></h1></td><td>' + str(dates[counter]) + '</td>' + \
                  '<td>' + str(deaths) + '</td><td rowspan=6><img src=/static/images/' + \
                  urllib.parse.quote(state) + '.png></td></tr>'
        if counter == len(dates)-1 or counter == len(dates)-2 or counter == len(dates)-3:
          html += '<tr><td>.</td><td>' + str(dates[counter]) + '</td>' + \
                  '<td>' + str(deaths) + '</td></tr>'
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
