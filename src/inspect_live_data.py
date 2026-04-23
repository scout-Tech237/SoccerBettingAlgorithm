import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

fixtures_path = data_folder / "live_fixtures.csv"
odds_path = data_folder / "live_odds.csv"


def main():
    fixtures_df = pd.read_csv(fixtures_path)
    odds_df = pd.read_csv(odds_path)

    print("=" * 70)
    print("LIVE FIXTURES SAMPLE")
    print("=" * 70)
    print(fixtures_df.head(20).to_string(index=False))

    print("\n" + "=" * 70)
    print("LIVE ODDS SAMPLE")
    print("=" * 70)
    print(odds_df.head(20).to_string(index=False))

    print("\n" + "=" * 70)
    print("UNIQUE FIXTURE TEAMS")
    print("=" * 70)
    fixture_teams = sorted(set(fixtures_df["home_team"]).union(set(fixtures_df["away_team"])))
    for team in fixture_teams:
        print(team)

    print("\n" + "=" * 70)
    print("UNIQUE ODDS TEAMS")
    print("=" * 70)
    odds_teams = sorted(set(odds_df["home_team"]).union(set(odds_df["away_team"])))
    for team in odds_teams:
        print(team)


if __name__ == "__main__":
    main()