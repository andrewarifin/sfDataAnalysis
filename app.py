# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm


df = pd.read_csv('./sfEnergyBenchmarks.csv', thousands=',')

eui = '2013 Site EUI (kBtu/sq.ft.)'
buildingArea = '2013 Building Area (sq. ft.)'
yearBuilt = 'Year Built'
buildingCategory = 'General Building Category'

meanBuildingCategory_df = df.groupby([buildingCategory]).mean().reset_index().sort_values(eui)

app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=meanBuildingCategory_df[buildingCategory],
                    y=meanBuildingCategory_df[eui],
                    name='EUI by Building Category',
                    marker=go.Marker(
                        color='rgb(55, 83, 109)'
                    )
                )
            ],
            layout=go.Layout(
                title='EUI by Building Category',
                showlegend=True,
                legend=go.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.Margin(l=40, r=0, t=40, b=30)
            )
        ),

        id='my-graph'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
