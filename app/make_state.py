from utils import get_dates_hash, spacer, load_json, dump_json, get_states, get_dates

import matplotlib.pyplot as plt
import requests
import random
import numpy
import json
import time


class Covid19:

  def __init__(self):
    self.states = get_states()
    self.reports_file = 'reports.json'
    self.reports_dir = 'reports/'
    self.image_dir = 'static/images/'
    self.api_endpoint = 'https://covid-api.com/api/'
    self.dates_file = 'dates.json'
    self.first_date = '2020-04-16'
    self.dates = get_dates(self.first_date)
    self.reports = []
    self.reports_parsed = []


  def dump_dates(self):
    dump_json(self.dates_file, self.dates)


  def dump_reports(self):
    dump_json(self.reports_file, self.reports_parsed)


  def make_reports(self):
    for day in self.dates:
      raw_reports = load_json(self.reports_dir + day + '_reports.json')
      for records in raw_reports.values():
        for record in records:
            self.reports.append({
              'date': record['date'],
              'state': record['region']['province'],
              'deaths': record['deaths'],
              'confirmed': record['confirmed'],
              'deaths_diff': record['deaths_diff'],
              'confirmed_diff': record['confirmed_diff'],
              'fatality_rate': record['fatality_rate'],
            })


  def parse_reports(self):
    for state in self.states:
      state_deaths = []
      state_confirmed = []
      state_fatality = []
      death_growth_rates = []
      confirmed_growth_rates = []
      fatality_growth_rates = []
      state_danger = False

      for report in self.reports:
        if state == report['state']:
          state_deaths.append(report['deaths'])
          state_confirmed.append(report['confirmed'])
          state_fatality.append(report['fatality_rate'])

      for day in range(0, len(state_deaths)):
        if day == 0:
          death_growth_rates.append(0.01)
        else:
          death_growth_rates.append(self._get_rate(state_deaths[0:day]))

      for day in range(0, len(state_confirmed)):
        if day == 0:
          confirmed_growth_rates.append(0.01)
        else:
          confirmed_growth_rates.append(self._get_rate(state_confirmed[0:day]))

      for day in range(0, len(state_fatality)):
        if day == 0:
          fatality_growth_rates.append(0.01)
        else:
          fatality_growth_rates.append(self._get_rate(state_fatality[0:day]))

      if len(death_growth_rates) > 1 and \
        len(confirmed_growth_rates) > 1 and \
        len(fatality_growth_rates) > 1:
        if death_growth_rates[-1] > death_growth_rates[-2] or \
          confirmed_growth_rates[-1] > confirmed_growth_rates[-2] or \
          fatality_growth_rates[-1] > fatality_growth_rates[-2]:
          state_danger = True;
        elif death_growth_rates[-1] == death_growth_rates[-2] or \
          confirmed_growth_rates[-1] == confirmed_growth_rates[-2] or \
          fatality_growth_rates[-1] == fatality_growth_rates[-2]:
          state_danger = random.choice([True, False])

      self.reports_parsed.append({
        'state': state,
        'dates': self.dates,
        'deaths': state_deaths,
        'confirmed': state_confirmed,
        'fatality': state_fatality,
        'confirmed_growth_rates': confirmed_growth_rates,
        'death_growth_rates': death_growth_rates,
        'fatality_growth_rates': fatality_growth_rates,
        'danger': state_danger,
      })


  def _get_rate(self, rate_list):

    _rate = numpy.diff(rate_list) / rate_list[:-1] * 100
    #_rate = (numpy.exp(numpy.diff(numpy.log(rate_list)))[0] - 1) * 100

    if not _rate.any():
      _rate = [ 0.01 ]

    return round(_rate[-1], 2)


  def get_raw_json(self):
    for day in self.dates:
      with open(self.reports_dir + \
                day + \
                '_' + \
                self.reports_file, \
                'wb') as outjson:

        payload = {'date': day, 'iso': 'USA'}
        response = requests.get(self.api_endpoint + 'reports', params=payload)
        print('processing ' + response.url)
        outjson.write(response.content)
        time.sleep(0.1)


  def make_images(self):
    for record in self.reports_parsed:

      # iowa missing data hack
      while len(record['death_growth_rates']) != len(self.dates):
        record['death_growth_rates'].insert(0, 0.01)
        #print('fluffing array make_images death', record['death_growth_rates'])
      while len(record['confirmed_growth_rates']) != len(self.dates):
        record['confirmed_growth_rates'].insert(0, 0.01)
        #print('fluffing array make_images infection', record['confirmed_growth_rates'])
      while len(record['fatality_growth_rates']) != len(self.dates):
        record['fatality_growth_rates'].insert(0, 0.01)
        #print('fluffing array make_images fatality', record['fatality_growth_rates'])

      plt.clf()
      plt.plot(self._plot_dates(),record['death_growth_rates'])
      plt.plot(self._plot_dates(),record['confirmed_growth_rates'])
      plt.plot(self._plot_dates(),record['fatality_growth_rates'])
      plt.ylabel('Growth Rates')
      plt.xlabel('Dates')
      plt.savefig(self.image_dir + record['state'] + '.' + get_dates_hash(self.dates_file) + '.png',
                  transparent=True)


  def _plot_dates(self):
    display_dates = []
    display_dates.append(self.dates[0] + spacer(20))
    for day in range(1, len(self.dates) - 1):
      display_dates.append(day)
    display_dates.append(spacer(20) + self.dates[-1])
    return display_dates


def main():
  covid = Covid19()
  covid.get_raw_json()
  covid.dump_dates()
  covid.make_reports()
  covid.parse_reports()
  covid.dump_reports()
  covid.make_images()


if __name__ == '__main__':
  main()
