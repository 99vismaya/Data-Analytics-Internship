# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 19:36:57 2023

@author: Dell
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('C:/Users/Dell/Desktop/flipkart_com-ecommerce_sample.csv')
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Responsive Dashboard"),
    
    dcc.Graph(id='bar-chart'),
    
    dcc.Graph(id='line-chart')
])

def update_charts(selected_value):
    filtered_df = df[df['Category'] == selected_value]
    
    bar_chart = px.bar(filtered_df, x='Category', y='Value1', title=f'Bar Chart for {selected_value}')
    
    line_chart = px.line(filtered_df, x='Category', y='Value2', title=f'Line Chart for {selected_value}')
    
    return bar_chart, line_chart

app.layout = html.Div([
    html.H1("Responsive Dashboard"),
    
    dcc.Dropdown(
        id='bar-line-dropdown',
        options=[{'label': category, 'value': category} for category in df['Category']],
        value=df['Category'][0]
    ),
    
    dcc.Graph(id='bar-chart'),
    
    dcc.Graph(id='line-chart')
])

if __name__ == '__main__':
    app.run_server(debug=True)






