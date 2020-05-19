from flask import Flask, send_from_directory
import requests
import json
import os

#import base64
#import matplotlib.pyplot as plt

app = Flask(__name__)
api_endpoint = 'https://covid-api.com/api'
header = '<script src="static/chart.min.js"></script><link rel="icon" type="image/x-icon" href="favicon.ico" /><b>Covid 19 Statistics</b><p>'
dates_file = 'dates.json'
states_file = 'states.json'
reports_dir = 'reports/'


@app.route('/favicon.ico')
def favicon():
    static_path = os.path.join(app.root_path, 'static')
    return send_from_directory(static_path, 'favicon.ico', mimetype='image/xicon')


@app.route('/static/chart.min.js')
def chart():
    static_path = os.path.join(app.root_path, 'static')
    return send_from_directory(static_path, 'chart.min.js', mimetype='text/javascript')


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
    state_html, deaths = get_state_info(state, record, dates, deaths)
    html += state_html
  html += get_growth_rate(deaths, dates)
  return html


def get_state_info(state, record, dates, deaths):
  state_html = ''
  if record['deaths']:
    if record['region']['province'] == state and record['region']['iso'] == 'USA':
      deaths.append(record['deaths'])
      if record['date'] == dates[0] or record['date'] == dates[-1] or record['date'] == dates[-2]:
        state_html += '<tr><td>' + record['region']['province'] + '</td><td>' + record['date'] + '</td><td>' + str(record['deaths']) + '</td></tr>'
  return state_html, deaths


def get_growth_rate(deaths, dates):
  growth_html = ''
  growth_rate = []
  for day in range(1, len(deaths)):
    print('(' + str(deaths[day]) + '/' + str(deaths[0]) + ')**(1/' + str(day) + ')-1)')
    growth_rate.append((deaths[day]/deaths[0])**(1/day)-1)

  if growth_rate[-1] > growth_rate[-2]:
    growth_html += get_growth_html('red', deaths, growth_rate)
  else:
    growth_html += get_growth_html('green', deaths, growth_rate)

  growth_html += get_growth_chart(growth_rate, dates)
  return growth_html


def get_growth_chart(growth_rate, dates):
  chart_html = '<td colspan=3>' + str(growth_rate) + '</td></tr><br>' + str(dates)

  #graph = io.BytesIO()
  #plt.plot(growth_rate,range(1,len(growth_rate)))
  #plt.savefig(graph, format='png')
  #graph.seek(0)
  #plot_url = base64.b64encode(graph.getvalue()),decode()
  #graph.write_image('/tmp/image.jpg')
  #growth_html += '<td colspan=3><img src="data:image/png;base64,' + plot_url + '"></td></tr>'
  #growth_html += '<td colspan=3>' + render_template('chart.html', values=growth_rate, labels=range(1,len(deaths))) + '</td></tr>'
  return chart_html


def get_growth_html(color, deaths, growth_rate):
  return '<tr><td bgcolor=' + color + '>current growth rate</td>' + \
         '<td bgcolor=' + color + '>first:' + str(deaths[0]) + ' last:' + str(deaths[-1]) + ' len:' + str(len(deaths)) + '</td>' + \
         '<td bgcolor=' + color + '>' + str(growth_rate[-1]) + '</td></tr><tr>' + \
         '<td bgcolor=' + color + '>last growth rate</td><td bgcolor=' + color + '>first:' + \
         str(deaths[0]) + ' last:' + str(deaths[-2]) + ' len:' + str(len(deaths)-1) + '</td>' + \
         '<td bgcolor=' + color + '>' + str(growth_rate[-2]) + '</td></tr>'


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
  with open(reports_dir + day + '_reports.json', 'r') as reports_in:
    reports_list = json.load(reports_in)['data']
  return reports_list
  

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
