import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
reports_folder = project_root / "reports"

backtest_path = reports_folder / "multi_day_backtest.csv"
output_chart_path = reports_folder / "bankroll_curve.png"


def main():
    df = pd.read_csv(backtest_path)

    df = df.dropna(subset=["bankroll_after_bet"]).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Infer starting bankroll from first row
    first_row = df.iloc[0]
    starting_bankroll = first_row["bankroll_after_bet"] - first_row["profit"]

    # Add artificial starting point one day before first bet
    start_date = df["date"].min() - pd.Timedelta(days=1)

    start_row = pd.DataFrame([{
        "date": start_date,
        "bankroll_after_bet": starting_bankroll
    }])

    df = pd.concat([start_row, df[["date", "bankroll_after_bet"]]], ignore_index=True)

    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["bankroll_after_bet"], marker="o")
    plt.title("Bankroll Curve")
    plt.xlabel("Date")
    plt.ylabel("Bankroll")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_chart_path, dpi=300)
    plt.show()

    print(f"Bankroll curve saved to: {output_chart_path}")


if __name__ == "__main__":
    main()