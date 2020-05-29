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
footer = '<center><p>COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University' + \
         '<p>SEDME<br><a href=https://github.com/nand0p/covid19>https://github.com/nand0p/covid19</a><p>If you find this useful, please contribute:<br><b>' + \
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
  death_growth_rates = []
  deaths = []
  confirmed_growth_rates = []
  confirmed = []
  for state in states:
    for record in reports:
      if state == record['state']:
        if record['danger'] == True:
          danger.append(state)
        death_growth_rate = record['death_growth_rate'][-1]
        confirmed_growth_rate = record['confirmed_growth_rate'][-1]
        death = record['deaths'][-1]
        confirm = record['confirmed'][-1]
        death_growth_rates.append([death_growth_rate, state])
        confirmed_growth_rates.append([confirmed_growth_rate, state])
        deaths.append([death, state])
        confirmed.append([confirm, state])
  death_growth_rates.sort()
  confirmed_growth_rates.sort()
  deaths.sort()
  confirmed.sort()
  return '<p>Total US deaths: <font color=red><b>' + str(calculate_totals(reports, 'deaths')) + '</b></font><p>' + \
         'Total US confirmed infections: <font color=red><b>' + str(calculate_totals(reports, 'confirmed')) + '</b></font><p>' + \
         'There are <font color=red><b>' + str(len(list(set(danger)))) + '</b></font>' + \
         ' states with an <font color=red><b>increasing</b></font> death or infection growth rate: ' + str(list(set(danger))) + \
         '<p><table cellpadding=30><tr><td>Top Infections:<hr>' + calculate_top_ten(confirmed) + '</td>' + \
         '<td><p>Top Deaths:<hr>' + calculate_top_ten(deaths) + '</td>' + \
         '<td><p>Top Infection Growth<hr>' + calculate_top_ten(confirmed_growth_rates) + '</td>' + \
         '<td><p>Top Death Growth<hr>' + calculate_top_ten(death_growth_rates) + '</td></tr></table><p>'


def calculate_top_ten(type):
  top_ten = ''
  for count in range(9, -1, -1):
    count = count - 10
    top_ten += str(type[count]) + '<br>'
  return top_ten
    

def calculate_totals(reports, report_type):
  total = 0
  for record in reports:
    total = total + record[report_type][-1]
  return total


def get_state_info_rows(state, dates, reports):
  html = ''
  for record in reports:
    if state == record['state']:
      counter = 0
      for deaths in record['deaths']:
        if counter == 0:
          html += '<tr><td><h1><center>' + state + '</center></h1></td><td>' + str(dates[counter]) + '</td>' + \
                  '<td>deaths: ' + str(deaths) + '<br>infections: ' + str(record['confirmed'][0]) + '</td><td rowspan=6><img src=/static/images/' + \
                  urllib.parse.quote(state) + '.png width=100%><br>' + str(dates) + '</td></tr>'
        if counter == len(dates)-1 or counter == len(dates)-2 or counter == len(dates)-3:
          html += '<tr><td>.</td><td>' + str(dates[counter]) + '</td>' + \
                  '<td>deaths: ' + str(deaths) + '<br>infections: ' + str(record['confirmed'][counter]) + '</td></tr>'
        counter = counter + 1
  return html


def get_growth_rate_rows(state, reports):
  for record in reports:
    if state == record['state']:
      if record['danger']:
        return get_growth_html('red', record['deaths'], record['death_growth_rate'], record['confirmed'], record['confirmed_growth_rate'])
      else:
        return get_growth_html('green', record['deaths'], record['death_growth_rate'], record['confirmed'], record['confirmed_growth_rate'])


def get_growth_html(color, deaths, death_growth_rate, confirmed, confirmed_growth_rate):
  return '<tr><td bgcolor=' + color + '>last growth rates</td>' + \
         '<td bgcolor=' + color + '>first: ' + str(deaths[0]) + '<br>last: ' + str(deaths[-2]) + '<br>len: ' + str(len(deaths)-1) + '<p>' + \
         '<br>first: ' + str(confirmed[0]) + '<br>last: ' + str(confirmed[-2]) + '<br>len: ' + str(len(confirmed)-1) + '</td>' + \
         '<td bgcolor=' + color + '>death: ' + str(death_growth_rate[-2]) + '<p>infection: ' + str(confirmed_growth_rate[-2]) + '</td></tr>' + \
         '<tr><td bgcolor=' + color + '>current growth rates</td>' + \
         '<td bgcolor=' + color + '>first: ' + str(deaths[0]) + '<br>last: ' + str(deaths[-1]) + '<br>len: ' + str(len(deaths)) + '<p>' + \
         'first: ' + str(confirmed[0]) + '<br>last: ' + str(confirmed[-1]) + '<br>len: ' + str(len(confirmed)) + '</td>' + \
         '<td bgcolor=' + color + '>death: ' + str(death_growth_rate[-1]) + '<p>infection: ' + str(confirmed_growth_rate[-1]) + '</td></tr><tr>'


def get_reports_list(day):
  with open(reports_dir + day + '_reports.json', 'r') as reports_in:
    reports_list = json.load(reports_in)['data']
  return reports_list
  

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
