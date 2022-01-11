import streamlit as st 
from PIL import Image

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import numpy as np

from nhl import run_NHL
from premiership import run_premiership

def main():
	slika = Image.open('tesseract_AI_logo.png')
	st.image(slika)

	st.header("SUPERSPORT WEB SCRAPER")
	password = st.text_input("Password", type='password')

	if password != "supersport123":
		st.write("Pogrešan password, pokušajte ponovno!")
		st.stop()
	else: 
		st.success("Uspješan login!")

	meni = ["Početna stranica", "Premiership", "NHL"]
	izbor = st.sidebar.selectbox("Izbor", meni)


	if izbor == "Početna stranica":
		st.subheader("Iz izbornika lijevo odaberite željenu opciju")

	elif izbor == "Premiership":
		run_premiership()
		

	elif izbor == "NHL":
		run_NHL()

	else: 
		st.subheader("Tesseract AI")
		slika = Image.open('tesseract_AI_logo.png')
		st.image(slika)

if __name__ == '__main__':
	main()
