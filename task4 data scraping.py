# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 22:37:21 2023

@author: Dell
"""

import csv
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import googleapiclient.discovery

# Set up credentials and API service
credentials = service_account.Credentials.from_service_account_file('path/to/service_account_credentials.json')
scopes = ['https://www.googleapis.com/auth/business.manage']
credentials = credentials.with_scopes(scopes)
if not credentials.valid:
    credentials.refresh(Request())

service = googleapiclient.discovery.build('mybusiness', 'v4', credentials=credentials)

# Fetch business listings
response = service.accounts().list().execute()
accounts = response.get('accounts', [])

# Prepare CSV file
csv_file_path = 'business_listings.csv'
fieldnames = ['Name', 'Contact', 'Address', 'Website']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for account in accounts:
        locations = service.accounts().locations().list(parent=account['name']).execute()
        for location in locations.get('locations', []):
            name = location['locationName']
            contact = location.get('phoneNumbers', ['NA'])[0].get('phoneNumber', 'NA')
            address = location.get('address', {}).get('addressLines', ['NA'])
            website = location.get('websiteUrl', 'NA')

            writer.writerow({'Name': name, 'Contact': contact, 'Address': address, 'Website': website})

print('Business listings saved to CSV file:', csv_file_path)