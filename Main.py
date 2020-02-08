import os
import sys
import dotenv
import plotly.express as px
import pandas as pd
import requests

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
