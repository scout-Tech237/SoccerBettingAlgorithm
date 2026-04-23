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

# Choose one:
# STAKING_MODE = "fixed_percentage"
STAKING_MODE = "kelly"

FIXED_STAKE_PERCENTAGE = 0.01  # 1%
KELLY_FRACTION = 0.5           # half-Kelly
KELLY_MAX_STAKE_PCT = 0.03     # max 3% of bankroll


def evaluate_combo_result(best_combo, results_df, target_date):
    """
    Return whether the combo won on the target date.
    """
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


def calculate_stake(bankroll, best_combo):
    """
    Choose stake based on selected staking mode.
    """
    if STAKING_MODE == "fixed_percentage":
        return fixed_percentage_stake(
            bankroll,
            stake_percentage=FIXED_STAKE_PERCENTAGE
        )

    if STAKING_MODE == "kelly":
        return kelly_stake(
            bankroll,
            decimal_odds=best_combo["combined_odds"],
            win_probability=best_combo["combined_probability"],
            fraction=KELLY_FRACTION,
            max_stake_pct=KELLY_MAX_STAKE_PCT
        )

    raise ValueError(f"Unknown staking mode: {STAKING_MODE}")


def main():
    matches_df = load_historical_matches()
    odds_df = load_historical_odds()
    results_df = load_historical_results()

    unique_dates = sorted(matches_df["match_date"].unique())

    backtest_rows = []
    total_staked = 0.0
    total_returned = 0.0
    total_bets = 0
    total_wins = 0
    total_losses = 0
    total_no_bets = 0

    bankroll = STARTING_BANKROLL
    peak_bankroll = STARTING_BANKROLL
    max_drawdown = 0.0

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

            backtest_rows.append({
                "date": target_date,
                "decision": "NO_BET",
                "staking_mode": STAKING_MODE,
                "stake": 0.0,
                "combined_odds": None,
                "combo_ev": None,
                "average_confidence": None,
                "result": None,
                "profit": 0.0,
                "bankroll_after_bet": round(bankroll, 2),
                "peak_bankroll": round(peak_bankroll, 2),
                "drawdown": round(drawdown, 2)
            })
            continue

        stake = calculate_stake(bankroll, best_combo)
        result = evaluate_combo_result(best_combo, results_df, target_date)

        total_staked += stake
        total_bets += 1

        if result is True:
            returned_amount = stake * best_combo["combined_odds"]
            profit = returned_amount - stake
            bankroll += profit
            total_returned += returned_amount
            total_wins += 1
            result_label = "WIN"

        elif result is False:
            profit = -stake
            bankroll += profit
            total_losses += 1
            result_label = "LOSS"

        else:
            profit = 0.0
            result_label = "MISSING_RESULT"

        peak_bankroll = max(peak_bankroll, bankroll)
        drawdown = peak_bankroll - bankroll
        max_drawdown = max(max_drawdown, drawdown)

        leg1, leg2 = best_combo["legs"]

        backtest_rows.append({
            "date": target_date,
            "decision": "BET",
            "staking_mode": STAKING_MODE,
            "stake": round(stake, 4),
            "leg1_match": f"{leg1['home_team']} vs {leg1['away_team']}",
            "leg1_selection": leg1["selection_name"],
            "leg2_match": f"{leg2['home_team']} vs {leg2['away_team']}",
            "leg2_selection": leg2["selection_name"],
            "combined_odds": round(best_combo["combined_odds"], 4),
            "combo_ev": round(best_combo["combo_ev"], 4),
            "average_confidence": round(best_combo["average_confidence"], 1),
            "result": result_label,
            "profit": round(profit, 4),
            "bankroll_after_bet": round(bankroll, 2),
            "peak_bankroll": round(peak_bankroll, 2),
            "drawdown": round(drawdown, 2)
        })

    net_profit = total_returned - total_staked
    roi = ((net_profit / total_staked) * 100) if total_staked > 0 else 0.0

    print("=" * 70)
    print("MULTI-DAY BACKTEST SUMMARY")
    print("=" * 70)
    print(f"Staking Mode: {STAKING_MODE}")
    print(f"Starting Bankroll: {STARTING_BANKROLL:.2f}")
    print(f"Ending Bankroll: {bankroll:.2f}")
    print(f"Total Betting Days: {total_bets}")
    print(f"Winning Days: {total_wins}")
    print(f"Losing Days: {total_losses}")
    print(f"No Bet Days: {total_no_bets}")
    print(f"Total Staked: {total_staked:.2f}")
    print(f"Total Returned: {total_returned:.2f}")
    print(f"Net Profit: {net_profit:.2f}")
    print(f"ROI: {roi:.2f}%")
    print(f"Max Drawdown: {max_drawdown:.2f}")

    df = pd.DataFrame(backtest_rows)
    output_path = reports_folder / "multi_day_backtest.csv"
    df.to_csv(output_path, index=False)
    print(f"\nBacktest details exported to: {output_path}")


if __name__ == "__main__":
    main()