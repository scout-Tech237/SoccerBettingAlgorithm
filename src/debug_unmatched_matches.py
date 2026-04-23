import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

fixtures_path = data_folder / "live_fixtures.csv"
odds_path = data_folder / "live_odds.csv"


def make_match_key(home_team, away_team):
    return f"{home_team} vs {away_team}"


def main():
    fixtures_df = pd.read_csv(fixtures_path)
    odds_df = pd.read_csv(odds_path)

    fixture_keys = set(
        fixtures_df.apply(lambda row: make_match_key(row["home_team"], row["away_team"]), axis=1)
    )

    odds_keys = set(
        odds_df.apply(lambda row: make_match_key(row["home_team"], row["away_team"]), axis=1)
    )

    only_in_fixtures = sorted(fixture_keys - odds_keys)
    only_in_odds = sorted(odds_keys - fixture_keys)

    print("=" * 70)
    print("ONLY IN FIXTURES")
    print("=" * 70)
    for key in only_in_fixtures[:50]:
        print(key)

    print("\n" + "=" * 70)
    print("ONLY IN ODDS")
    print("=" * 70)
    for key in only_in_odds[:50]:
        print(key)


if __name__ == "__main__":
    main()