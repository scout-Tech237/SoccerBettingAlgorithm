import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

MIN_EDGE = 0.03
MIN_EV = 0.02
MIN_MODEL_PROBABILITY = 0.55

ALLOWED_MARKETS = ["1X", "X2", "HOME_DNB", "AWAY_DNB"]


def main():
    path = data_folder / "live_model_vs_market.csv"
    df = pd.read_csv(path)

    filtered = df[
        (df["market_name"].isin(ALLOWED_MARKETS)) &
        (df["edge"] >= MIN_EDGE) &
        (df["expected_value"] >= MIN_EV) &
        (df["model_probability"] >= MIN_MODEL_PROBABILITY)
    ].copy()

    filtered = filtered.sort_values(
        by=["expected_value", "edge", "model_probability"],
        ascending=False
    )

    output_path = data_folder / "live_filtered_picks.csv"
    filtered.to_csv(output_path, index=False)

    print(f"Filtered picks: {len(filtered)}")
    print(f"Saved to: {output_path}")
    print(filtered.to_string(index=False))


if __name__ == "__main__":
    main()