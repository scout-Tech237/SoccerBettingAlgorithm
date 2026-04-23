import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"


def main():
    path = data_folder / "aggregated_odds.csv"
    df = pd.read_csv(path)

    # Convert odds → implied probability
    df["implied_prob"] = 1 / df["decimal_odds"]

    # Normalize per match (remove bookmaker margin)
    df["norm_prob"] = df.groupby("match_key")["implied_prob"].transform(
        lambda x: x / x.sum()
    )

    output_path = data_folder / "live_probabilities.csv"
    df.to_csv(output_path, index=False)

    print("Built probabilities:")
    print(df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()