from choose_combo import main as run_combo_process
from evaluate_match import evaluate_all_selections
from selection_filter import filter_selections
from combo_builder import build_two_leg_combos, rank_combos
from result_checker import evaluate_best_combo


def main():
    evaluated = evaluate_all_selections()
    valid_selections = filter_selections(evaluated)
    combos = build_two_leg_combos(valid_selections)
    ranked_combos = rank_combos(combos)

    best_combo = ranked_combos[0] if ranked_combos else None
    result = evaluate_best_combo(best_combo)

    print("=" * 70)
    print("BACKTEST RESULT")
    print("=" * 70)

    if best_combo is None:
        print("No bet today.")
        return

    if result["status"] == "PARTIAL":
        print("Some match results are missing.")
        return

    for leg in result["legs"]:
        print(f"\nMatch: {leg['match']}")
        print(f"Selection: {leg['selection']}")
        print(f"Final Score: {leg['home_goals']} - {leg['away_goals']}")
        print(f"Won: {'YES' if leg['won'] else 'NO'}")

    print("\n" + "=" * 70)
    print(f"COMBO WON: {'YES' if result['combo_won'] else 'NO'}")
    print("=" * 70)


if __name__ == "__main__":
    main()