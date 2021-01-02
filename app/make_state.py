from utils import get_dates_hash, spacer, load_json, dump_json, get_states, get_dates, check_danger

import matplotlib.pyplot as plt
import requests
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

    dump_json(self.dates_file, self.dates)


  def parse_json(self):
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


  def _get_rates(self, report, growth_rates):
    for day in range(0, len(report)):
      if day == 0:
        growth_rates.append(0.01)
      else:
        growth_rates.append(self._get_rate(report[0:day]))

    return growth_rates


  def make_reports(self):
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

      death_growth_rates = self._get_rates(state_deaths, death_growth_rates)
      confirmed_growth_rates = self._get_rates(state_confirmed, confirmed_growth_rates)
      fatality_growth_rates = self._get_rates(state_fatality, fatality_growth_rates)

      state_danger = check_danger(death_growth_rates,
                                  confirmed_growth_rates,
                                  fatality_growth_rates)

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

      dump_json(self.reports_file, self.reports_parsed)


  def _get_rate(self, rate_list):

    _rate = numpy.diff(rate_list) / rate_list[:-1] * 100
    #_rate = (numpy.exp(numpy.diff(numpy.log(rate_list)))[0] - 1) * 100

    if not _rate.any():
      _rate = [ 0.01 ]

    return round(_rate[-1], 2)


  def get_raw_json(self):
    for day in self.dates:
      with open(self.reports_dir + day + '_' + self.reports_file, 'wb') as outjson:
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
  covid.parse_json()
  covid.make_reports()
  covid.make_images()


if __name__ == '__main__':
  main()
