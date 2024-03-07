from datetime import datetime
import requests
import os
import ipinfo
from flask import jsonify, request
from pprint import pprint
# from geopy.geocoders import Nominatim

API_KEY = "0076ee81a63b89b07f08185f778da75b"

def get_current_weather(city_name):
    request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={city_name}&units=metric'
    weather_data = requests.get(request_url).json()
    # pprint(weather_data)
    return weather_data

def get_forecast_weather(city_name):
    API_URL = "https://api.openweathermap.org/geo/1.0/direct?q="+city_name+"&limit=1&appid="+API_KEY
    data = requests.get(API_URL).json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    city =data[0]['name']
    print(lat,lon,city)
    
    
    url = "https://api.openweathermap.org/data/2.5/forecast?lat="+str(lat)+"&lon="+str(lon)+"&appid="+API_KEY
    
    data1= requests.get(url).json()
    pprint(data1)
    unique_forecast_days = []
    five_days_forecast = []

    for forecast in data1['list']:
        forecast_date = datetime.fromisoformat(forecast['dt_txt']).date()
        if forecast_date not in unique_forecast_days:
            unique_forecast_days.append(forecast_date)
            five_days_forecast.append(forecast)

    forecast_list = []

    for i in range(len(five_days_forecast)):
        fordate = str(five_days_forecast[i]["dt_txt"]).split(" ")[0]
        foricon =  five_days_forecast[i]["weather"][0]["icon"]+"@4x.png"
        fortemp =  round(five_days_forecast[i]["main"]["temp"]-273.15,2)
        forwind = five_days_forecast[i]['wind']["speed"]
        forhumidity = five_days_forecast[i]['main']['humidity']
        
        forecast_list.append({'date':fordate,'icon':foricon,'temp':fortemp,'wind':forwind,'humidity':forhumidity})
    # pprint(forecast_list)
    return forecast_list

def get_city_name():
    access_token = '8fa7f3d134a23c'
    handler = ipinfo.getHandler(access_token)
    ip_address = ""
    try:
        response = requests.get('https://ifconfig.me/ip')
        response.raise_for_status()  # Raise an error for non-200 status codes
        ip_address=response.text.strip()
        details = handler.getDetails(ip_address)
        cityname= details.city
        return cityname
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None
    
if __name__ == "__main__":
    city_name=input("Enter a city name : ")
    # pprint(get_forecast_weather(city_name))
    get_forecast_weather(city_name)