import requests

def get_confirmed_lineup_names():
    """
    Fetch confirmed MLB lineups and return a list of player names.
    Uses ESPN's public scoreboard API.
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    res = requests.get(url)
    if res.status_code != 200:
        return []

    data = res.json()
    confirmed_names = []

    for event in data.get("events", []):
        competitions = event.get("competitions", [])
        if not competitions:
            continue

        for competitor in competitions[0].get("competitors", []):
            lineup = competitor.get("lineup", {})
            if lineup.get("confirmed", False):
                for player in lineup.get("lineup", []):
                    player_info = player.get("athlete", {})
                    name = player_info.get("displayName")
                    if name:
                        confirmed_names.append(name)

    return confirmed_names
# Placeholder for fetch_lineups.py
