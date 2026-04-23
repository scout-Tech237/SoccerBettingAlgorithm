from itertools import combinations

COMBO_MIN_ODDS = 1.90
COMBO_MAX_ODDS = 2.10


def build_two_leg_combos(valid_selections):
    combos = []

    for leg1, leg2 in combinations(valid_selections, 2):
        if leg1["match_id"] == leg2["match_id"]:
            continue

        combined_odds = leg1["decimal_odds"] * leg2["decimal_odds"]
        combined_probability = leg1["model_probability"] * leg2["model_probability"]
        combo_ev = (combined_probability * combined_odds) - 1
        average_edge = (leg1["edge"] + leg2["edge"]) / 2
        average_confidence = (leg1["confidence_score"] + leg2["confidence_score"]) / 2

        if COMBO_MIN_ODDS <= combined_odds <= COMBO_MAX_ODDS:
            combos.append({
                "legs": [leg1, leg2],
                "combined_odds": combined_odds,
                "combined_probability": combined_probability,
                "combo_ev": combo_ev,
                "average_edge": average_edge,
                "average_confidence": average_confidence
            })

    return combos


def rank_combos(combos):
    return sorted(
        combos,
        key=lambda c: (c["combo_ev"], c["average_confidence"], c["combined_probability"]),
        reverse=True
    )