import yaml
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from datetime import datetime as DT
from flask import Flask, render_template
from retry_requests import retry
from geopy import geocoders

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
gn = geocoders.GeoNames(username="andrewp")

app = Flask(__name__) 

@app.route('/')
def splash_page():
    weather_info = get_weather("Frisco, TX")
    temp = int(weather_info.get("temp"))
    wmo = weather_info.get("wmo")
    time = DT.now().strftime("%I:%M %p")
    return render_template('index.html', temp=temp, time=time, wmo=wmo)

def get_coords(location: str):
    place, (lat, lng) = gn.geocode(location)
    return place, lat, lng

def get_weather(location: str) -> dict:
    place, lat, lng = get_coords(location)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timeformat": "unixtime",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    temp = response.Current().Variables(0).Value()
    wmo = response.Current().Variables(8).Value()
    i = 0
    while i < 11:
        print(f"{response.Current().Variables(i).Value()} : {str(response.Current().Variables(i))}")
    print(wmo)
    return {"temp": temp, "wmo": wmo}

if __name__ == "__main__":
    app.run()