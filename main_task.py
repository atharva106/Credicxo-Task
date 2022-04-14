# author: Atharva Chalke
# Finished on April 12 2022

#==============================================================================
# Package Import
#==============================================================================

import os
import time
import json
import pathlib
import warnings
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

warnings.filterwarnings("ignore", category=DeprecationWarning) 

path_dir = pathlib.Path('') # Enter the path to the directory here
os.chdir(path_dir)

pd.options.mode.chained_assignment = None

#==============================================================================
# Package Import
#==============================================================================

options = Options()
# options.add_argument("--headless")

def scrape(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    title = None
    price = None
    description = None
    img = None

    # Get Title
    try:
        title = driver.find_element_by_id('productTitle').text
    except:
        print(url, 'not available')
        return None

    # Get price
    try:
        price = driver.find_element_by_id('price').text
    except:
        pass

    try:
        price = driver.find_element_by_class_name('a-price-whole').text.strip() + driver.find_element_by_class_name('a-price-fraction').text.strip() + driver.find_element_by_class_name('a-price-symbol').text.strip()
    except:
        pass

    # Get description
    try:
        description = driver.find_element_by_id('featurebullets_feature_div').text.strip()
    except:
        pass
    try:
        description = driver.find_element_by_id('bookDescription_feature_div').text.strip()
    except:
        pass

    # Get image url
    try:
        img = driver.find_element_by_id('imgTagWrapperId').find_element_by_tag_name('img').get_attribute('src')
    except:
        pass
    try:
        img = driver.find_element_by_id('img-canvas').find_element_by_tag_name('img').get_attribute('src')
    except:
        pass

    return {'url' : str(url),
            'title' : str(title),
            'price' : str(price),
            'description' : str(description),
            'image' : str(img)}

#=============================================================================
# Working Code
#=============================================================================

df = pd.read_csv('https://raw.githubusercontent.com/atharva106/Credicxo-Task/main/amazon_scraping_sheet.csv')

data = []

for i in df.index:
    url = 'https://www.amazon.' + str(df['country'][i]) + '/dp/' + str(df['Asin'][i])

    product = scrape(url)

    if product != None:
        data.append(product)

with open('products.json', 'w') as out:
    json.dump(data, out)

data = pd.DataFrame(data)
data.to_csv('products.csv', index=False)