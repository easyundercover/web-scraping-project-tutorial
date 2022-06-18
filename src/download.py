import requests 
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
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

#remove the rows in the dataframe that are empty strings or are NaN in the Revenue column.
df['revenue'].replace('', np.nan, inplace=True)
df.dropna(subset = ['revenue'], inplace= True)
print(df)
print(type(df)) #to make sure it's still a dataframe

#convert dataframe into list of tuples
records = df.to_records(index=False)
list_of_tuples = list(records)
print(list_of_tuples)

#connect to sqlite
conn = sqlite3.connect('Tesla.db')
c = conn.cursor()

#create table
#c.execute('''CREATE TABLE teslarevenue
#             (date, revenue)''')

# insert data
c.executemany('INSERT INTO teslarevenue VALUES (?,?)', list_of_tuples)

# save (commit) the changes
conn.commit()

# retrieving data from database
df_rev = pd.read_sql('SELECT * FROM teslarevenue', conn)
print(df_rev)

# create plot
print(df_rev.dtypes)
df_rev['date'] = pd.to_datetime(df_rev['date'])
df_rev['revenue'] = df_rev['revenue'].astype(float)

df_rev.plot('date', 'revenue')
plt.title('Tesla Revenue')
plt.xlabel('Date')
plt.show()
