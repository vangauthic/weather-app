import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from geopy import geocoders

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
gn = geocoders.GeoNames(username="andrewp")

def get_coords(location: str):
    place, (lat, lng) = gn.geocode(location)
    return place, lat, lng

def get_weather(lat: float, lng: float):
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
    
if __name__ == "__main__":
    place, lat, lng = get_coords("Frisco, TX")
    get_weather(lat, lng)