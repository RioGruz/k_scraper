import streamlit as st 
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

import time
import pandas as pd
import numpy as np

from webdriver_manager.chrome import ChromeDriverManager

import base64
from io import BytesIO

pd.set_option("display.max_rows", 200)

def to_excel(osnovna):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    osnovna.to_excel(writer, index = False, sheet_name='Sheet1')
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(osnovna):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(osnovna)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="nhl.xlsx">Download Excel file</a>'  

def run_premiership():
	st.write("Molimo pričekajte - Download trenutno dostupnih utakmica sa web stranice")
	st.write("Ukoliko su u utakmice LIVE u tijeku ili trenutno nema ponude, dohvaćeni dataframe neće biti sasvim ispravan!")

	web = 'https://www.supersport.hr/sport/dan/30/sport/5/liga/354716' 

	# pozivanje drivera - otvaranje browsera
	driver = webdriver.Chrome(path="/home/appuser/venv/lib/python3.7/site-packages/selenium/webdriver/remote/webdriver.py")
	driver.get(web)

	# prihvaćanje cookiea
	time.sleep(3) 
	accept = driver.find_element_by_xpath('//*[@id="mount-app"]/div/div[3]/div/div/div[2]')
	accept.click()

	# biranje osnovne ponude
	time.sleep(3) 
	accept = driver.find_element_by_xpath('//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[1]')
	accept.click()

	time.sleep(3)

	dfs = pd.read_html(driver.page_source)

	len(dfs)

	def sredjivanje(df):
		df = df.loc[:,['Unnamed: 6', '1', 'X', '2', '1X', 'X2', '12']]
		df.columns = ['dogadjaj', '1', 'X', '2', '1X', 'X2', '12']
		df[['1', 'X', '2', '1X', 'X2', '12']] = df[['1', 'X', '2', '1X', 'X2', '12']].div(100) 
		pd.options.display.float_format = "{:,.2f}".format
		return df

	osnovna = dfs[0]

	osnovna = sredjivanje(osnovna)

	st.write(osnovna)

	st.write("Uspješan dohvat!")

	st.markdown(get_table_download_link(osnovna), unsafe_allow_html=True)


		
