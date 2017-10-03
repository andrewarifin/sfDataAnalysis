# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
import pandas as pd

from dash.dependencies import Input, Output
from flask import Flask

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
app = dash.Dash(name = __name__, server = server)
app.config.supress_callback_exceptions = True

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.config['suppress_callback_exceptions']=True

df = pd.read_csv('./sfEnergyBenchmarks.csv', thousands=',')

del df['SFPUC Code']
del df['Notes']
del df['Dpt.']
del df['ENERGY STAR Bldg Type']
del df['2013 ENERGY STAR rating ']
del df['2013 Building Area (sq. ft.)']

eui = '2013 Site EUI (kBtu/sq.ft.)'
buildingArea = '2013 Building Area (sq. ft.)'
yearBuilt = 'Year Built'
buildingCategory = 'General Building Category'

yearLabels = [
    '1880-1889',
    '1890-1899',
    '1900-1909',
    '1910-1919',
    '1920-1929',
    '1930-1939',
    '1940-1949',
    '1950-1959',
    '1960-1969',
    '1970-1979',
    '1980-1989',
    '1990-1999',
    '2000-2009',]

colorPalette = [
    '#F09F8A',
    '#EF9EA0',
    '#E2A2B5',
    '#CCA9C5',
    '#AFB2CC',
    '#92B9CA',
    '#7DBFBC',
    '#78C2A7',
    '#85C18E',
    '#9CBE77',
    '#B7B866',
    '#D2AF61',
    '#E9A569',
    '#F89C7B',
]

categories = [
    {'label': 'General', 'value': 'General'},
    {'label': 'Hospitals', 'value': 'Hospitals'},
    {'label': 'Health & Human Services', 'value': 'Health & Human Services'},
    {'label': 'Airport', 'value': 'Airport'},
    {'label': 'Museums and Art', 'value': 'Museums and Art'},
    {'label': 'Recreation Facilities', 'value': 'Recreation Facilities'},
    {'label': 'Public Safety', 'value': 'Public Safety'},
    {'label': 'Convention Centers', 'value': 'Convention Centers'},
    {'label': 'Offices', 'value': 'Offices'},
    {'label': 'Performance Halls', 'value': 'Performance Halls'},
    {'label': 'Libraries', 'value': 'Libraries'},
    {'label': 'Service, Repair, and Storage', 'value': 'Service, Repair, and Storage'},
    {'label': 'Transit Stations', 'value': 'Transit Stations'},
    {'label': 'Education', 'value': 'Education'},
    {'label': 'Parking Garages', 'value': 'Parking Garages'},
]

def generateGeneralGraph():
    meanBuildingCategory_df = df.groupby([buildingCategory]).mean().reset_index().sort_values(eui)

    trace = [
        go.Bar(
            x=meanBuildingCategory_df[buildingCategory],
            y=meanBuildingCategory_df[eui],
            marker=dict(
                color=colorPalette
            )
        )
    ]
    return html.Div([
        dcc.Graph(
            figure={
                'data': trace,
                'layout': go.Layout(
                    title='EUI by Building Category',
                    xaxis=dict(
                        title='Building Category'
                    ),
                    yaxis=dict(
                        title=eui
                    ),
                    margin=go.Margin(b=160)
                )
            },
            id='generalBarGraph'
        )
    ])

def generatePieChart(category):
    category_df = df[df[buildingCategory].isin([category])].head(10)
    labels = category_df['Facility']

    trace = [
        go.Pie(
            labels=labels,
            values=category_df[eui],
            marker=dict(
                colors=colorPalette,
                line=dict(color='#000000', width=1)
            )
        ),
    ]

    return html.Div([
        dcc.Graph(figure={
            'data': trace,
            'layout': go.Layout(
                title='Top 10 EUI for %s' % category,
                showlegend=True,
                legend=go.Legend(
                    x=1,
                    y=1,
                    font=dict(
                        size=8
                    )
                ),
                margin=go.Margin(l=0, r=0, t=60, b=0),
            )
        }, id='pieChart')
    ], className= 'six columns')

def generateCategoryBarGraph(category):
    category_df = df[df[buildingCategory].isin([category])]
    category_df['Facility Type'] = category_df['Facility Type'].str.lower()
    byFacilityType_df = category_df.groupby('Facility Type').mean()
    byCategory = byFacilityType_df.unstack()[eui]
    trace = [
        go.Bar (
            x=byCategory.index,
            y=byCategory,
            marker=dict(
                color=colorPalette
            )
        )
    ]

    return html.Div([
        dcc.Graph(figure={
            'data': trace,
            'layout': go.Layout(
                title='Average EUI by Facility Type',
                xaxis=dict(
                    title='Facility Type'
                ),
                yaxis=dict(
                    title='Average %s' % eui
                ),
            )
        }, id='categoryBarGraph')
    ], className='six columns')

def generateTable(category):
    if (category == 'General'):
        return None
    category_df = df[df[buildingCategory].isin([category])].head(10)
    category_df.sort_values(eui, ascending=False, inplace=True)
    return html.Div([
        html.Table(
            [html.Tr([html.Th(col) for col in category_df.columns])] +

            [html.Tr([
                html.Td(category_df.iloc[i][col]) for col in category_df.columns
            ]) for i in range(0,len(category_df))]
        )
    ], className='six columns')

def generateYearRangeGraph(category):
    if (category == 'General'):
        return None
    category_df = df[df[buildingCategory].isin([category])]
    category_df['Year Renov.'].fillna(category_df[yearBuilt], inplace=True)
    category_df.rename(columns={'Year Renov.': 'Year Built/Renovated'}, inplace=True)
    category_df['year_range'] = pd.cut(category_df['Year Built/Renovated'], range(1880, 2011, 10), right=False, labels=yearLabels)
    byYear_df = category_df.groupby(['year_range']).mean()
    byYear = byYear_df.unstack()[eui]

    div = html.Div([
        dcc.Graph(
            figure = {
                'data': [
                    go.Bar(
                        x=byYear.index,
                        y=byYear,
                        marker=dict(
                            color=colorPalette
                        )
                    )
                ],
                'layout': go.Layout(
                    title='Average EUI by Construction/Renovation Year',
                    xaxis=dict(
                        title='Construction/Renovation Year'
                    ),
                    yaxis=dict(
                        title='Average %s' % eui
                    )
                )
            }, id='lineChart'
        )
    ], className='six columns')

    return div

@app.callback(
    dash.dependencies.Output('pieBarRow', 'children'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def generateGraphs(selectedCategory):
    if (selectedCategory == 'General'):
        return [generateGeneralGraph()]
    return [
        generatePieChart(selectedCategory),
        generateCategoryBarGraph(selectedCategory),
    ]

@app.callback(
    dash.dependencies.Output('yearTableRow', 'children'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def generateTableAndChart(selectedCategory):
    if (selectedCategory == 'General'):
        return None
    return [
        generateYearRangeGraph(selectedCategory),
        generateTable(selectedCategory),
    ]

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options = categories,
        value='General'
    ),
    html.Div(id='pieBarRow', className='row'),
    html.Div(id='yearTableRow', className='row'),
])
