import requests
import pandas as pd

API_KEY = "08b01ca094df2346d92227d1682f38ac"  # From user

def get_weather_data():
    # You’d typically match weather to stadiums. For simplicity, mock example here:
    weather_data = {
        "stadium": ["Coors Field", "Fenway Park"],
        "wind_speed": [12, 7],
        "temperature": [75, 62],
        "wind_direction": ["out to center", "left to right"]
    }
    return pd.DataFrame(weather_data)
# Placeholder for fetch_weather.py
