import os
from datetime import datetime
import pandas as pd

def generate_predictions():
    matches = [
        {"league": "EPL", "home_team": "Arsenal", "away_team": "Chelsea", "home_lambda": 1.8, "away_lambda": 0.9},
        {"league": "La Liga", "home_team": "Real Madrid", "away_team": "Sevilla", "home_lambda": 2.0, "away_lambda": 0.8},
        {"league": "Serie A", "home_team": "Inter", "away_team": "Lazio", "home_lambda": 1.7, "away_lambda": 1.0},
    ]

    today = datetime.utcnow().strftime("%Y-%m-%d")
    rows = []

    for m in matches:
        if m["home_lambda"] > m["away_lambda"]:
            pick = "Home Win"
            confidence = round(min(0.5 + (m["home_lambda"] - m["away_lambda"]) / 3, 0.92), 2)
        elif m["away_lambda"] > m["home_lambda"]:
            pick = "Away Win"
            confidence = round(min(0.5 + (m["away_lambda"] - m["home_lambda"]) / 3, 0.92), 2)
        else:
            pick = "Draw"
            confidence = 0.50

        rows.append({
            "prediction_date": today,
            "league": m["league"],
            "home_team": m["home_team"],
            "away_team": m["away_team"],
            "pick": pick,
            "confidence": confidence,
            "home_lambda": m["home_lambda"],
            "away_lambda": m["away_lambda"],
        })

    return pd.DataFrame(rows)

def main():
    os.makedirs("data", exist_ok=True)
    df = generate_predictions()
    df.to_csv("data/predictions_latest.csv", index=False)
    print("Saved predictions to data/predictions_latest.csv")

if __name__ == "__main__":
    main()