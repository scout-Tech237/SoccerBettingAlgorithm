import pandas as pd
from pathlib import Path

from historical_data_loader import (
    load_historical_matches,
    load_historical_odds,
    load_historical_results
)
from historical_evaluator import evaluate_day_selections
from selection_filter import filter_selections
from combo_builder import build_two_leg_combos, rank_combos
from result_checker import selection_won
from staking import fixed_percentage_stake, kelly_stake

project_root = Path(__file__).resolve().parent.parent
reports_folder = project_root / "reports"
reports_folder.mkdir(exist_ok=True)

STARTING_BANKROLL = 100.0


def evaluate_combo_result(best_combo, results_df, target_date):
    if best_combo is None:
        return None

    for leg in best_combo["legs"]:
        match_name = f"{leg['home_team']} vs {leg['away_team']}"
        result_row = results_df[
            (results_df["match_date"] == target_date) &
            (results_df["match"] == match_name)
        ]

        if result_row.empty:
            return None

        home_goals = int(result_row.iloc[0]["home_goals"])
        away_goals = int(result_row.iloc[0]["away_goals"])

        won = selection_won(leg["selection_name"], home_goals, away_goals)
        if not won:
            return False

    return True


def calculate_stake(bankroll, best_combo, strategy_name):
    if strategy_name == "fixed_1pct":
        return fixed_percentage_stake(bankroll, stake_percentage=0.01)

    if strategy_name == "fixed_0_5pct":
        return fixed_percentage_stake(bankroll, stake_percentage=0.005)

    if strategy_name == "kelly_half_capped":
        return kelly_stake(
            bankroll=bankroll,
            decimal_odds=best_combo["combined_odds"],
            win_probability=best_combo["combined_probability"],
            fraction=0.5,
            max_stake_pct=0.03
        )

    raise ValueError(f"Unknown strategy: {strategy_name}")


def run_backtest_for_strategy(strategy_name, matches_df, odds_df, results_df):
    unique_dates = sorted(matches_df["match_date"].unique())

    bankroll = STARTING_BANKROLL
    peak_bankroll = STARTING_BANKROLL
    max_drawdown = 0.0

    total_staked = 0.0
    total_returned = 0.0
    total_bets = 0
    total_wins = 0
    total_losses = 0
    total_no_bets = 0

    for target_date in unique_dates:
        evaluated = evaluate_day_selections(matches_df, odds_df, target_date)
        valid_selections = filter_selections(evaluated)
        combos = build_two_leg_combos(valid_selections)
        ranked_combos = rank_combos(combos)

        best_combo = ranked_combos[0] if ranked_combos else None

        if best_combo is None:
            total_no_bets += 1
            drawdown = peak_bankroll - bankroll
            max_drawdown = max(max_drawdown, drawdown)
            continue

        stake = calculate_stake(bankroll, best_combo, strategy_name)
        result = evaluate_combo_result(best_combo, results_df, target_date)

        total_staked += stake
        total_bets += 1

        if result is True:
            returned_amount = stake * best_combo["combined_odds"]
            profit = returned_amount - stake
            bankroll += profit
            total_returned += returned_amount
            total_wins += 1
        elif result is False:
            profit = -stake
            bankroll += profit
            total_losses += 1
        else:
            profit = 0.0

        peak_bankroll = max(peak_bankroll, bankroll)
        drawdown = peak_bankroll - bankroll
        max_drawdown = max(max_drawdown, drawdown)

    net_profit = total_returned - total_staked
    roi = ((net_profit / total_staked) * 100) if total_staked > 0 else 0.0

    return {
        "strategy": strategy_name,
        "starting_bankroll": round(STARTING_BANKROLL, 2),
        "ending_bankroll": round(bankroll, 2),
        "total_betting_days": total_bets,
        "winning_days": total_wins,
        "losing_days": total_losses,
        "no_bet_days": total_no_bets,
        "total_staked": round(total_staked, 2),
        "total_returned": round(total_returned, 2),
        "net_profit": round(net_profit, 2),
        "roi_percent": round(roi, 2),
        "max_drawdown": round(max_drawdown, 2)
    }


def main():
    matches_df = load_historical_matches()
    odds_df = load_historical_odds()
    results_df = load_historical_results()

    strategies = [
        "fixed_1pct",
        "fixed_0_5pct",
        "kelly_half_capped"
    ]

    results = []

    for strategy in strategies:
        summary = run_backtest_for_strategy(strategy, matches_df, odds_df, results_df)
        results.append(summary)

    comparison_df = pd.DataFrame(results)

    print("=" * 90)
    print("STAKING STRATEGY COMPARISON")
    print("=" * 90)
    print(comparison_df.to_string(index=False))

    output_path = reports_folder / "strategy_comparison.csv"
    comparison_df.to_csv(output_path, index=False)
    print(f"\nStrategy comparison exported to: {output_path}")


if __name__ == "__main__":
    main()