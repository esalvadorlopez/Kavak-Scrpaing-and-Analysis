from numpy import append
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json
import gspread
import pandas as pd

from main import _scrap_main_page
from main import _scrap_cars
from main import _create_dataframe
from clean import clean
from send import send

def run():
    _scrap_main_page()
    _scrap_cars()
    _create_dataframe()
    print('Dataframe Created')
    clean()
    print('Dataframe Cleaned')
    send()
    print('Dataframe Sended!')

if __name__ == '__main__':
    run()
