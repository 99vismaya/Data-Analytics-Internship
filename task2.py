# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:38:54 2023

@author: Dell
"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def scrape_mohfw():
    url = 'https://www.mohfw.gov.in/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'table'})
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:
        columns = row.find_all('td')
        state = columns[1].get_text().strip()
        active_cases = int(columns[2].get_text().strip())
        recovered = int(columns[3].get_text().strip())
        deaths = int(columns[4].get_text().strip())
        data.append((state, active_cases, recovered, deaths))

    return data

def scrape_worldometer():
    url = 'https://www.worldometers.info/coronavirus/country/india/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'usa_table_countries_today'})
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:
        columns = row.find_all('td')
        state = columns[1].get_text().strip()
        total_cases = int(columns[2].get_text().strip().replace(',', ''))
        recovered = int(columns[6].get_text().strip().replace(',', ''))
        deaths = int(columns[4].get_text().strip().replace(',', ''))
        data.append((state, total_cases, recovered, deaths))

    return data

def scrape_mygov():
    url = 'https://www.mygov.in/covid-19/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    cards = soup.find_all('div', {'class': 'iblock_text'})
    
    data = []
    for card in cards:
        state = card.find('div', {'class': 'info_label'}).get_text().strip()
        active_cases = int(card.find('div', {'class': 'active-case'}).get_text().strip().replace(',', ''))
        recovered = int(card.find('div', {'class': 'discharge'}).get_text().strip().replace(',', ''))
        deaths = int(card.find('div', {'class': 'death_case'}).get_text().strip().replace(',', ''))
        data.append((state, active_cases, recovered, deaths))

    return data

def plot_chart(data):
    states = [item[0] for item in data]
    active_cases = [item[1] for item in data]
    recovered = [item[2] for item in data]
    deaths = [item[3] for item in data]

    plt.figure(figsize=(12, 6))
    x = range(len(states))
    plt.bar(x, active_cases, width=0.25, label='Active Cases')
    plt.bar(x, recovered, width=0.25, label='Recovered', bottom=active_cases)
    plt.bar(x, deaths, width=0.25, label='Deaths', bottom=[i + j for i, j in zip(active_cases, recovered)])
    plt.xlabel('States')
    plt.ylabel('Cases')
    plt.title('COVID-19 Cases in India by State')
    plt.xticks(x, states, rotation='vertical')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Scrape data from multiple sources
data_mohfw = scrape_mohfw()
data_worldometer = scrape_worldometer()
data_mygov = scrape_mygov()

# Combine the data from all sources
combined_data = []
for i in range(len(data_mohfw)):
    state = data_mohfw[i][0]
    active_cases = data_mohfw[i][1]
    recovered = data_mohfw[i][2]
    deaths = data_mohfw[i][3]
    combined_data.append((state, active_cases, recovered, deaths))

    if i < len(data_worldometer) and data_worldometer[i][0] == state:
        total_cases = data_worldometer[i][1]
        combined_data[i] += (total_cases,)
    
    if i < len(data_mygov) and data_mygov[i][0] == state:
        combined_data[i] += (data_mygov[i][1],)

# Print the combined data
for item in combined_data:
    print(item)

# Plot the chart
plot_chart(combined_data)
