# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 19:48:27 2023

@author: Dell
"""

import requests
from bs4 import BeautifulSoup

url = 'https://www.findeasy.in/tobacco-use-among-adults-in-india/'  # Replace with the URL of the webpage containing the table
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')  # Use appropriate tag, class, or attributes to locate the table

import pandas as pd

table_data = []
for row in table.find_all('tr'):
    row_data = []
    for cell in row.find_all(['th', 'td']):
        row_data.append(cell.get_text(strip=True))
    table_data.append(row_data)

df = pd.DataFrame(table_data[1:], columns=table_data[0])
df.to_csv('table_data.csv', index=False)

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load the data into a pandas DataFrame
df = pd.read_csv('C:/Users/Dell/Desktop/tobacco_consumption_data.csv')  # Replace with the actual filename

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("State-wise Comparison of Male and Female Tobacco Consumers"),
    
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': state, 'value': state} for state in df['State'].unique()],
        value=df['State'].unique()[0],
        multi=False
    ),

    dcc.Graph(id='tobacco-comparison-graph')
])

# Define the callback to update the graph based on the selected state
@app.callback(
    Output('tobacco-comparison-graph', 'figure'),
    [Input('state-dropdown', 'value')]
)
def update_graph(selected_state):
    filtered_df = df[df['State'] == selected_state]
    
    fig = px.bar(filtered_df, x='Gender', y='Tobacco Consumers', color='Gender',
                 labels={'Tobacco Consumers': 'Number of Tobacco Consumers'},
                 title=f"Tobacco Consumers in {selected_state}")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
