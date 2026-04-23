def implied_probability(decimal_odds: float) -> float:
    """
    Convert decimal odds to implied probability.
    """
    if decimal_odds <= 0:
        raise ValueError("Decimal odds must be greater than zero.")
    return 1 / decimal_odds


def expected_value(model_probability: float, decimal_odds: float) -> float:
    """
    Calculate EV = (probability * odds) - 1
    """
    return (model_probability * decimal_odds) - 1


def edge(model_probability: float, market_probability: float) -> float:
    """
    Calculate edge = model probability - market probability
    """
    return model_probability - market_probability