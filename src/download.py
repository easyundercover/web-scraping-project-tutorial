import requests 
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data = requests.get(url).text
#print(html_data) just to check if it worked

result = BeautifulSoup(html_data, "html.parser")
tables = result.find_all("table") #will look for every table

#loops through every table looking for Tesla Quarterly Revenue
for index, table in enumerate(tables):
    if "Tesla Quarterly Revenue" in str(table):
        my_index = index
print(my_index) #prints index 1 = table 2

df = pd.DataFrame(columns = ['date', 'revenue']) #creates empty dataframe

for row in tables[my_index].tbody.find_all('tr'): #looks for every tr(table row)
    col = row.find_all('td')
    if col != "":
        fecha = col[0].text
        ingreso = col[1].text.replace("$", "").replace(",", "")
        df = df.append({'date': fecha, 'revenue': ingreso}, ignore_index=True)
print(df)
