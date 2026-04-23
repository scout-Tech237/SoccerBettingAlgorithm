import pandas as pd
from pathlib import Path

from fetch_live_fixtures import fetch_all_live_fixtures
from fetch_live_odds import fetch_all_live_odds

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"
data_folder.mkdir(exist_ok=True)


def main():
    fixtures = fetch_all_live_fixtures()
    odds = fetch_all_live_odds()

    fixtures_df = pd.DataFrame(fixtures)
    odds_df = pd.DataFrame(odds)

    fixtures_path = data_folder / "live_fixtures.csv"
    odds_path = data_folder / "live_odds.csv"

    fixtures_df.to_csv(fixtures_path, index=False)
    odds_df.to_csv(odds_path, index=False)

    print(f"Saved fixtures to {fixtures_path}")
    print(f"Saved odds to {odds_path}")


if __name__ == "__main__":
    main()