from expected_goals import calculate_expected_goals
from poisson_model import build_score_matrix, calculate_market_probabilities
from odds_tools import implied_probability, expected_value, edge
from confidence import calculate_confidence


def evaluate_day_selections(matches_df, odds_df, target_date):
    """
    Evaluate all selections for one date from historical CSV files.
    """
    day_matches = matches_df[matches_df["match_date"] == target_date]
    day_odds = odds_df[odds_df["match_date"] == target_date]

    evaluated = []
    match_id_counter = 1

    for _, match_row in day_matches.iterrows():
        league = match_row["league"]
        home_team = match_row["home_team"]
        away_team = match_row["away_team"]

        lambda_home, lambda_away = calculate_expected_goals(home_team, away_team, league)
        score_matrix = build_score_matrix(lambda_home, lambda_away)
        market_probs = calculate_market_probabilities(score_matrix)

        match_odds = day_odds[
            (day_odds["home_team"] == home_team) &
            (day_odds["away_team"] == away_team)
        ]

        for _, odds_row in match_odds.iterrows():
            selection_name = odds_row["selection_name"]
            market_type = odds_row["market_type"]
            decimal_odds = odds_row["decimal_odds"]

            if selection_name not in market_probs:
                continue

            model_prob = market_probs[selection_name]
            market_prob = implied_probability(decimal_odds)
            selection_edge = edge(model_prob, market_prob)
            selection_ev = expected_value(model_prob, decimal_odds)

            selection = {
                "match_id": match_id_counter,
                "match_date": target_date,
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

        match_id_counter += 1

    return evaluated