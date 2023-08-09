# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 19:28:08 2023

@author: Dell
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load your data into a pandas DataFrame
df = pd.read_csv('C:/Users/Dell/Desktop/flipkart_com-ecommerce_sample.csv')  # Replace with your data filename

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Tobacco Consumption Analysis"),

    dcc.Graph(id='state-pie-chart'),
    dcc.Graph(id='gender-bar-chart'),
    dcc.Graph(id='age-group-histogram'),
    dcc.Graph(id='consumption-scatter-plot')
])

# Define callback to update graphs based on user input
@app.callback(
    Output('state-pie-chart', 'figure'),
    Output('gender-bar-chart', 'figure'),
    Output('age-group-histogram', 'figure'),
    Output('consumption-scatter-plot', 'figure'),
    [Input('state-dropdown', 'value')]  # Assuming you have a dropdown to select state
)
def update_graphs(selected_state):
    state_data = df[df['State'] == selected_state]
    
    # Pie chart showing gender distribution
    gender_pie = px.pie(state_data, names='Gender', title=f'Gender Distribution in {selected_state}')
    
    # Bar chart comparing gender-wise consumption
    gender_bar = px.bar(state_data, x='Gender', y='Tobacco Consumers', color='Gender',
                        title=f'Gender-wise Tobacco Consumption in {selected_state}')
    
    # Histogram of age group distribution
    age_histogram = px.histogram(state_data, x='Age Group', title=f'Age Group Distribution in {selected_state}')
    
    # Scatter plot showing consumption amount vs. age
    scatter_plot = px.scatter(state_data, x='Age Group', y='Consumption Amount', color='Gender',
                              title=f'Consumption Amount vs. Age in {selected_state}')
    
    return gender_pie, gender_bar, age_histogram, scatter_plot

if __name__ == '__main__':
    app.run_server(debug=True)
