from evaluate_match import evaluate_all_selections
from selection_filter import filter_selections
from combo_builder import build_two_leg_combos, rank_combos
from report_exporter import (
    export_valid_selections,
    export_valid_combos,
    export_best_combo
)


def print_valid_selections(valid_selections):
    print("=" * 70)
    print("VALID SELECTIONS")
    print("=" * 70)

    if not valid_selections:
        print("No valid selections found.")
        return

    for item in valid_selections:
        print(f"\nMatch: {item['home_team']} vs {item['away_team']}")
        print(f"Expected Goals: Home={item['lambda_home']:.2f}, Away={item['lambda_away']:.2f}")
        print(f"Market: {item['market_type']}")
        print(f"Selection: {item['selection_name']}")
        print(f"Odds: {item['decimal_odds']:.2f}")
        print(f"Model Probability: {item['model_probability']:.4f}")
        print(f"Market Probability: {item['market_probability']:.4f}")
        print(f"Edge: {item['edge']:.4f}")
        print(f"Expected Value: {item['expected_value']:.4f}")
        print(f"Confidence Score: {item['confidence_score']:.1f}")


def print_combos(combos):
    print("\n" + "=" * 70)
    print("VALID 2-LEG COMBOS")
    print("=" * 70)

    if not combos:
        print("No valid combos found near odds 2.00.")
        return

    for i, combo in enumerate(combos, start=1):
        leg1, leg2 = combo["legs"]

        print(f"\nCombo #{i}")
        print(f"Leg 1: {leg1['home_team']} vs {leg1['away_team']} | "
              f"{leg1['selection_name']} @ {leg1['decimal_odds']:.2f}")
        print(f"       Expected Goals: Home={leg1['lambda_home']:.2f}, Away={leg1['lambda_away']:.2f}")
        print(f"       Confidence: {leg1['confidence_score']:.1f}")

        print(f"Leg 2: {leg2['home_team']} vs {leg2['away_team']} | "
              f"{leg2['selection_name']} @ {leg2['decimal_odds']:.2f}")
        print(f"       Expected Goals: Home={leg2['lambda_home']:.2f}, Away={leg2['lambda_away']:.2f}")
        print(f"       Confidence: {leg2['confidence_score']:.1f}")

        print(f"Combined Odds: {combo['combined_odds']:.4f}")
        print(f"Combined Probability: {combo['combined_probability']:.4f}")
        print(f"Combo EV: {combo['combo_ev']:.4f}")
        print(f"Average Edge: {combo['average_edge']:.4f}")
        print(f"Average Confidence: {combo['average_confidence']:.1f}")


def print_best_combo(best_combo):
    print("\n" + "=" * 70)
    print("BEST COMBO")
    print("=" * 70)

    if best_combo is None:
        print("No bet today. No combo passed the rules.")
        return

    leg1, leg2 = best_combo["legs"]

    print(f"\nLeg 1: {leg1['home_team']} vs {leg1['away_team']}")
    print(f"Selection: {leg1['selection_name']} @ {leg1['decimal_odds']:.2f}")
    print(f"Expected Goals: Home={leg1['lambda_home']:.2f}, Away={leg1['lambda_away']:.2f}")
    print(f"Confidence Score: {leg1['confidence_score']:.1f}")

    print(f"\nLeg 2: {leg2['home_team']} vs {leg2['away_team']}")
    print(f"Selection: {leg2['selection_name']} @ {leg2['decimal_odds']:.2f}")
    print(f"Expected Goals: Home={leg2['lambda_home']:.2f}, Away={leg2['lambda_away']:.2f}")
    print(f"Confidence Score: {leg2['confidence_score']:.1f}")

    print(f"\nCombined Odds: {best_combo['combined_odds']:.4f}")
    print(f"Combined Probability: {best_combo['combined_probability']:.4f}")
    print(f"Combo EV: {best_combo['combo_ev']:.4f}")
    print(f"Average Edge: {best_combo['average_edge']:.4f}")
    print(f"Average Confidence: {best_combo['average_confidence']:.1f}")


def main():
    evaluated = evaluate_all_selections()
    valid_selections = filter_selections(evaluated)
    combos = build_two_leg_combos(valid_selections)
    ranked_combos = rank_combos(combos)

    print_valid_selections(valid_selections)
    print_combos(ranked_combos)

    best_combo = ranked_combos[0] if ranked_combos else None
    print_best_combo(best_combo)

    # Export reports
    export_valid_selections(valid_selections)
    export_valid_combos(ranked_combos)
    export_best_combo(best_combo)


if __name__ == "__main__":
    main()