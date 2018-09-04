import os
from flask import Flask, flash, redirect, render_template, request, session, abort, make_response, url_for
#from random import randint
import pandas as pd
import numpy as np
import gspread
from altair import Chart, X, Y, Color, Scale, Axis, Data, DataFormat
import altair as alt
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

#scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
#gc = gspread.authorize(credentials)


#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
#
#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)
#
## Paginate file lists by specifying number of max results
#for file_list in drive.ListFile({'maxResults': 10}):
#  print('Received %s files from Files.list()' % len(file_list)) # <= 10
#  for file1 in file_list:
#    print('title: %s, id: %s' % (file1['title'], file1['id']))
    
    
    
# read all data in spreadsheet and organise into a dict
#def get_meta():
#    meta = {}
#    raw_data = {}
#    sh =  gc.open('KPI-Dashboard-Example')
#    #    ws = sh.get_worksheet(1)
#    for i, ws in enumerate(sh.worksheets()):
#        # any sheet with a cell value of type is made into a widget
#        raw_data[ws.title] = ws.get_all_values()
#    
#    for j, ws in enumerate(raw_data):
#        if any(['type' in i for i in raw_data[ws]]):
#            meta[ws] = {}
#            for i in raw_data[ws]:
#                try:
#                    val = int(i[1])
#                except:
#                    val = i[1]
#                meta[ws][i[0]] = val
#            
#            if meta[ws]['type'] == 'horizontal-bar':
#                meta[ws]['color-class'] = 'c1-bg'
#            else:
#                meta[ws]['color-class'] = 'c' + str(j) + '-bg'
#            
#            if meta[ws].get('data', False):
#                data = raw_data[meta[ws]['data']]
#                meta[ws]['df'] = data
#            
#            if str(meta[ws].get('value', 'no value')).count(' ') > 0 and meta[ws]['type'] == 'simple':
#                meta[ws]['type'] = 'text'
#    
#            def get_val(key):
#                return int(meta['kpi2meta'].get(key, 50).replace(',', '').replace('£', ''))
#            
#            if meta[ws]['type'] == 'budget-spent':
#                meta[ws]['perc-spent'] = str(int(round(get_val('spent') / get_val('total') * 100, 0)))
#    return meta
#meta = get_meta()



        # set some default values
# appened static content with version number to overcome caching
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# serve index html
@app.route("/")
def index():
#    meta = get_meta()
#    mymeta = meta
    mymeta = {'kpi5meta': {'type': 'simple', 'value': 6, 'color-class': 'c6-bg'}, 'kpi6meta': {'type': 'simple', 'value': 8, 'color-class': 'c8-bg'}}
    return render_template('grid.html',**locals())


# horizontal bar chart - currently with hardcoded name
#@app.route("/data/kpi1meta")
#def data_bar():
#    data = gc.open_by_key('1rO7J7iriFjE3d7Hbc4vW5uzz_xpOCmnorMCU9Ehik2Q').sheet1.get_all_values()
#    meta = get_meta()
#    mymeta = meta
#    df = pd.DataFrame(data[1:], columns=data[0]).copy()
#    tb = df.groupby(['Profession']).size()
#
##    data['value'] = pd.to_numeric(data['value'])
##    data.dtypes
#    df = tb.reset_index()
#    temp = df[df['Profession'] != '']
#    temp.columns = ['category', 'value']
##    temp['value'] = pd.to_numeric(temp['value'])
#
#    data = temp
#
#
#
#    bars = alt.Chart(data, height=150, width=50).mark_bar(size=15).encode(
#        alt.X('value:Q', axis=Axis(title='')),
#        alt.Y('category:N', axis=Axis(title=''))
#    )
#    
#    text = bars.mark_text(
#        align='left',
#        baseline='middle',
#        dx=3,
#        font='HelveticaNeue',
#        fontSize=15,
##        fontStyle=Undefined
#    ).encode(
#        text='value'
#    )
#    
#    chart = bars + text
#    chart = chart.configure_axis(grid=False, ticks=False
#                  ).configure_axisX(labels=False, domainColor='transparent'
#                  ).configure_axisY(domainColor='transparent', labelFont='HelveticaNeue', labelFontSize=15, labelLimit=300, labelPadding=6
#                  ).configure_view(strokeOpacity=0)
#    return chart.to_json()

## remaining bar chart - currently with hardcoded name
#@app.route("/data/kpi2meta")
#def data_bar2():
#    mymeta = meta
##    data = mymeta['kpi1meta']['df']
#    def get_val(key):
#        return int(mymeta['kpi2meta'].get(key, 50).replace(',', '').replace('£', ''))
#    total_spent = get_val('total') - get_val('remaining')
#    data = pd.DataFrame({'value': [total_spent, get_val('remaining')], 'category': ['remaining', 'total']})
##    data['value'] = pd.to_numeric(data['value'])
#    data.dtypes
#
#
#    chart = alt.Chart(data, height=40, width=250).mark_bar(size=40).encode(
#        alt.X('value:Q', axis=Axis(title='')),
##        alt.Y('category:N', axis=Axis(title=''))
#        alt.Color('category:N', legend=None, scale=Scale(domain=['remaining', 'total'], range=['rgb(234, 112, 112)', 'green']))
#    )
#
#    chart = chart.configure_axis(grid=False, ticks=False
#                  ).configure_axisX(labels=False, domainColor='transparent'
#                  ).configure_axisY(domainColor='transparent'
#                  ).configure_view(strokeOpacity=0)
#    return chart.to_json()


if __name__ == '__main__':
    app.run(debug=True)