# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
import random
from time import gmtime, strftime
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='InnSight'),

    html.Div(children='''
        Zipcode:
    '''),

    html.Div([
        html.Div(dcc.Input(id='input-box', type='text')),
        html.Button('Submit', id='button'),
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='average-price'
                    )
                ], className='six columns'),
                html.Div([
                    dcc.Graph(
                        id='average-price2'
                    )
                ], className='six columns'),
            ], className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='distribution'
                    )
                ], className='six columns'),
                html.Div([
                    dcc.Graph(
                        id='distribution2'
                    )
                ], className='six columns'),
            ], className='row')
        ], className='nine columns'),
        html.Div([
            dash_table.DataTable(
                id='price-event',
                columns=[{"name": "Time", "id": "time"}, {"name": "Price", "id": "price"}],
            )
        ], className='three columns'),
    ], className='row'),
])


@app.callback(
    dash.dependencies.Output('average-price', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(_, value):
    return {'data': [get_average_price(value)],
            'layout': {'title': 'Historical Price Trend'}}

@app.callback(
    dash.dependencies.Output('average-price2', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(_, value):
    return {'data': [get_seasonality(value)],
            'layout': {'title': 'Seasonality'}}


@app.callback(
    dash.dependencies.Output('distribution', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(_, value):
    return {'data': [get_property_type(value)],
            'layout': {'title': 'Property Type'}}


@app.callback(
    dash.dependencies.Output('distribution2', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(_, value):
    return {'data': [get_bedroom_type(value)],
            'layout': {'title': 'Room Type'}}


@app.callback(
    dash.dependencies.Output('price-event', 'data'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(_, value):
    return get_price_event(value)


def read_data_from_db(database, sql):
    try:
        connection = psycopg2.connect(user=config['DEFAULT']['DB_USER'],
                                      password=config['DEFAULT']['DB_PASSWORD'],
                                      host=config['DEFAULT']['POSTGRESQL_IP'],
                                      port=config['DEFAULT']['POSTGRESQL_PORT'],
                                      database=database)
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        return records
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def get_bedroom_type(zipcode):
    if zipcode is None:
        # return empty dict
        return {'x': [], 'y': [], 'type': 'bar', 'name': 'Price'}

    rows = read_data_from_db('price_insight_db',
                             "select * from result_room_type_distribution_san_francisco where zipcode = '%s' order by bedrooms" % zipcode)

    dict_data = {'x': [], 'y': [], 'type': 'bar', 'name': 'Price'}
    for row in rows:
        dict_data['x'].append(str(row[1]).split(' ')[0])
        dict_data['y'].append(str(row[2]))

    return dict_data


def get_property_type(zipcode):
    if zipcode is None:
        # return empty dict
        return {'x': [], 'y': [], 'type': 'bar', 'name': 'Price'}

    rows = read_data_from_db('price_insight_db',
                             "select * from result_rental_type_distribution_san_francisco where zipcode = '%s' and count > 5" % zipcode)

    dict_data = {'x': [], 'y': [], 'type': 'bar', 'name': 'Price'}
    for row in rows:
        dict_data['x'].append(str(row[1]).split(' ')[0])
        dict_data['y'].append(str(row[2]))

    return dict_data


def get_seasonality(zipcode):
    if zipcode is None:
        # return empty dict
        return {'x': [], 'y': [], 'type': 'bar', 'name': 'Price'}

    rows = read_data_from_db('price_insight_db',
                             "select * from seasonality_san_francisco where zipcode = '%s' order by month" % zipcode)

    dict_data = {'x': [], 'y': [], 'type': 'bar', 'name': 'Price'}
    for row in rows:
        dict_data['x'].append(str(row[1]).split(' ')[0])
        dict_data['y'].append(str(row[2]))

    return dict_data


def get_average_price(zipcode):
    if zipcode is None:
        # return empty dict
        return go.Scatter(x=[], y=[], mode='lines', name='Price')

    rows = read_data_from_db('price_insight_db',
                             "select * from trend_by_zipcode_sf where zipcode = '%s' order by timestamp" % zipcode)

    x = []
    y = []
    for row in rows:
        x.append(str(row[1]).split(' ')[0])
        y.append(str(row[2]))

    return go.Scatter(x=x, y=y, mode='lines', name='Price')


curtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())


def get_price_event(zipcode):
    if zipcode is None:
        # return empty dict
        return []
    return [{'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 600)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time': curtime, 'price': random.randint(200, 500)},
            {'time':'2019-02-06 01:45:13', 'price': random.randint(200, 500)},
            {'time':'2019-02-06 03:45:25', 'price': random.randint(200, 500)},
            {'time':'2019-02-06 08:45:46', 'price': random.randint(200, 500)},
            {'time':'2019-02-06 08:09:45', 'price': random.randint(200, 500)}]

    rows = read_data_from_db('price_insight_db',
                             "select * from zipcode_stats where zipcode = '%s' order by timestamp" % zipcode)

    data = []
    for row in rows:
        data.append({'time': str(row[1]).split(' ')[0], 'price': str(row[2])})

    return data


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=80)
