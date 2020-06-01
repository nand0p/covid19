import matplotlib
import matplotlib.pyplot as plt
import requests
import json

provinces = []
provinces_file = 'states.json'
reports_file = 'reports.json'
reports_dir = 'reports/'
image_dir = 'static/images/'
date_file = 'dates.json'
api_endpoint = 'https://covid-api.com/api/'
dates = [
  '2020-04-16',
  '2020-04-17',
  '2020-04-18',
  '2020-04-19',
  '2020-04-20',
  '2020-04-21',
  '2020-04-22',
  '2020-04-23',
  '2020-04-24',
  '2020-04-25',
  '2020-04-26',
  '2020-04-27',
  '2020-04-28',
  '2020-04-29',
  '2020-04-30',
  '2020-05-01',
  '2020-05-02',
  '2020-05-03',
  '2020-05-04',
  '2020-05-05',
  '2020-05-06',
  '2020-05-07',
  '2020-05-08',
  '2020-05-09',
  '2020-05-10',
  '2020-05-11',
  '2020-05-12',
  '2020-05-13',
  '2020-05-14',
  '2020-05-15',
  '2020-05-16',
  '2020-05-17',
  '2020-05-18',
  '2020-05-19',
  '2020-05-20',
  '2020-05-21',
  '2020-05-22',
  '2020-05-23',
  '2020-05-24',
  '2020-05-25',
  '2020-05-26',
  '2020-05-27',
  '2020-05-28',
  '2020-05-29',
  '2020-05-30',
  '2020-05-31',
]

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']



def make_dates():
  with open(date_file, 'w') as fileout:
    json.dump(dates, fileout)


def make_reports():
  raw_reports = []
  reports = []
  reports_parsed = []
  for day in dates:
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
    reports_parsed.append({'state': state, 'dates': dates, 'deaths': state_deaths, 'confirmed': state_confirmed, 'confirmed_growth_rate': confirmed_growth_rate, 'death_growth_rate': death_growth_rate, 'danger': state_danger})
  with open(reports_file, 'w') as fileout:
    json.dump(reports_parsed, fileout)
  return reports_parsed


def get_raw_json():
  for day in dates:
    with open(reports_dir + day + '_' + reports_file, 'wb') as outjson:
      payload = {'date': day, 'iso': 'USA'}
      response = requests.get(api_endpoint + 'reports', params=payload)
      print('processing ' + response.url)
      outjson.write(response.content)


def make_images(reports):
  for record in reports:
    plt.clf()
    plt.plot(dates,record['death_growth_rate'])
    plt.plot(dates,record['confirmed_growth_rate'])
    plt.ylabel('Growth Rates')
    plt.xlabel('Dates')
    plt.savefig(image_dir + record['state'] + '.png', transparent=True)


def main():
  get_raw_json()
  make_dates()
  reports = make_reports()
  make_images(reports)


if __name__ == '__main__':
  main()
