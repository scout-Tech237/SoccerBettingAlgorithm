import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"


def main():
    merged_path = data_folder / "merged_live_data.csv"
    df = pd.read_csv(merged_path)

    # We only care about H2H market
    df = df[df["market_type"] == "H2H"].copy()

    # Group by match + selection and take BEST odds
    agg_df = (
        df.groupby(
            ["match_key", "selection_name"],
            as_index=False
        )
        .agg({
            "decimal_odds": "max",  # best available price
            "home_team_fixture": "first",
            "away_team_fixture": "first",
            "match_date_utc": "first"
        })
    )

    output_path = data_folder / "aggregated_odds.csv"
    agg_df.to_csv(output_path, index=False)

    print(f"Aggregated rows: {len(agg_df)}")
    print(f"Saved to: {output_path}")
    print(agg_df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()