# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dash.dependencies import Input, Output

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.config['suppress_callback_exceptions']=True

df = pd.read_csv('./sfEnergyBenchmarks.csv', thousands=',')

eui = '2013 Site EUI (kBtu/sq.ft.)'
buildingArea = '2013 Building Area (sq. ft.)'
yearBuilt = 'Year Built'
buildingCategory = 'General Building Category'

meanBuildingCategory_df = df.groupby([buildingCategory]).mean().reset_index().sort_values(eui)

hospital_df = df[df[buildingCategory].isin(['Hospitals'])]
hospital_labels = hospital_df['Facility']

@app.callback (
    dash.dependencies.Output('pie-chart-with-dropdown', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def updatePieChart(selectedCategory):
    if (selectedCategory == 'General'):
        trace = [
            go.Bar(
                x=meanBuildingCategory_df[buildingCategory],
                y=meanBuildingCategory_df[eui],
                name='EUI by Building Category',
            )
        ]
        return {
            'data': trace,
            'id': 'bar-graph',

        }
    category_df = df[df[buildingCategory].isin([selectedCategory])].head(10)
    labels = category_df['Facility']

    trace = [
        go.Pie(labels=labels, values=category_df[eui]),
    ]

    return {
        'data': trace,
        'id': 'pie-chart',
        'layout': go.Layout(
            title=selectedCategory,
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
    }

@app.callback (
    dash.dependencies.Output('table-div', 'children'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def updateTable(selectedCategory):
    if (selectedCategory == 'General'):
        return None
    category_df = df[df[buildingCategory].isin([selectedCategory])].head(10)
    return html.Table(
        [html.Tr([html.Th(col) for col in category_df.columns])] +

        [html.Tr([
            html.Td(category_df.iloc[i][col]) for col in category_df.columns
        ]) for i in range(0,len(category_df))]
    )

@app.callback (
    dash.dependencies.Output('bar-graph-with-dropdown', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def updateBarGraph(selectedCategory):
    if (selectedCategory == 'General' or selectedCategory == 'Hospitals'):
        return {
            'data': [],
            'id': 'facility-chart'
        }
    category_df = df[df[buildingCategory].isin([selectedCategory])]
    byFacilityType_df = category_df.groupby('Facility Type').mean()
    trace = [
        go.Bar (
            x=category_df['Facility Type'],
            y=category_df[eui]
        )
    ]

    return {
        'data': trace,
        'id': 'facility-chart'
    }

@app.callback(
    dash.dependencies.Output('pie-chart-column', 'className'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def updateBarGraphFormating(selectedCategory):
    if (selectedCategory == 'General' or selectedCategory == 'Hospitals'):
        return ''
    return 'six columns'

@app.callback(
    dash.dependencies.Output('bar-graph-with-dropdown', 'style'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def updateBarGraphDisplay(selectedCategory):
    if (selectedCategory == 'General' or selectedCategory == 'Hospitals'):
        return {'display': 'none'}

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options = [
            {'label': 'Select a category', 'value': 'General'},
            {'label': 'Hospitals', 'value': 'Hospitals'},
            {'label': 'Health & Human Services', 'value': 'Health & Human Services'},
            {'label': 'Museums and Art', 'value': 'Museums and Art'},
            {'label': 'Recreation Facilities', 'value': 'Recreation Facilities'},
            {'label': 'Education', 'value': 'Education'},
        ],
        value='General'
    ),
    html.Div([
        html.Div([
            dcc.Graph(id='pie-chart-with-dropdown'),
        ], id='pie-chart-column'),
        html.Div([
            dcc.Graph(id='bar-graph-with-dropdown'),
        ], className='six columns'),
    ]),
    html.Div(id='table-div')
    # dcc.Graph(
    #     figure=go.Figure(
    #         data=[
    #             go.Bar(
    #                 x=meanBuildingCategory_df[buildingCategory],
    #                 y=meanBuildingCategory_df[eui],
    #                 name='EUI by Building Category',
    #                 marker=go.Marker(
    #                     color='rgb(55, 83, 109)'
    #                 )
    #             )
    #         ],
            # layout=go.Layout(
            #     title='EUI by Building Category',
            #     showlegend=True,
            #     legend=go.Legend(
            #         x=0,
            #         y=1.0
            #     ),
            #     margin=go.Margin(l=40, r=0, t=40, b=30)
            # )
    #     ),
    #
    #     id='my-graph'
    # ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
