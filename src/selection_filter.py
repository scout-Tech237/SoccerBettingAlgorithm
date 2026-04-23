MIN_ODDS_PER_LEG = 1.18
MAX_ODDS_PER_LEG = 1.65
MIN_EDGE = 0.02
MIN_EV = 0.01
MIN_MODEL_PROBABILITY = 0.60
MIN_CONFIDENCE_SCORE = 70.0


def is_valid_selection(selection):
    """
    Check whether a selection passes our filter rules.
    """
    if selection["decimal_odds"] < MIN_ODDS_PER_LEG:
        return False

    if selection["decimal_odds"] > MAX_ODDS_PER_LEG:
        return False

    if selection["edge"] < MIN_EDGE:
        return False

    if selection["expected_value"] < MIN_EV:
        return False

    if selection["model_probability"] < MIN_MODEL_PROBABILITY:
        return False

    if selection["confidence_score"] < MIN_CONFIDENCE_SCORE:
        return False

    return True


def filter_selections(evaluated_selections):
    """
    Return only the selections that pass the rules.
    """
    return [s for s in evaluated_selections if is_valid_selection(s)]