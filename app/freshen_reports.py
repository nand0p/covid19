import requests
import json

reports_file = 'reports.json'
reports_dir = 'reports/'
api_endpoint = 'https://covid-api.com/api/reports'

with open('dates.json', 'r') as infile:
  dates = json.load(infile)

def main():
  print('slurping ' + api_endpoint)
  for day in dates:
    with open(reports_dir + day + '_' + reports_file, 'wb') as outjson:
      payload = {'date': day, 'iso': 'USA'}
      response = requests.get(api_endpoint, params=payload)
      print('saving ' + response.url)
      outjson.write(response.content)

  
if __name__ == '__main__':
  main()
