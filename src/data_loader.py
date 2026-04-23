import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

teams_path = project_root / "data" / "teams.csv"
leagues_path = project_root / "data" / "leagues.csv"


def load_team_stats():
    df = pd.read_csv(teams_path)

    team_dict = {}

    for _, row in df.iterrows():
        team_dict[row["team"]] = {
            "home_goals_scored": row["home_goals_scored"],
            "home_goals_conceded": row["home_goals_conceded"],
            "away_goals_scored": row["away_goals_scored"],
            "away_goals_conceded": row["away_goals_conceded"]
        }

    return team_dict


def load_league_averages():
    df = pd.read_csv(leagues_path)

    league_dict = {}

    for _, row in df.iterrows():
        league_dict[row["league"]] = {
            "home_goals": row["home_goals"],
            "away_goals": row["away_goals"]
        }

    return league_dict