import requests
import pandas as pd

def get_today_pitchers():
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher"
    response = requests.get(url)
    data = response.json()

    pitcher_data = []
    for date in data["dates"]:
        for game in date["games"]:
            for side in ["home", "away"]:
                pitcher = game.get(f"{side}ProbablePitcher")
                if pitcher:
                    pitcher_data.append({
                        "team": game[side]["team"]["abbreviation"],
                        "pitcher_id": pitcher["id"],
                        "pitcher_name": pitcher["fullName"]
                    })
    return pd.DataFrame(pitcher_data)
# Placeholder for fetch_pitcher_data.py
