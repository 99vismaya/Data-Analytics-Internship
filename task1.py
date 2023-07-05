# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 12:38:45 2023

@author: Dell
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def download_images(person_name, num_images):
    # Create a directory to store the downloaded images
    save_dir = f"{person_name}_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Encode the person's name for the search query
    encoded_person_name = quote(person_name)

    # Perform a Google Images search for the person
    url = f"https://www.google.com/search?q={encoded_person_name}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all image elements in the page
    image_elements = soup.find_all("img")

    # Download the images
    count = 0
    for img in image_elements:
        if count == num_images:
            break

        # Get the image source URL
        img_url = img["src"]

        try:
            # Send a request to download the image
            img_response = requests.get(img_url)
            img_response.raise_for_status()

            # Save the image to disk
            with open(f"{save_dir}/{count+1}.jpg", "wb") as f:
                f.write(img_response.content)

            print(f"Downloaded image {count+1}/{num_images}")
            count += 1
        except requests.exceptions.HTTPError:
            # Skip if unable to download the image
            continue

    print("Image download completed.")

# Example usage
person_name = input("Enter the person's name: ")
num_images = 50

download_images(person_name, num_images)