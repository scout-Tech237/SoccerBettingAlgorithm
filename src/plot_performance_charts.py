import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
reports_folder = project_root / "reports"

backtest_path = reports_folder / "multi_day_backtest.csv"
profit_chart_path = reports_folder / "cumulative_profit_curve.png"
drawdown_chart_path = reports_folder / "drawdown_curve.png"


def main():
    df = pd.read_csv(backtest_path)

    df = df.dropna(subset=["bankroll_after_bet"]).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    first_row = df.iloc[0]
    starting_bankroll = first_row["bankroll_after_bet"] - first_row["profit"]

    df["cumulative_profit"] = df["bankroll_after_bet"] - starting_bankroll
    df["drawdown"] = pd.to_numeric(df["drawdown"], errors="coerce")

    start_date = df["date"].min() - pd.Timedelta(days=1)

    start_row = pd.DataFrame([{
        "date": start_date,
        "cumulative_profit": 0.0,
        "drawdown": 0.0
    }])

    # Profit chart dataframe
    profit_df = pd.concat(
        [start_row[["date", "cumulative_profit"]], df[["date", "cumulative_profit"]]],
        ignore_index=True
    )

    # Drawdown chart dataframe
    drawdown_df = pd.concat(
        [start_row[["date", "drawdown"]], df[["date", "drawdown"]]],
        ignore_index=True
    )

    # ---------------------------
    # Plot 1: Cumulative Profit
    # ---------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(profit_df["date"], profit_df["cumulative_profit"], marker="o")
    plt.title("Cumulative Profit Curve")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Profit")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(profit_chart_path, dpi=300)
    plt.show()

    print(f"Cumulative profit chart saved to: {profit_chart_path}")

    # ---------------------------
    # Plot 2: Drawdown
    # ---------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(drawdown_df["date"], drawdown_df["drawdown"], marker="o")
    plt.title("Drawdown Curve")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(drawdown_chart_path, dpi=300)
    plt.show()

    print(f"Drawdown chart saved to: {drawdown_chart_path}")


if __name__ == "__main__":
    main()