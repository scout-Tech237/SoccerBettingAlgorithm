import pandas as pd
from pathlib import Path
from itertools import combinations

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

TARGET_ODDS_MIN = 1.8
TARGET_ODDS_MAX = 2.2


def main():
    path = data_folder / "live_filtered_picks.csv"
    df = pd.read_csv(path)

    combos = []

    records = df.to_dict("records")

    for leg1, leg2 in combinations(records, 2):
        # reject same match combos
        if leg1["match_key"] == leg2["match_key"]:
            continue

        odds1 = leg1["market_odds_est"]
        odds2 = leg2["market_odds_est"]

        prob1 = leg1["model_probability"]
        prob2 = leg2["model_probability"]

        combined_odds = odds1 * odds2
        combined_probability = prob1 * prob2

        if not (TARGET_ODDS_MIN <= combined_odds <= TARGET_ODDS_MAX):
            continue

        combined_ev = (combined_probability * combined_odds) - 1
        avg_edge = (leg1["edge"] + leg2["edge"]) / 2

        combos.append({
            "leg1": f"{leg1['match_key']} | {leg1['market_name']}",
            "leg2": f"{leg2['match_key']} | {leg2['market_name']}",
            "combined_odds": combined_odds,
            "combined_probability": combined_probability,
            "combined_ev": combined_ev,
            "average_edge": avg_edge
        })

    combo_df = pd.DataFrame(combos)
    output_path = data_folder / "live_combos.csv"

    if combo_df.empty:
        combo_df = pd.DataFrame(columns=[
            "leg1", "leg2", "combined_odds",
            "combined_probability", "combined_ev", "average_edge"
        ])
        combo_df.to_csv(output_path, index=False)

        print("No valid combos found.")
        print("Reason: not enough picks from different matches.")
        print("\nTop single picks instead:\n")

        singles = df.sort_values(
            by=["expected_value", "edge", "model_probability"],
            ascending=False
        )

        print(singles[[
            "match_key",
            "market_name",
            "market_odds_est",
            "model_probability",
            "edge",
            "expected_value"
        ]].to_string(index=False))
        return

    combo_df = combo_df.sort_values(
        by=["combined_ev", "average_edge"],
        ascending=False
    )

    combo_df.to_csv(output_path, index=False)

    print(f"Built {len(combo_df)} combos")
    print(combo_df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()