import os
import sys
import dotenv
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import datetime
from datetime import datetime

# settings.py
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), './.config/.env')
load_dotenv(dotenv_path)

# functions
# def get_apikey(email=None, passwd=None):
#     if email == None or passwd == None:
#         email = input("enter your email: ")
#         passwd = input("enter your password: ")

#     url = "https://app.climate.azavea.com?email={email}&password={passwd}"
#     payload = {}
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)

#     # print(response.cookies.get_dict())
#     #  # doesn't quite work


api_key = os.getenv("CLIMATE_API_KEY")
user_email = os.getenv("CLIMATE_EMAIL")
user_passwd = os.getenv("CLIMATE_PASSWORD")
if api_key == None:
    pass
    # api_key = get_apikey(user_email, user_passwd)
print(api_key)


fig = px.imshow([[1, 20, 30],
                 [20, 1, 60],
                 [30, 60, 1]])
fig.show()

#   code for prepping climate data for mapping.

#cleaning dataset

#take a look at the data. look at top 5 rows, the data types & size of dataset, and the number of unique values of each variable.
print('Global land temperature dataframe:')
display(global_land_temp.head())
print('\n')
print(global_land_temp.info(), '\n')
print('Number of unique values of each variable:')
print(global_land_temp.nunique(), '\n')

#look at the countries included in the dataset.
print('Countries in the dataset:')
print(global_land_temp['Country'].unique(), '\n')

#create a new dataframe from a subset of the complete dataframe. return the percentage of null values for each variable.
us_land_temp = global_land_temp.loc[global_land_temp['Country'] == 'United States']
print('Percentage null values for us_land_temp dataframe:')
print((us_land_temp.isnull().sum()*100)/us_land_temp.isnull().count(), '\n')

#remove white spaces from column names and rename two columns.
us_land_temp = us_land_temp.rename(columns=lambda x: x.strip())
us_land_temp = us_land_temp.rename(columns={'dt':'Date', 'AverageTemperature':'Average Temperature'})

#look at the u.s. states and territories in the data set.
print('States and territories in the dataset:')
print(us_land_temp['State'].unique(), '\n')

#change State values to align with plot.ly basemap's state names.
us_land_temp['State'] = us_land_temp['State'].map(
    {'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District Of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia (State)': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'})

#convert date column to datetime type in order to subset by date.
us_land_temp.loc[:,'Date'] = pd.to_datetime(us_land_temp['Date'])

#subset the dataframe to include dates when there is less missing data for all states. then check for null values.
us_land_temp_post1850 = us_land_temp.loc[us_land_temp['Date'] >= '1850-01-01']
print('Percentage of null values for us_land_temp_post1850:')
print(us_land_temp_post1850.isnull().sum()*100/us_land_temp_post1850.isnull().count(), '\n')

#fill null values
us_land_temp_post1850_2 = us_land_temp_post1850.interpolate(method='linear')

#extract month and year from 'Date' and then check the dataframe again.
us_land_temp_post1850_2['month'] = us_land_temp_post1850_2[['Date']].apply(lambda x: (x['Date'].month), axis=1)
us_land_temp_post1850_2['year'] = us_land_temp_post1850_2[['Date']].apply(lambda x: (x['Date'].year), axis=1)
print('US land temperature after 1850 dataframe:')
display(us_land_temp_post1850_2.head())
print(us_land_temp_post1850_2.info())

#subset data to include january average temperatures only.
january_us_land_temp_post1850 = us_land_temp_post1850_2.loc[us_land_temp_post1850_2['month'] == 1]

#sort rows based on timestamp and then convert 'Date' to a string. this code was needed to work around an error.
#see https://github.com/plotly/plotly.py/issues/1737 for details.
january_us_land_temp_post1850 = january_us_land_temp_post1850.sort_values(by='Date') 
january_us_land_temp_post1850['Date'] = january_us_land_temp_post1850.Date.apply(lambda x: x.date()).apply(str)

#subset data to include july average temperatures only.
july_us_land_temp_post1850 = us_land_temp_post1850_2.loc[us_land_temp_post1850_2['month'] == 7]

#sort rows based on timestamp and then convert 'Date' to a string. this code was needed to work around an error.
#see https://github.com/plotly/plotly.py/issues/1737 for details.
july_us_land_temp_post1850 = july_us_land_temp_post1850.sort_values(by='Date') 
july_us_land_temp_post1850['Date'] = july_us_land_temp_post1850.Date.apply(lambda x: x.date()).apply(str)

#   creating chloropleth maps

#created animated map for the month of january for data from 1850 through 2013 using plot.ly express.
fig_january = px.choropleth(
    january_us_land_temp_post1850,
    locations='State', 
    color='Average Temperature',
    color_continuous_scale=px.colors.diverging.Spectral_r,
    locationmode='USA-states', 
    scope='usa',
    animation_frame='Date',
    title='Average Monthly Temperature (C): January 1850 - 2013')
fig_january.show()

#created animated map for the month of july for data from 1850 through 2013 using plot.ly express.
fig_july = px.choropleth(
    july_us_land_temp_post1850,
    locations='State', 
    color='Average Temperature',
    color_continuous_scale=px.colors.diverging.Spectral_r,
    locationmode='USA-states', 
    scope='usa',
    animation_frame='Date',
    title='Average Monthly Temperature (C): July 1850 - 2013')
fig_july.show()
