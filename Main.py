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

#   to be updated when api access fixed (see code above).
global_land_temp_state = pd.read_csv('file_name.csv')

global_land_temp_state.head()

global_land_temp_state.nunique()

global_land_temp_state['Country'].unique()

global_land_temp_state.info()

us_land_temp_state = global_land_temp_state.loc[global_land_temp_state['Country'] == 'United States']

us_land_temp_state.head()

print((us_land_temp_state.isnull().sum()*100)/us_land_temp_state.isnull().count())

#remove white spaces from column names and remove extra column that was added after saving the dataframe to csv.
us_land_temp_state = us_land_temp_state.rename(columns=lambda x: x.strip())

us_land_temp_state.loc[:,'dt'] = pd.to_datetime(us_land_temp_state['dt'])

us_land_temp_state.info()

us_land_temp_state['State'].unique()

us_land_temp_state['State'].nunique()

us_1830_land_temp_state = us_land_temp_state.loc[us_land_temp_state['dt'] >= '1830-01-01']

us_1830_land_temp_state.isnull().sum()*100/us_1830_land_temp_state.isnull().count()

us_1830_land_temp_state2 = us_1830_land_temp_state.interpolate(method='linear')

us_1830_land_temp_state2.isnull().sum()*100/us_1830_land_temp_state2.isnull().count()

us_1830_land_temp_state2['State'] = us_1830_land_temp_state2['State'].map(
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

us_1830_land_temp_state2['State'].unique()

fig = plt.gcf()
fig.set_size_inches(12, 8)

ax = sns.lineplot(x="dt", y="AverageTemperature", hue="State", data=us_1830_land_temp_state2)

#   code for creating a chloropleth map for one month of data (January 2000).

us_land_temp_Jan2000 = us_1830_land_temp_state2.loc[us_1830_land_temp_state2['dt'] == '2000-01-01']

us_land_temp_Jan2000.head()

## Mapping

fig = go.Figure(data=go.Choropleth(
    locations=us_land_temp_Jan2000['State'], # 
    z = us_land_temp_Jan2000['AverageTemperature'].astype(float), #data to be color coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Average Temperature (Celsius) for January 2000",
))

fig.update_layout(
    title_text = 'January 2000 Average Temperature by U.S. State',
    geo_scope='usa', # limite map scope to USA
)

fig.show()
