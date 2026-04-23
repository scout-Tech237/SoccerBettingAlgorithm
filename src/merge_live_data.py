import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"


def make_match_key(home_team, away_team):
    return f"{home_team} vs {away_team}"


def main():
    fixtures_path = data_folder / "live_fixtures.csv"
    odds_path = data_folder / "live_odds.csv"

    fixtures_df = pd.read_csv(fixtures_path)
    odds_df = pd.read_csv(odds_path)

    fixtures_df["match_key"] = fixtures_df.apply(
        lambda row: make_match_key(row["home_team"], row["away_team"]),
        axis=1
    )

    odds_df["match_key"] = odds_df.apply(
        lambda row: make_match_key(row["home_team"], row["away_team"]),
        axis=1
    )

    print("=" * 70)
    print("FIXTURE MATCH KEYS")
    print("=" * 70)
    print(fixtures_df["match_key"].drop_duplicates().to_string(index=False))

    print("\n" + "=" * 70)
    print("ODDS MATCH KEYS")
    print("=" * 70)
    print(odds_df["match_key"].drop_duplicates().to_string(index=False))

    merged = fixtures_df.merge(
        odds_df,
        on="match_key",
        how="inner",
        suffixes=("_fixture", "_odds")
    )

    output_path = data_folder / "merged_live_data.csv"
    merged.to_csv(output_path, index=False)

    print("\n" + "=" * 70)
    print(f"Merged rows: {len(merged)}")
    print(f"Saved merged file to: {output_path}")

    if len(merged) > 0:
        print(merged.head(20).to_string(index=False))
    else:
        print("Still no matches. Compare the printed match keys above.")


if __name__ == "__main__":
    main()