"""Scrapes quotes from the given url.

The url is 'https://quotes.toscrape.com/'.
"""

import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--disable-gpu')

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install(), options=chrome_options)

url = 'https://google.com/'
time.sleep(1000000)
driver.get(url)
