from datetime import datetime, timedelta
from utils import get_dates_hash

import matplotlib.pyplot as plt
import requests
import pandas
import random
import numpy
import json
import time


provinces = []
provinces_file = 'states.json'
reports_file = 'reports.json'
reports_dir = 'reports/'
image_dir = 'static/images/'
dates_file = 'dates.json'
api_endpoint = 'https://covid-api.com/api/'
first_date = '2020-04-16'

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


def dump_dates(dates):
  with open(dates_file, 'w') as fileout:
    json.dump(dates, fileout)


def get_dates():
  yesterday = datetime.today() - timedelta(days = 1)
  return pandas.date_range(start=first_date,end=yesterday).strftime(date_format='%Y-%m-%d').to_list()


def make_reports(dates):
  raw_reports = []
  reports = []
  reports_parsed = []

  for day in dates:
    with open(reports_dir + day + '_reports.json', 'r') as reports_in:
      raw_reports = json.load(reports_in)
    for records in raw_reports.values():
      for record in records:
          reports.append({
            'date': record['date'],
            'state': record['region']['province'],
            'deaths': record['deaths'],
            'confirmed': record['confirmed'],
            'deaths_diff': record['deaths_diff'],
            'confirmed_diff': record['confirmed_diff'],
            'fatality_rate': record['fatality_rate'],
          })

  for state in states:
    state_deaths = []
    state_confirmed = []
    state_fatality = []
    death_growth_rate = []
    confirmed_growth_rate = []
    fatality_growth_rate = []
    state_danger = False

    for report in reports:
      if state == report['state']:
        state_deaths.append(report['deaths'])
        state_confirmed.append(report['confirmed'])
        state_fatality.append(report['fatality_rate'])

    for day in range(0, len(state_deaths)):
      if day == 0:
        death_growth_rate.append(0.01)
      else:
        death_growth_rate.append(_get_rate(state_deaths[0:day]))

    for day in range(0, len(state_confirmed)):
      if day == 0:
        confirmed_growth_rate.append(0.01)
      else:
        confirmed_growth_rate.append(_get_rate(state_confirmed[0:day]))

    for day in range(0, len(state_fatality)):
      if day == 0:
        fatality_growth_rate.append(0.01)
      else:
        fatality_growth_rate.append(_get_rate(state_fatality[0:day]))

    if death_growth_rate[-1] > death_growth_rate[-2] or \
      confirmed_growth_rate[-1] > confirmed_growth_rate[-2] or \
      fatality_growth_rate[-1] > fatality_growth_rate[-2]:
      state_danger = True;
    elif death_growth_rate[-1] == death_growth_rate[-2] or \
      confirmed_growth_rate[-1] == confirmed_growth_rate[-2] or \
      fatality_growth_rate[-1] == fatality_growth_rate[-2]:
      state_danger = random.choice([True, False])

    reports_parsed.append({
      'state': state,
      'dates': dates,
      'deaths': state_deaths,
      'confirmed': state_confirmed,
      'fatality': state_fatality,
      'confirmed_growth_rate': confirmed_growth_rate,
      'death_growth_rate': death_growth_rate,
      'fatality_growth_rate': fatality_growth_rate,
      'danger': state_danger,
    })

  with open(reports_file, 'w') as fileout:
    json.dump(reports_parsed, fileout)
  return reports_parsed


def _get_rate(rate_list):
  if len(rate_list) < 2:
    _rate = [ 0.01 ]
  else:
    _rate = numpy.diff(rate_list) / rate_list[:-1] * 100
    #_rate = (numpy.exp(numpy.diff(numpy.log(rate_list)))[0] - 1) * 100
  if _rate[-1] < 0.01:
    return 0.01
  else:
    return round(_rate[-1], 2)


def get_raw_json(dates):
  for day in dates:
    with open(reports_dir + day + '_' + reports_file, 'wb') as outjson:
      payload = {'date': day, 'iso': 'USA'}
      response = requests.get(api_endpoint + 'reports', params=payload)
      print('processing ' + response.url)
      outjson.write(response.content)
      time.sleep(0.5)


def make_images(reports, dates):
  for record in reports:

    # iowa missing data hack
    while len(record['death_growth_rate']) != len(dates):
      record['death_growth_rate'].insert(0, 0.01)
    while len(record['confirmed_growth_rate']) != len(dates):
      record['confirmed_growth_rate'].insert(0, 0.01)
    while len(record['fatality_growth_rate']) != len(dates):
      record['fatality_growth_rate'].insert(0, 0.01)

    plt.clf()
    plt.plot(_plot_dates(dates),record['death_growth_rate'])
    plt.plot(_plot_dates(dates),record['confirmed_growth_rate'])
    plt.plot(_plot_dates(dates),record['fatality_growth_rate'])
    plt.ylabel('Growth Rates')
    plt.xlabel('Dates')
    plt.savefig(image_dir + record['state'] + '.' + get_dates_hash(dates_file) + '.png',
                transparent=True)


def _plot_dates(dates):
  display_dates = []
  display_dates.append(dates[0] + _spacer())
  for day in range(1, len(dates) - 1):
    display_dates.append(day)
  display_dates.append(_spacer() + dates[-1])
  return display_dates


def _spacer():
  spacer = '.'
  for space in range(20):
    spacer += '.'
  return spacer


def main():
  dates = get_dates()
  get_raw_json(dates)
  dump_dates(dates)
  reports = make_reports(dates)
  make_images(reports, dates)


if __name__ == '__main__':
  main()
