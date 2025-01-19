import yaml
import requests
from datetime import datetime as DT
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def splash_page():
    weather_data: dict = get_weather()
    hourly = weather_data.get('timelines').get('hourly')[0]
    daily = weather_data.get('timelines').get('daily')[0]
    up_to_date = weather_data.get('timelines').get('minutely')[0]
    weather_values = up_to_date.get('values')
    precip = weather_values.get('precipitationProbability')
    temp = calculate_farenheit(weather_values.get('temperature'))
    time = DT.now().strftime("%I:%M %p")
    return render_template('index.html', temp=temp, rest=str(hourly), rest2=str(daily), precip=precip, time=time)


with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

API_KEY = data["TOMORROW_API"]["KEY"]

def calculate_farenheit(temp: int) -> int:
    return int((temp * 9/5) + 32)

def get_weather():
    url = f"https://api.tomorrow.io/v4/weather/forecast?location=33.1507,-96.8236&apikey={API_KEY}"
    headers = {
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run()