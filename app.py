import pandas as pd
import streamlit as st

st.set_page_config(page_title="Daily Soccer Predictions", layout="wide")

st.title("⚽ Daily Soccer Predictions")
st.caption("Automatically updated every day")

csv_path = "data/predictions_latest.csv"

try:
    df = pd.read_csv(csv_path)

    st.subheader("Today's Predictions")
    st.dataframe(df, use_container_width=True)

    if "prediction_date" in df.columns and len(df) > 0:
        st.success(f"Latest update: {df['prediction_date'].iloc[0]}")

    if "confidence" in df.columns:
        st.subheader("Top Picks")
        top_df = df.sort_values("confidence", ascending=False).head(10)
        st.dataframe(top_df, use_container_width=True)

except FileNotFoundError:
    st.warning("No predictions file found yet. Run the daily prediction script first.")