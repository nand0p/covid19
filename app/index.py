from utils import load_json, get_dates_hash, get_states
from html_helper import get_header, get_footer
from flask_classful import FlaskView
from flask import Flask

import urllib.parse
import requests
import json
import os


app = Flask(__name__, static_url_path='/static')


class Covid19(FlaskView):

  def __init__(self):
    self.states = get_states()
    self.dates_file = 'dates.json'
    self.reports_file = 'reports.json'
    self.reports = load_json(self.reports_file)
    self.dates = load_json(self.dates_file)
    self.danger = []
    self.deaths = []
    self.confirmed = []
    self.fatality = []
    self.deaths_growth = []
    self.confirmed_growth = []
    self.fatality_growth = []
    self.scoreboard_items = 10


  def index(self):
    html = get_header()
    html += self._get_scoreboard()

    for state in self.states:
      html += '<table border=30 width=100%>' + \
              self._get_state_info_rows(state) + \
              self._get_growth_rate_rows(state) + \
              '</table>'

    html += get_footer()

    return html


  def _get_scoreboard(self):
    self.danger = []
    self.deaths = []
    self.confirmed = []
    self.fatality = []
    self.deaths_growth = []
    self.confirmed_growth = []
    self.fatality_growth = []

    for state in self.states:
      for record in self.reports:
        if state == record['state']:
          if record['danger'] == True:
            if state not in self.danger:
              self.danger.append(state)

          self.deaths.append([ record['deaths'][-1], state ])
          self.deaths_growth.append([ record['death_growth_rates'][-1], state ])
          self.confirmed.append([ record['confirmed'][-1], state ])
          self.confirmed_growth.append([ record['confirmed_growth_rates'][-1], state ])
          self.fatality.append([ record['fatality'][-1], state ])
          self.fatality_growth.append([ record['fatality_growth_rates'][-1], state ])

    self.danger.sort()
    self.deaths.sort()
    self.confirmed.sort()
    self.fatality.sort()
    self.deaths_growth.sort()
    self.confirmed_growth.sort()
    self.fatality_growth.sort()

    # jinjafy this
    return '<p>Total US deaths: <font color=red><b>' + \
           str(self._calculate_totals('deaths')) + \
           '</b></font><p>Total US confirmed infections: <font color=red><b>' + \
           str(self._calculate_totals('confirmed')) + \
           '</b></font><p>There are <font color=red><b>' + \
           str(len(self.danger)) + \
           '</b></font> states with <font color=red><b>increasing</b>' + \
           '</font> growth rates.<p><table cellpadding=30>' + \
           '<tr><td>Top Infections:<hr>' + \
           self._calculate_top_ten(self.confirmed, False) + \
           '</td><td>Top Infection Growth:<hr>' + \
           self._calculate_top_ten(self.confirmed_growth, True) + \
           '</td></tr><tr><td>Top Deaths:<hr>' + \
           self._calculate_top_ten(self.deaths, False) + \
           '</td><td>Top Death Growth:<hr>' + \
           self._calculate_top_ten(self.deaths_growth, True) + \
           '</td></tr><tr><td>Top Fatality Rate:<hr>' + \
           self._calculate_top_ten(self.fatality, False) + \
           '</td><td>Top Fatality Rate Growth:<hr>' + \
           self._calculate_top_ten(self.fatality_growth, True) + \
           '</td></tr></table><p>'


  def _calculate_top_ten(self, report, growth):
    top_ten = ''

    for count in range(self.scoreboard_items -1, -1, -1):
      count = count - self.scoreboard_items
      rate = str(report[count][0])
      state = report[count][1].replace(' ', '_')
      top_ten += rate + '&#37;___' + state + '<br>' if growth else \
                 rate + '___' + state + '<br>'

    return top_ten


  def _calculate_totals(self, report_type):
    total = 0

    for record in self.reports:
      total = total + record[report_type][-1]

    return total


  def _get_state_info_rows(self, state):
    html = ''
    for record in self.reports:
      if state == record['state']:
        counter = 0
        for deaths in record['deaths']:

          if counter == 0:
            html += '<tr><td><h1><center>' + \
                    state + \
                    '</center></h1></td><td>' + \
                    str(self.dates[counter]) + \
                    '</td><td>death: ' + \
                    str(deaths) + \
                    '<br>infection: ' + \
                    str(record['confirmed'][0]) + \
                    '<br>fatality: ' + \
                    str(record['fatality'][0]) + \
                    '</td><td rowspan=6><img src=/static/images/' + \
                    urllib.parse.quote(state) + \
                    '.' + \
                    get_dates_hash(self.dates_file) + \
                    '.png width=100%></td></tr>'

          if counter == len(self.dates) - 1 or \
            counter == len(self.dates) - 2 or \
            counter == len(self.dates) - 3:
            html += '<tr><td>.</td><td>' + \
                    str(self.dates[counter]) + \
                    '</td><td>death: ' + \
                    str(deaths) + \
                    '<br>infection: ' + \
                    str(record['confirmed'][counter]) + \
                    '<br>fatality: ' + \
                    str(record['fatality'][counter]) + \
                    '</td></tr>'

          counter = counter + 1

    return html


  def _get_growth_rate_rows(self, state):
    for record in self.reports:
      if state == record['state']:
        color = 'red' if record['danger'] else 'green'

        # jinjafy this
        return '<tr><td align=center bgcolor=' + \
               color + \
               '>last growth rates</td><td bgcolor=' + \
               color + \
               '><br>len:' + \
               str(len(self.dates) - 1) + \
               '</td><td bgcolor=' + \
               color + \
               '>death: ' + \
               str(record['death_growth_rates'][-2]) + \
               '&#37;<br>infection: ' + \
               str(record['confirmed_growth_rates'][-2]) + \
               '&#37;<br>fatality: ' + \
               str(record['fatality_growth_rates'][-2]) + \
               '&#37;</td></tr><tr><td align=center bgcolor=' + \
               color + \
               '>current growth rates</td><td bgcolor=' + \
               color + \
               '>len:' + \
               str(len(self.dates)) + \
               '</td><td bgcolor=' + \
               color + \
               '>death: ' + \
               str(record['death_growth_rates'][-1]) + \
               '&#37;<br>infection: ' + \
               str(record['confirmed_growth_rates'][-1]) + \
               '&#37;<br>fatality: ' + \
               str(record['fatality_growth_rates'][-1]) + \
               '&#37;</td></tr>'


Covid19.register(app, route_base='/')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
