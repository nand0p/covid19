@app.route('/static/chart.min.js')
def chart():
    static_path = os.path.join(app.root_path, 'static')
    return send_from_directory(static_path, 'chart.min.js', mimetype='text/javascript')


@app.route('/totals')
def totals(path='/reports/total'):
  html = header + api_endpoint + path
  totals_json = call_api(api_endpoint + path)
  html += parse_totals(totals_json)
  return html


@app.route('/regions')
def regions(path='/regions'):
  html = header + api_endpoint + path
  regions_json = call_api(api_endpoint + path)
  html += get_html(regions_json)
  return html
  

@app.route('/provinces')  
def provinces(path='/provinces/USA'):
  html = header + api_endpoint + path
  provinces_json = call_api(api_endpoint + path)
  html += get_html(provinces_json)
  return html


@app.route('/reports')
def reports(path='/reports'):
  html = header + api_endpoint + path
  reports_json = call_api(api_endpoint + path)
  html += get_html(reports_json)
  return html
