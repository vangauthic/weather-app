import yaml
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def splash_page():
    weather_data: dict = get_weather()
    up_to_date = weather_data.get('timelines').get('minutely')[0]
    weather_values = up_to_date.get('values')
    temp = calculate_farenheit(weather_values.get('temperature'))
    return render_template('index.html', temp=temp)


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