from datetime import datetime, timedelta
from utils import get_dates_hash
import matplotlib.pyplot as plt
import requests
import pandas
import json

provinces = []
provinces_file = 'states.json'
reports_file = 'reports.json'
reports_dir = 'reports/'
image_dir = 'static/images/'
dates_file = 'dates.json'
api_endpoint = 'https://covid-api.com/api/'
first_date = '2020-04-16'

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


def dump_dates():
  with open(dates_file, 'w') as fileout:
    json.dump(_get_dates(), fileout)


def _get_dates():
  yesterday = datetime.today() - timedelta(days = 1)
  return pandas.date_range(start=first_date,end=yesterday).strftime(date_format='%Y-%m-%d').to_list()


def make_reports():
  raw_reports = []
  reports = []
  reports_parsed = []

  for day in _get_dates():
    with open(reports_dir + day + '_reports.json', 'r') as reports_in:
      raw_reports = json.load(reports_in)
    for records in raw_reports.values():
      for record in records:
          reports.append({'date': record['date'], 'state': record['region']['province'], 'deaths': record['deaths'], 'confirmed': record['confirmed'], 'deaths_diff': record['deaths_diff'], 'confirmed_diff': record['confirmed_diff']})

  for state in states:
    state_deaths = []
    death_growth_rate = []
    state_confirmed = []
    confirmed_growth_rate = []
    state_danger = False

    for report in reports:
      if state == report['state']:
        state_deaths.append(report['deaths'])
        state_confirmed.append(report['confirmed'])

    for day in range(0, len(state_deaths)):
      #print('(' + str(state_deaths[day]) + '/' + str(state_deaths[0]) + ')**(1/' + str(day) + ')-1)')
      if day == 0:
        death_growth_rate.append(0.0000001)
      else:
        death_growth_rate.append(round((state_deaths[day]/state_deaths[0])**(1/day)-1, 7))

    for day in range(0, len(state_confirmed)):
      #print('(' + str(state_confirmed[day]) + '/' + str(state_confirmed[0]) + ')**(1/' + str(day) + ')-1)')
      if day == 0:
        confirmed_growth_rate.append(0.0000001)
      else:
        confirmed_growth_rate.append(round((state_confirmed[day]/state_confirmed[0])**(1/day)-1, 7))

    if death_growth_rate[-1] > death_growth_rate[-2] or confirmed_growth_rate[-1] > confirmed_growth_rate[-2]:
      state_danger = True;
    reports_parsed.append({'state': state, 'dates': _get_dates(), 'deaths': state_deaths, 'confirmed': state_confirmed, 'confirmed_growth_rate': confirmed_growth_rate, 'death_growth_rate': death_growth_rate, 'danger': state_danger})

  with open(reports_file, 'w') as fileout:
    json.dump(reports_parsed, fileout)
  return reports_parsed


def get_raw_json():
  for day in _get_dates():
    with open(reports_dir + day + '_' + reports_file, 'wb') as outjson:
      payload = {'date': day, 'iso': 'USA'}
      response = requests.get(api_endpoint + 'reports', params=payload)
      print('processing ' + response.url)
      outjson.write(response.content)


def make_images(reports):
  for record in reports:
    plt.clf()

    # iowa hack
    while len(record['death_growth_rate']) != len(_get_dates()):
      record['death_growth_rate'].append(0.000001)
    while len(record['confirmed_growth_rate']) != len(_get_dates()):
      record['confirmed_growth_rate'].append(0.000001)

    plt.plot(_plot_dates(),record['death_growth_rate'])
    plt.plot(_plot_dates(),record['confirmed_growth_rate'])
    plt.ylabel('Growth Rates')
    plt.xlabel('Dates')
    plt.savefig(image_dir + record['state'] + '.' + get_dates_hash(dates_file) + '.png', transparent=True)


def _plot_dates():
  display_dates = []
  display_dates.append(_get_dates()[0])
  for spacer in range(1, len(_get_dates()) - 1):
    display_dates.append(str(spacer))
  display_dates.append(_get_dates()[-1])
  return display_dates

def main():
  get_raw_json()
  dump_dates()
  reports = make_reports()
  make_images(reports)


if __name__ == '__main__':
  main()
