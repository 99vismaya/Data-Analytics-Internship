# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 19:44:05 2023

@author: Dell
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset (replace 'dataset.csv' with your file)
df = pd.read_csv('dataset.csv')

# Check for missing values
print(df.isnull().sum())

# Drop rows with missing values
df.dropna(inplace=True)

# Summary statistics
print(df.describe())

# Correlation matrix
corr_matrix = df.corr()
print(corr_matrix)

# Histogram of Population
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Population', bins=20)
plt.title('Population Distribution')
plt.xlabel('Population')
plt.ylabel('Frequency')
plt.show()

# Scatter plot of GDP vs Life Expectancy
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='GDP', y='Life Expectancy', hue='Country')
plt.title('GDP vs Life Expectancy')
plt.xlabel('GDP')
plt.ylabel('Life Expectancy')
plt.legend()
plt.show()

# Box plot of CO2 Emissions by Region
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Region', y='CO2 Emissions')
plt.title('CO2 Emissions by Region')
plt.xlabel('Region')
plt.ylabel('CO2 Emissions')
plt.xticks(rotation=45)
plt.show()