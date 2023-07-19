# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 22:34:34 2023

@author: Dell
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset from the CSV file
df = pd.read_csv('C:/Users/Dell/Desktop/business_data.csv')

# Replace missing contact numbers and website URLs with 'NA'
df['Contact Number'].fillna('NA', inplace=True)
df['Website URL'].fillna('NA', inplace=True)

# Group the data by state and count the number of websites
website_counts = df[df['Website URL'] != 'NA'].groupby('Location')['Website URL'].count().reset_index()
website_counts.columns = ['State', 'Website Count']

# Sort the states by the number of websites in descending order
website_counts = website_counts.sort_values(by='Website Count', ascending=False)

# Create a bar chart to compare the number of websites by state
plt.figure(figsize=(12, 6))
sns.barplot(x='State', y='Website Count', data=website_counts, palette='viridis')
plt.xlabel('State')
plt.ylabel('Website Count')
plt.title('Number of Websites by State')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()