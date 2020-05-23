from flask import Flask, send_from_directory
from utils import load_json
import urllib.parse
import requests
import json
import os


app = Flask(__name__, static_url_path='/static')
api_endpoint = 'https://covid-api.com/api'
dates_file = 'dates.json'
reports_file = 'reports.json'
reports_dir = 'reports/'
header = '<link rel="icon" type="image/x-icon" href="favicon.ico" />''<h1>Covid-19 US Statistics</h1><p>'
footer = '<p<br><center>If you find this useful, please contribute:<br><b>' + \
         'BTC: 112JJvxsvRYn4QtpWJqZmLsTbPEG7aPsdB<br>' + \
         'ETH: 0x5b857cc1103c82384457BACdcd6E2a9FCD0b7e2A'

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


@app.route('/favicon.ico')
def favicon():
    static_path = os.path.join(app.root_path, 'static')
    return send_from_directory(static_path, 'favicon.ico', mimetype='image/xicon')


@app.route('/')
def home():
  reports = load_json(reports_file)
  dates = load_json(dates_file)
  html = header + get_scoreboard(reports)
  for state in states:
    html += '<table border=30 width=100%>' + \
            get_state_info_rows(state, dates, reports) + \
            get_growth_rate_rows(state, reports) + '</table>'
  html += footer
  return html


def get_scoreboard(reports):
  danger = []
  rates = []
  deaths = []
  for state in states:
    for record in reports:
      if state == record['state']:
        if record['danger'] == True:
          danger.append(state)
        rate = record['rate'][-1]
        death = record['deaths'][-1]
        rates.append([rate, state])
        deaths.append([death, state])
  rates.sort()
  deaths.sort()
  html = '<p>Total US deaths: <font color=red><b>' + str(death_total(reports)) + \
          '</b></font> -- SEDME<p>There are <font color=red><b>' + str(len(list(set(danger)))) + \
          '</b></font> states with an <font color=red>increasing</font> growth rate: ' + str(list(set(danger))) + \
          '<p>Top rate growth:<br>-------------------------<br>'
  for r in range(9, 1, -1):
    r = r - 10
    html += str(rates[r]) + '<br>'
  html += '<p>Top deaths:<br>-----------------<br>'
  for r in range(9, 1, -1):
    r = r - 10
    html += str(deaths[r]) + '<br>'
  html += '<p>COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University'
  return html


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
                  urllib.parse.quote(state) + '.png width=100%><br>' + str(dates) + '</td></tr>'
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
