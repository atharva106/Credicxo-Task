# author: Atharva Chalke
# Finished on April 12 2022

#==============================================================================
# Package Import
#==============================================================================

import os
import json
import random
import pathlib
import requests
import pandas as pd
from bs4 import BeautifulSoup

path_dir = pathlib.Path('/Users/atharva/Desktop/Credicxo Task')
os.chdir(path_dir)

pd.options.mode.chained_assignment = None

#==============================================================================
# Package Import
#==============================================================================

def scrape(country, asin):
    url = 'https://www.amazon.' + str(country) + '/dp/' + str(asin)

    agents = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"]

    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding" : "gzip, deflate", 
        "Dnt": "1", 
        'User-Agent' : random.choice(agents)
    }

    r = requests.get(url, headers=headers)

    if int(r.status_code) != 404:
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            title = soup.find('span', {'id' : 'productTitle'}).text.strip()
            img = soup.find('div', {'class' : 'imgTagWrapper'}).find('img')['src']
            price = soup.find('span', {'class' : 'a-price-whole'}).text.strip()+ soup.find('span', {'class' : 'a-price-fraction'}).text.strip() + soup.find('span', {'class' : 'a-price-symbol'}).text.strip()
            
            fb = soup.find('div', {'data-feature-name' : 'featurebullets'}).findAll('li')
            features = [li.text.strip() for li in fb]

            print( {'title' : title, 
                    'img' : img, 
                    'price' : price, 
                    'description' : features})
        except:
            return None
    else:
        print(url, 'not available!')

#=============================================================================
# Working Code
#=============================================================================

df = pd.read_csv('amazon_scraping_sheet.csv')

for i in df.index:
    print(scrape(df['country'][i], df['Asin'][i]))
    print()