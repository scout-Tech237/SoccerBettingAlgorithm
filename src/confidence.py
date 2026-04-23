def calculate_confidence(selection):
    """
    Calculate a simple confidence score from 0 to 100.
    This is a rule-based first version.
    """

    score = 50.0

    lambda_home = selection["lambda_home"]
    lambda_away = selection["lambda_away"]
    edge = selection["edge"]
    model_probability = selection["model_probability"]
    selection_name = selection["selection_name"]

    goal_gap = abs(lambda_home - lambda_away)
    total_goals = lambda_home + lambda_away

    # Stronger edge increases confidence
    if edge >= 0.10:
        score += 20
    elif edge >= 0.06:
        score += 14
    elif edge >= 0.03:
        score += 8
    elif edge >= 0.02:
        score += 4

    # High model probability increases confidence
    if model_probability >= 0.85:
        score += 15
    elif model_probability >= 0.75:
        score += 10
    elif model_probability >= 0.65:
        score += 6

    # Match-shape rules
    # If home side looks clearly stronger, home-protective markets gain confidence
    if selection_name in ["1X", "HOME_DNB"]:
        if lambda_home > lambda_away:
            score += 10
        if goal_gap >= 0.80:
            score += 10
        elif goal_gap >= 0.40:
            score += 5

    # Under 4.5 is more reliable in moderate-total-goal games
    if selection_name == "UNDER_4_5":
        if total_goals <= 3.2:
            score += 12
        elif total_goals <= 3.8:
            score += 6
        else:
            score -= 8

    # BTTS_NO is better when away attack is weak
    if selection_name == "BTTS_NO":
        if lambda_away <= 0.80:
            score += 10
        elif lambda_away <= 1.00:
            score += 5

    # BTTS_YES is better when both teams project to score reasonably
    if selection_name == "BTTS_YES":
        if lambda_home >= 1.2 and lambda_away >= 1.0:
            score += 8
        else:
            score -= 8

    # Penalize very high total goal environments for defensive markets
    if selection_name in ["UNDER_4_5", "BTTS_NO"] and total_goals > 4.0:
        score -= 10

    # Clamp score
    score = max(0, min(100, score))

    return round(score, 1)