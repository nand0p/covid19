from flask import Flask
import requests


app = Flask(__name__)


@app.route('/')
def home():
  raw_json = requests.get('https://api.covid19api.com/live/country/US').json()
  return print_html(raw_json)


def print_html(raw_json):
  html = 'Covid-19 Data Visualization<p>'
  html += '<p>state deaths<p>'
  html += get_state_info('New York', raw_json)
  html += get_state_info('Texas', raw_json)
  html += get_state_info('Oregon', raw_json)
  html += get_state_info('New Hampshire', raw_json)
  html += get_state_info('Idaho', raw_json)
  html += get_state_info('Minnesota', raw_json)
  html += get_state_info('Maryland', raw_json)
  html += get_state_info('Nebraska', raw_json)
  html += get_state_info('New Jersey', raw_json)
  html += get_state_info('Georgia', raw_json)
  html += get_state_info('Louisiana', raw_json)
  html += get_state_info('Iowa', raw_json)
  html += get_state_info('Arizona', raw_json)
  html += get_state_info('Oklahoma', raw_json)
  html += get_state_info('Delaware', raw_json)
  html += get_state_info('Connecticut', raw_json)
  html += get_state_info('Michigan', raw_json)
  html += get_state_info('Colorado', raw_json)
  html += get_state_info('Washington', raw_json)
  html += get_state_info('Mississippi', raw_json)
  html += get_state_info('Tennessee', raw_json)
  html += get_state_info('South Dakota', raw_json)
  html += get_state_info('Pennsylvania', raw_json)
  html += get_state_info('Missouri', raw_json)
  html += get_state_info('Ohio', raw_json)
  html += get_state_info('Virginia', raw_json)
  html += get_state_info('Alabama', raw_json)
  html += get_state_info('New Mexico', raw_json)
  html += get_state_info('Montana', raw_json)
  html += get_state_info('Kansas', raw_json)
  html += get_state_info('North Dakota', raw_json)
  html += get_state_info('Wisconsin', raw_json)
  html += get_state_info('Rhode Island', raw_json)
  html += get_state_info('Hawaii', raw_json)
  html += get_state_info('Vermont', raw_json)
  html += get_state_info('Illinois', raw_json)
  html += get_state_info('Massachusetts', raw_json)
  html += get_state_info('Maine', raw_json)
  html += get_state_info('Kentucky', raw_json)
  html += get_state_info('Indiana', raw_json)
  html += get_state_info('Alaska', raw_json)
  html += get_state_info('Utah', raw_json)
  html += get_state_info('Florida', raw_json)
  html += get_state_info('North Carolina', raw_json)
  html += get_state_info('West Virginia', raw_json)
  html += get_state_info('South Carolina', raw_json)
  return html


def get_state_info(state, raw_json):
  state_html = '<p>' + '<table border=10>'
  state_info = {}
  for entry in raw_json:
    if entry['Province'] == state:
      state_info[entry['Date']] = str(entry['Deaths'])

  state_list = list(state_info.items())
  for entry in state_list:
    state_html += '<tr><td>' + state + '</td><td>' + entry[0] + '</td><td>' + entry[1] + '</td></tr>'
  rate_growth = (int(state_list[-1][1])/int(state_list[0][1]))**(1/len(state_list))-1
  state_html += '<tr><td>' + state + '</td><td>rate of growth:</td><td>' + str(rate_growth) + '</td></tr></table>'
  return state_html
  

if __name__ == '__main++':
  app.run(debug=True)
