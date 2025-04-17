import requests
import pandas as pd
from datetime import datetime

def get_today_batters():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=team,linescore,game(content(media(epg)))"

    response = requests.get(url)
    data = response.json()

    game_ids = [game['gamePk'] for date in data['dates'] for game in date['games']]
    batters = []

    for game_id in game_ids:
        try:
            lineup_url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
            r = requests.get(lineup_url).json()
            for team_key in ['home', 'away']:
                players = r['teams'][team_key]['players']
                for pid, info in players.items():
                    stats = info.get('stats', {}).get('batting', {})
                    if stats and stats.get('atBats', 0) > 0:
                        batters.append({
                            'player_id': info['person']['id'],
                            'player_name': info['person']['fullName'],
                            'team': r['teams'][team_key]['team']['abbreviation'],
                            'opponent': r['teams']['away' if team_key == 'home' else 'home']['team']['abbreviation'],
                            'game_time': r['info'][0]['value'],
                        })
        except:
            continue

    return pd.DataFrame(batters)
