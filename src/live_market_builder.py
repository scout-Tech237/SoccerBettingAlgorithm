import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"


def main():
    path = data_folder / "live_probabilities.csv"
    df = pd.read_csv(path)

    rows = []

    for match_key, group in df.groupby("match_key"):
        group = group.copy()

        home_team = group["home_team_fixture"].iloc[0]
        away_team = group["away_team_fixture"].iloc[0]
        match_date_utc = group["match_date_utc"].iloc[0]

        probs = {}
        odds = {}

        for _, row in group.iterrows():
            selection = row["selection_name"]

            if selection == home_team:
                probs["HOME_WIN"] = row["norm_prob"]
                odds["HOME_WIN"] = row["decimal_odds"]

            elif selection == away_team:
                probs["AWAY_WIN"] = row["norm_prob"]
                odds["AWAY_WIN"] = row["decimal_odds"]

            elif selection == "Draw":
                probs["DRAW"] = row["norm_prob"]
                odds["DRAW"] = row["decimal_odds"]

        if not all(k in probs for k in ["HOME_WIN", "DRAW", "AWAY_WIN"]):
            continue

        # Derived markets
        probs["1X"] = probs["HOME_WIN"] + probs["DRAW"]
        probs["X2"] = probs["DRAW"] + probs["AWAY_WIN"]
        probs["12"] = probs["HOME_WIN"] + probs["AWAY_WIN"]

        if (1 - probs["DRAW"]) > 0:
            probs["HOME_DNB"] = probs["HOME_WIN"] / (1 - probs["DRAW"])
            probs["AWAY_DNB"] = probs["AWAY_WIN"] / (1 - probs["DRAW"])
        else:
            probs["HOME_DNB"] = 0.0
            probs["AWAY_DNB"] = 0.0

        # Estimate odds for derived markets using probabilities
        odds["1X"] = 1 / probs["1X"] if probs["1X"] > 0 else None
        odds["X2"] = 1 / probs["X2"] if probs["X2"] > 0 else None
        odds["12"] = 1 / probs["12"] if probs["12"] > 0 else None
        odds["HOME_DNB"] = 1 / probs["HOME_DNB"] if probs["HOME_DNB"] > 0 else None
        odds["AWAY_DNB"] = 1 / probs["AWAY_DNB"] if probs["AWAY_DNB"] > 0 else None

        for market_name in ["HOME_WIN", "DRAW", "AWAY_WIN", "1X", "X2", "12", "HOME_DNB", "AWAY_DNB"]:
            rows.append({
                "match_key": match_key,
                "match_date_utc": match_date_utc,
                "home_team": home_team,
                "away_team": away_team,
                "market_name": market_name,
                "market_probability": probs[market_name],
                "market_odds_est": odds[market_name]
            })

    out_df = pd.DataFrame(rows)
    output_path = data_folder / "live_derived_markets.csv"
    out_df.to_csv(output_path, index=False)

    print(f"Built {len(out_df)} derived market rows")
    print(f"Saved to: {output_path}")
    print(out_df.head(30).to_string(index=False))


if __name__ == "__main__":
    main()