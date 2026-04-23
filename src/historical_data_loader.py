import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

matches_path = project_root / "data" / "historical_matches.csv"
odds_path = project_root / "data" / "historical_odds.csv"
results_path = project_root / "data" / "historical_results.csv"


def load_historical_matches():
    return pd.read_csv(matches_path)


def load_historical_odds():
    return pd.read_csv(odds_path)


def load_historical_results():
    return pd.read_csv(results_path)