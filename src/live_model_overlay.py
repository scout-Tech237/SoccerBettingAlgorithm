import pandas as pd
from pathlib import Path

from expected_goals import calculate_expected_goals
from poisson_model import build_score_matrix, calculate_market_probabilities
from odds_tools import edge, expected_value

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"


def main():
    path = data_folder / "live_derived_markets.csv"
    df = pd.read_csv(path)

    rows = []

    for match_key, group in df.groupby("match_key"):
        group = group.copy()

        home_team = group["home_team"].iloc[0]
        away_team = group["away_team"].iloc[0]

        # for now, assume all live matches are in Primera Division if Spanish names are found
        # later we will make this automatic from fixture source
        league = "La Liga"

        lambda_home, lambda_away = calculate_expected_goals(home_team, away_team, league)
        score_matrix = build_score_matrix(lambda_home, lambda_away)
        model_probs = calculate_market_probabilities(score_matrix)

        for _, row in group.iterrows():
            market_name = row["market_name"]

            if market_name not in model_probs:
                continue

            model_probability = model_probs[market_name]
            market_probability = row["market_probability"]
            market_odds_est = row["market_odds_est"]

            selection_edge = edge(model_probability, market_probability)
            selection_ev = expected_value(model_probability, market_odds_est)

            rows.append({
                "match_key": match_key,
                "match_date_utc": row["match_date_utc"],
                "home_team": home_team,
                "away_team": away_team,
                "market_name": market_name,
                "market_probability": market_probability,
                "market_odds_est": market_odds_est,
                "model_probability": model_probability,
                "edge": selection_edge,
                "expected_value": selection_ev,
                "lambda_home": lambda_home,
                "lambda_away": lambda_away
            })

    out_df = pd.DataFrame(rows)
    output_path = data_folder / "live_model_vs_market.csv"
    out_df.to_csv(output_path, index=False)

    print(f"Built {len(out_df)} model comparison rows")
    print(f"Saved to: {output_path}")
    print(out_df.head(30).to_string(index=False))


if __name__ == "__main__":
    main()