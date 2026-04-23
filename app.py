import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Soccer Betting Model", layout="wide")

project_root = Path(__file__).resolve().parent
data_folder = project_root / "data"

st.title("⚽ Live Soccer Betting Model")

picks_path = data_folder / "live_filtered_picks.csv"
combo_path = data_folder / "live_combos.csv"

st.subheader("🔥 Today's Best Picks")

if not picks_path.exists():
    st.warning("No picks available. Run the live pipeline first.")
else:
    df = pd.read_csv(picks_path)

    if df.empty:
        st.info("No strong picks today.")
    else:
        st.dataframe(df, use_container_width=True)

        best = df.sort_values(by="expected_value", ascending=False).iloc[0]

        st.subheader("🏆 Top Single Pick")
        st.markdown(f"""
### {best['match_key']}

**Market:** {best['market_name']}  
**Model Probability:** {best['model_probability']:.3f}  
**Market Probability:** {best['market_probability']:.3f}  
**Edge:** {best['edge']:.3f}  
**Expected Value:** {best['expected_value']:.3f}  
**Expected Odds:** {best['market_odds_est']:.3f}  
**Expected Goals:** {best['home_team']} {best['lambda_home']:.3f} - {best['lambda_away']:.3f} {best['away_team']}
""")

st.subheader("🎯 Best Combos (~2.0 Odds)")

if not combo_path.exists():
    st.warning("No combo file found yet. Run: python src/live_combo_builder.py")
else:
    combo_df = pd.read_csv(combo_path)

    if combo_df.empty:
        st.info("No valid combos today. Not enough picks from different matches.")
    else:
        st.dataframe(combo_df, use_container_width=True)

        best_combo = combo_df.sort_values(by="combined_ev", ascending=False).iloc[0]

        st.subheader("🔥 Best Combo")
        st.markdown(f"""
### Combo Recommendation

**Leg 1:** {best_combo['leg1']}  
**Leg 2:** {best_combo['leg2']}  

**Combined Odds:** {best_combo['combined_odds']:.2f}  
**Combined Probability:** {best_combo['combined_probability']:.3f}  
**Combined EV:** {best_combo['combined_ev']:.3f}  
**Average Edge:** {best_combo['average_edge']:.3f}
""")