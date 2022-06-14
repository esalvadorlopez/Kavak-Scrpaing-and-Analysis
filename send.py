import pandas as pd
import json
import gspread
from clean import clean

def send():
    gc = gspread.service_account(filename='general-project-352815-e291ea0ea410.json')
    sh = gc.open("cars_comparative_kavak")
    worksheet = sh.worksheet('raw')
    worksheet.update([clean().columns.values.tolist()] + clean().values.tolist())


if __name__ == '__main__':
    send()