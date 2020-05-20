from flask import Flask, send_from_directory
from utils import load_json
import requests
import json
import os


app = Flask(__name__)
api_endpoint = 'https://covid-api.com/api'
dates_file = 'dates.json'
states_file = 'states.json'
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
  for state in states:
    html += '<table border=4>' + get_state_html(state) + '</table>'
  return html


def get_state_html(state):
  html = ''
  reports_list = []
  growth = []
  deaths = []
  dates = load_json(dates_file)
  for day in dates:
    reports_list += get_reports_list(day)
  for record in reports_list:
    state_html, deaths = get_state_info_rows(state, record, dates, deaths)
    html += state_html
  growth_html, growth_rate = get_growth_rate_rows(deaths, dates)
  html += growth_html
  html += get_growth_chart_rows(growth_rate, dates)
  return html


def get_state_info_rows(state, record, dates, deaths):
  state_html = ''
  if record['deaths']:
    if record['region']['province'] == state and record['region']['iso'] == 'USA':
      deaths.append(record['deaths'])
      if record['date'] == dates[0] or record['date'] == dates[-1] or record['date'] == dates[-2]:
        state_html += '<tr><td>' + record['region']['province'] + '</td><td>' + record['date'] + '</td>' + \
                      '<td>' + str(record['deaths']) + '</td></tr>'
  return state_html, deaths


def get_growth_rate_rows(deaths, dates):
  growth_html = ''
  growth_rate = []
  for day in range(1, len(deaths)):
    print('(' + str(deaths[day]) + '/' + str(deaths[0]) + ')**(1/' + str(day) + ')-1)')
    growth_rate.append((deaths[day]/deaths[0])**(1/day)-1)
  if growth_rate[-1] > growth_rate[-2]:
    growth_html += get_growth_html('red', deaths, growth_rate)
  else:
    growth_html += get_growth_html('green', deaths, growth_rate)
  return growth_html, growth_rate


def get_growth_chart_rows(growth_rate, dates):
  chart_html = '<tr><td colspan=3>' + str(growth_rate) + '<br>' + str(dates) + '</td></tr>'
  #chart_html = '<tr><td colspan=3><table border=10 width=100%><tr height=100>'
  #for entry in growth_rate:
  #  if entry < .0001:
  #    entry = .0001
  #  chart_html += '<td bgcolor=blue><b>'
  #  for x in range(1,int(entry*1000)):
  #    chart_html += ' X '
  #  chart_html += '</b></td>'
  #chart_html += '</tr><tr>'
  #for date in dates:
  #  if date is not dates[0]:
  #      chart_html += '<td>' + date[5:] + '</td>'
  #chart_html += '</tr><tr>'
  #for rate in growth_rate:
  #  chart_html += '<td>' + str(round(rate,4)) + '</td>'
  #chart_html += '</tr></table></td></tr>'
  return chart_html


def get_growth_html(color, deaths, growth_rate):
  return '<tr><td bgcolor=' + color + '>current growth rate</td>' + \
         '<td bgcolor=' + color + '>first:' + str(deaths[0]) + ' last:' + str(deaths[-1]) + ' len:' + str(len(deaths)) + '</td>' + \
         '<td bgcolor=' + color + '>' + str(growth_rate[-1]) + '</td></tr><tr>' + \
         '<td bgcolor=' + color + '>last growth rate</td><td bgcolor=' + color + '>first:' + \
         str(deaths[0]) + ' last:' + str(deaths[-2]) + ' len:' + str(len(deaths)-1) + '</td>' + \
         '<td bgcolor=' + color + '>' + str(growth_rate[-2]) + '</td></tr>'


def get_reports_list(day):
  with open(reports_dir + day + '_reports.json', 'r') as reports_in:
    reports_list = json.load(reports_in)['data']
  return reports_list
  

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
