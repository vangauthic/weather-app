import yaml
import openmeteo_requests
import requests_cache
import pytz
from datetime import datetime as DT
from flask import Flask, render_template, request
from retry_requests import retry
from geopy import geocoders
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
gn = geocoders.GeoNames(username="andrewp")
geolocator = Nominatim(user_agent="weather_app")
tf = TimezoneFinder()

app = Flask(__name__) 

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

WMO_CODES = data["WMO"]
STATE_CODES = data["STATE_CODES"]

def give_stats(weather_info: dict):
    temp = int(weather_info.get("temp"))
    wmo = (WMO_CODES[int(weather_info.get("wmo"))]).title()
    lat = weather_info.get("lat")
    lng = weather_info.get("lng")
    location = geolocator.reverse((lat, lng))
    city = location.raw["address"]["city"] + ", " + (STATE_CODES[location.raw["address"]["state"].upper()])

    timezone_str = tf.timezone_at(lat=lat, lng=lng)
    timezone = pytz.timezone(timezone_str)
    time = DT.now(timezone).strftime("%I:%M %p")
    return {"temp": temp, "wmo": wmo, "city": city, "time": time, "lat": lat, "lng": lng}

@app.route('/', methods=['GET', 'POST'])
def splash_page():
    city = "Frisco, TX"
    if request.method == 'POST':
        city = request.form['city']
    if "," not in city:
        city = "Frisco, TX"
    try:
        weather_info = get_weather(city)
    except:
        weather_info = get_weather("Frisco, TX")
    
    try:
        info = give_stats(weather_info)
    except:
        info = give_stats(get_weather("Frisco, TX"))

    return render_template('index.html', temp=info.get('temp'), time=info.get('time'), wmo=info.get('wmo'), city=info.get('city'))

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
    return {"temp": temp, "wmo": wmo, "lng": lng, "lat": lat}

if __name__ == "__main__":
    app.run()