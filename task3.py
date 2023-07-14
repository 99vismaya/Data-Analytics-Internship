# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 18:46:00 2023

@author: Dell
"""

import requests
from bs4 import BeautifulSoup
import geopandas as gpd
import matplotlib.pyplot as plt

def scrape_per_capita_income():
    url = 'https://data.gov.in/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'views-table cols-8'})
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:
        columns = row.find_all('td')
        state = columns[0].get_text().strip()
        per_capita_income = float(columns[1].get_text().strip())
        data.append((state, per_capita_income))

    return data

def plot_choropleth(data):
    # Load the shapefile for India's states
    shapefile_path = 'C:/Users/Dell/Downloads/india_administrative_boundaries_state_level.shp'
    india_map = gpd.read_file(shapefile_path)

    # Merge the data with the shapefile based on the state names
    merged_data = india_map.set_index('st_nm').join(
        gpd.GeoDataFrame(data, columns=['state', 'per_capita_income']).set_index('state')
    )

    # Plot the choropleth map
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Per Capita Income in Indian States', fontdict={'fontsize': '16', 'fontweight': 'bold'})

    merged_data.plot(column='per_capita_income', cmap='YlGnBu', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    plt.show()

# Scrape per capita income data
data = scrape_per_capita_income()

# Plot the choropleth map
plot_choropleth(data)
