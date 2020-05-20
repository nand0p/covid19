import json
import requests

provinces = []
provinces_file = 'states.json'
reports_file = 'reports.json'
reports_dir = 'reports/'
date_file = 'dates.json'
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
]

remove_provinces = [
  'Norfolk County, MA',
  'Alameda County, CA',
  'American Samoa',
  'Ashland, NE',
  'Bennington County, VT',
  'Bergen County, NJ',
  'Berkshire County, MA',
  'Berkeley, CA',
  'Boston, MA',
  'Broward County, FL',
  'Carver County, MN',
  'Charleston County, SC',
  'Charlotte County, FL',
  'Chatham County, NC',
  'Cherokee County, GA',
  'Chicago',
  'Chicago, IL',
  'Clark County, NV',
  'Clark County, WA',
  'Cobb County, GA',
  'Collin County, TX',
  'Contra Costa County, CA',
  'Cook County, IL',
  'Davidson County, TN',
  'Davis County, UT',
  'Delaware County, PA',
  'Denver County, CO',
  'Diamond Princess',
  'District of Columbia',
  'Douglas County, CO',
  'Douglas County, NE',
  'Douglas County, OR',
  'El Paso County, CO',
  'Fairfax County, VA',
  'Fairfield County, CT',
  'Fayette County, KY',
  'Federal Bureau of Prisons',
  'Floyd County, GA',
  'Fort Bend County, TX',
  'Fresno County, CA',
  'Fulton County, GA',
  'Grafton County, NH',
  'Grand Princess',
  'Grand Princess Cruise Ship',
  'Grant County, WA', 
  'Guam',
  'Harford County, MD',
  'Harris County, TX',
  'Harrison County, KY',
  'Hendricks County, IN',
  'Hillsborough, FL',
  'Honolulu County, HI',
  'Hudson County, NJ',
  'Humboldt County, CA',
  'Jackson County, OR',
  'Jefferson County, KY',
  'Jefferson County, WA',
  'Jefferson Parish, LA',
  'Johnson County, IA',
  'Johnson County, KS', 
  'Kershaw County, SC',
  'King County, WA',
  'Kittitas County, WA',
  'Klamath County, OR',
  'Lackland, TX',
  'Lackland, TX (From Diamond Princess)',
  'Lee County, FL',
  'Los Angeles, CA', 
  'Madera County, CA', 
  'Madison, WI', 
  'Manatee County, FL',
  'Maricopa County, AZ',
  'Marion County, IN',
  'Marion County, OR',
  'Middlesex County, MA',
  'Montgomery County, MD', 
  'Montgomery County, PA',
  'Montgomery County, TX',
  'Nassau County, NY',
  'New York City, NY',
  'New York County, NY',
  'Norfolk County, MA', 
  'Northern Mariana Islands',
  'Norwell County, MA', 
  'Okaloosa County, FL',
  'Omaha, NE (From Diamond Princess)',
  'Orange County, CA',
  'Orange, CA',
  'Pierce County, WA',
  'Pinal County, AZ',
  'Placer County, CA',
  'Plymouth County, MA',
  'Polk County, GA',
  'Portland, OR',
  'Providence County, RI',
  'Providence, RI',
  'Queens County, NY',
  'Ramsey County, MN',
  'Recovered', 
  'Riverside County, CA',
  'Rockingham County, NH',
  'Rockland County, NY',
  'Sacramento County, CA',
  'San Antonio, TX',
  'San Benito, CA',
  'San Diego County, CA',
  'San Francisco County, CA',
  'San Mateo, CA',
  'Santa Clara County, CA',
  'Santa Clara, CA',
  'Santa Cruz County, CA',
  'Santa Rosa County, FL',
  'Sarasota, FL',
  'Saratoga County, NY',
  'Seattle, WA',
  'Shasta County, CA',
  'Shelby County, TN',
  'Snohomish County, WA',
  'Sonoma County, CA', 
  'Spartanburg County, SC',
  'Spokane County, WA',
  'St. Louis County, MO', 
  'Suffolk County, MA',
  'Suffolk County, NY',
  'Summit County, CO',
  'Tempe, AZ', 
  'Travis, CA',
  'Travis, CA (From Diamond Princess)',
  'Tulsa County, OK',
  'Ulster County, NY',
  'Umatilla, OR',
  'Unassigned Location (From Diamond Princess)',
  'Unassigned Location, VT',
  'Unassigned Location, WA',
  'United States Virgin Islands',
  'Unknown Location, MA',
  'US',
  'US Military', 
  'Veteran Hospitals', 
  'Virgin Islands, U.S.',
  'Volusia County, FL',
  'Wake County, NC', 
  'Washington County, OR',
  'Washington, D.C.',
  'Washoe County, NV',
  'Wayne County, PA', 
  'Westchester County, NY',
  'Williamson County, TN', 
  'Wuhan Evacuee',
  'Yolo County, CA'
]


def make_dates():
  with open(date_file, 'w') as fileout:
    json.dump(dates, fileout)


def make_states():
  response = requests.get('https://covid-api.com/api/provinces/USA')
  for entry in json.loads(response.content)['data']:
    provinces.append(entry['province'].strip())
  for province in remove_provinces:
    provinces.remove(province)
  print('states: ' + str(provinces))
  with open(provinces_file, 'w') as fileout:
    json.dump(provinces, fileout)


def make_reports():
  reports_list = []
  reports = []
  for day in dates:
    with open(reports_dir + day + '_reports.json', 'r') as reports_in:
      reports_list = json.load(reports_in)['data']
    for record in reports_list:
      if record['region']['iso'] == 'USA':
        state = record['region']['province']
        deaths = record['deaths']
        date = record['date']
        reports.append([date, state, deaths])
  print(reports)
  with open(reports_file, 'w') as fileout:
    json.dump(reports, fileout)


def main():
  make_states()
  make_dates()
  make_reports()


if __name__ == '__main__':
  main()
