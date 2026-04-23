import sqlite3
from pathlib import Path

from poisson_model import build_score_matrix, calculate_market_probabilities
from odds_tools import implied_probability, expected_value, edge
from expected_goals import calculate_expected_goals
from confidence import calculate_confidence

project_root = Path(__file__).resolve().parent.parent
db_path = project_root / "database" / "betting_model.db"


def evaluate_all_selections():
    """
    Read all match odds from the database and evaluate them
    using automatically calculated expected goals.
    Returns a list of dictionaries.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT m.match_id, m.league, m.home_team, m.away_team, o.market_type, o.selection_name, o.decimal_odds
    FROM matches m
    JOIN odds o ON m.match_id = o.match_id
    ORDER BY m.match_id, o.odds_id
    """)

    rows = cursor.fetchall()
    conn.close()

    evaluated = []

    for row in rows:
        match_id, league, home_team, away_team, market_type, selection_name, decimal_odds = row

        lambda_home, lambda_away = calculate_expected_goals(home_team, away_team, league)

        score_matrix = build_score_matrix(lambda_home, lambda_away)
        market_probs = calculate_market_probabilities(score_matrix)

        if selection_name not in market_probs:
            continue

        model_prob = market_probs[selection_name]
        market_prob = implied_probability(decimal_odds)
        selection_edge = edge(model_prob, market_prob)
        selection_ev = expected_value(model_prob, decimal_odds)

        selection = {
            "match_id": match_id,
            "league": league,
            "home_team": home_team,
            "away_team": away_team,
            "market_type": market_type,
            "selection_name": selection_name,
            "decimal_odds": decimal_odds,
            "model_probability": model_prob,
            "market_probability": market_prob,
            "edge": selection_edge,
            "expected_value": selection_ev,
            "lambda_home": lambda_home,
            "lambda_away": lambda_away
        }

        selection["confidence_score"] = calculate_confidence(selection)

        evaluated.append(selection)

    return evaluated


def print_evaluation(evaluated):
    print("=" * 70)
    print("MATCH EVALUATION")
    print("=" * 70)

    for item in evaluated:
        print(f"\nLeague: {item['league']}")
        print(f"Match: {item['home_team']} vs {item['away_team']}")
        print(f"Expected Goals: Home={item['lambda_home']:.3f}, Away={item['lambda_away']:.3f}")
        print(f"Market: {item['market_type']}")
        print(f"Selection: {item['selection_name']}")
        print(f"Odds: {item['decimal_odds']:.2f}")
        print(f"Model Probability: {item['model_probability']:.4f}")
        print(f"Market Probability: {item['market_probability']:.4f}")
        print(f"Edge: {item['edge']:.4f}")
        print(f"Expected Value: {item['expected_value']:.4f}")
        print(f"Confidence Score: {item['confidence_score']:.1f}")


if __name__ == "__main__":
    evaluated = evaluate_all_selections()
    print_evaluation(evaluated)