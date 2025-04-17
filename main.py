import streamlit as st
import pandas as pd
from data_fetchers.fetch_batter_data import get_today_batters
from data_fetchers.fetch_pitcher_data import get_today_pitchers
from data_fetchers.fetch_weather import get_weather_data
from data_fetchers.fetch_lineups import get_confirmed_lineups
from utils.feature_engineering import build_features
from utils.scoring import predict_home_run_probs
from utils.team_logos import load_team_logo
from utils.sportsbook_odds import fetch_hr_odds

st.set_page_config(page_title="MLB AI HR Prop Bot", layout="wide")

st.title("💣 MLB AI Home Run Projection Bot")
st.caption("Live data + AI-powered projections for today’s top HR hitters")

# ⏳ Load data
with st.spinner("Fetching live MLB data..."):
    batters_df = get_today_batters()
    pitchers_df = get_today_pitchers()
    weather_df = get_weather_data()
    lineups = get_confirmed_lineups()
    hr_odds = fetch_hr_odds()

# ✨ Filter for confirmed lineups (toggle)
confirmed_toggle = st.checkbox("✅ Show only confirmed lineups", value=True)
if confirmed_toggle:
    batters_df = batters_df[batters_df['player_id'].isin(lineups)]

# 🔬 Feature engineering
features = build_features(batters_df, pitchers_df, weather_df)

# 🤖 AI predictions
with st.spinner("Running AI home run projections..."):
    preds_df = predict_home_run_probs(features)

# 🧠 Merge odds and logos
preds_df = preds_df.merge(hr_odds, on='player_id', how='left')
preds_df["Logo"] = preds_df["team"].apply(load_team_logo)

# 📊 Display leaderboard
st.subheader("🏆 Top AI HR Picks Today")
top_n = st.slider("How many top players to show?", 5, 50, 20)

styled_df = preds_df.sort_values("HR_Confidence", ascending=False).head(top_n)

# Columns: Logo | Player | Team | Opponent | Game Time | Best HR Odds | HR Confidence
st.dataframe(
    styled_df[["Logo", "player_name", "team", "opponent", "game_time", "best_odds", "HR_Confidence"]],
    use_container_width=True
)

# 🔁 Refresh
if st.button("🔄 Refresh Projections"):
    st.experimental_rerun()
