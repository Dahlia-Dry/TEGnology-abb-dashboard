from dash import Dash, callback, Output, Input, State,no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import pymysql
import datetime
from dash.exceptions import PreventUpdate
from decouple import config
import boto3
import numpy as np

from dashboard_components.dashboard_layout import *
import dashboard_components.email_smtp as email_smtp
import dashboard_components.settings as settings
import dashboard_components.timestream_wrapper as aws_ts

fontawesome='https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css'
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,fontawesome])
app.scripts.append_script({ 'external_url' : mathjax })
server = app.server
app.layout = LAYOUT
timestream_region_name='eu-central-1'

abb_db = aws_ts.TimestreamDB('tegnology_demo_sensors','abb')


@callback(
    [Output('temp-graph', 'figure'),
     Output('last-updated','children')],
    [Input('update_interval', 'n_intervals'),
     Input('n_points','value')]
)
def update_graph(value,buffer_length,sampling_frequency = 180):
    try:
        results = pd.DataFrame.from_records(abb_db.read(buffer_length))
        results['time'] = pd.to_datetime(results['time'])+datetime.timedelta(hours=2)
        results['current_scaled'] =4+(results['current1'].astype('float')/65535)*16
        results['pressure'] = (results['current1'].astype('float')/65535)*1100
        if (datetime.datetime.now(results['time'].iloc[0].tzinfo)-results['time'].iloc[0]).total_seconds() > 500: #check if data is current 
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the system is in sleep mode and no recent readings are available.*"
        else:
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: data collection is live*"
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=results['time'],y=results['temp1'].astype('float'),
                                 mode='lines',name='temperature sensor',
                                 hovertemplate='%{y:.1f} C'),secondary_y=False)
        fig.add_trace(go.Scatter(x=results['time'],
                                 y=results['current_scaled'].astype('float'),
                                 mode='lines',
                                 name = 'pressure sensor',
                                 customdata=np.stack((results['pressure'],results['current_scaled']),axis=-1),
                                 hovertemplate= '%{y:.2f} mA<br>Pressure [kPa]:%{customdata[0]:.2f}',
                                 ),secondary_y=True)
        fig.update_yaxes(title_text="Temperature [C]", secondary_y=False)
        fig.update_yaxes(title_text="Current [mA]", secondary_y=True)
    except Exception as e:
        print(e)
        fig=go.Figure()
        last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: internal error.*"
    fig.update_layout(xaxis_title='Time',hovermode = "x unified")
    return fig,last_updated

@callback(
    Output('data-download','data'),
    Input('download-button', 'n_clicks'),
    [State('n_points','value')],
    prevent_initial_call=True
)
def download_data(n,buffer_length):
    try:
        conn =  pymysql.connect(host=config('AWS_SQL_ENDPOINT'), user=config('AWS_SQL_USER'), passwd=config('AWS_SQL_PASSWORD'), port=3306, database='sensors')
        cur = conn.cursor()
        cur.execute('SELECT * FROM watteco_temp_2 ORDER BY timestamp DESC')
        results = cur.fetchmany(buffer_length)
        times = [results[i][0]+datetime.timedelta(hours=2) for i in range(len(results))]
        if (datetime.datetime.now(times[0].tzinfo)-times[0]).total_seconds() > 120: #check if data is current within the last 2 minutes
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is currently recharging its internal buffer; thus the system is in sleep mode and no recent readings are available.*"
        else:
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is powering the sensor and data collection is live*"
        temp1 = [results[i][1] for i in range(len(results))]
        temp2 = [results[i][2] for i in range(len(results))]
        df = pd.DataFrame({'Timestamp':times,'Temperature 1 [C]':temp1,'Temperature 2 [C]':temp2})
        return dcc.send_data_frame(df.to_csv, 'watteco_temp_2_export.csv')
    except Exception as e:
        raise PreventUpdate
if __name__ == '__main__':
    app.run(debug=True)