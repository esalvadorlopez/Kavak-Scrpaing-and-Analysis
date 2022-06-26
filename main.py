#Importing libraries
from numpy import append
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#Creating URL's
URL = 'https://www.kavak.com'
iso = 'mx'
query_1 = f'estatus-Disponible'
query_2 = f'precio-1000000-max'
page_number = 1


#Selenium
sl_paths = json.load(open('selenium_paths.json', encoding='utf-8'))


#List to save URL's for each page in the search results
urls_to_scrap = []


#Counting number of pages
def _get_number_of_pages():
    try:
        MAIN_PAGE = bs4.BeautifulSoup(requests.get(f'{URL}/{iso}/{query_1}/{query_2}/compra-de-autos').text,'html.parser')
        pages = int(MAIN_PAGE.find('div','results').text.replace('1 de ',''))
    except:
        pages = 60
    return pages


#For each page we save in the pr
# evious list crated
for i in range(0,_get_number_of_pages()):
        final_url = f'{URL}/{iso}/{query_1}/page-{page_number}/{query_2}/compra-de-autos'
        page_number = page_number + 1
        urls_to_scrap.append(final_url)


#Car URI's
car_uris = []


#This function get the urls for each car in the result main page
def _scrap_main_page():
    url_count = 0
    for z in urls_to_scrap:
        try:
            response = requests.get(urls_to_scrap[url_count])
            main_page = bs4.BeautifulSoup(response.text,'html.parser')
            a_labels = main_page.find_all('a',{'class':'card-inner'})
            for label in a_labels:
                car_uris.append(label['href'])
            print(f'Scrapping main page {url_count}')
            url_count += 1
        except Exception as e:
            print(f'ERROR IN PAGE {page_number}')
            print(e)
            pass


#This function get each car information and save it in the gobal variables for the dataframe
def _scrap_cars():
    header_added = False
    counter_cars = 0
    for uri in car_uris:
        try:
            #URL by car
            response_car = requests.get(f'{URL}{uri}',timeout=1000)
            car_deatil_page = bs4.BeautifulSoup(response_car.text,'html.parser')

            #main info
            car_main = car_deatil_page.find('title').text.split('|')
            car_titles = car_main[0]   

            try:       
                car_kms = car_main[1]
            except:        
                car_kms = None

            try:      
                car_prices = car_main[2]
            except:          
                car_prices = None

            #photo
            car_photo = car_deatil_page.find_all('img',{'class':'media'})
            car_photos = car_photo[0]['src']

            #features
            car_features = car_deatil_page.find_all('div',{'class':['feature','feature link']})
            car_features_text = []

            for features in car_features:
                car_features_text.append(features.text) 
            text = ''.join(car_features_text).split('  ')
            count = 0
            keys = []
            values = []
            car_features_dict = {}

            for i in text:
                if not count%2:
                    keys.append(text[count])
                if count%2:
                    values.append(text[count])
                count += 1   
            for x in range(len(keys)):
                car_features_dict[keys[x]] = values[x]

            car_main_features = car_features_dict

            #car url
            car_final_urls = f'{URL}{uri}'

            #Location
            try:
                driver = webdriver.Chrome(executable_path=sl_paths['windows_path'])
                driver.get(f'{URL}{uri}')
                location_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a.feature-value")))
           
                car_locations = location_element.text

            except Exception as e:
                print('Error in car location')
                print(e)
                car_locations = None
                pass

            #City
            try:
                city = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//strong[text()[contains(.,'Ciudad')]]/following::span")))
         
                car_cities = city.text
                driver.quit()

            except Exception as a:
                print(a)
                print('Error getting car city')      
                car_cities = None
                pass
            
            with open('raw_dataset.csv', 'a', encoding='utf-8', newline='') as f:

                if not header_added:     
                    f.write(f'title;km;price;features;car_location;car_city;url;image_link\n')
                    header_added = True

                f.write(f'{car_titles};{car_kms};{car_prices};{car_main_features};{car_locations};{car_cities};{car_final_urls};{car_photos}\n')
            

            print(f'Scrapping car {counter_cars}')
            
            counter_cars += 1

        except Exception as e:
            print(f'ERROR IN {URL}{uri}')
            print(e)
            pass

if __name__ == '__main__':
    _scrap_main_page()
    _scrap_cars()
