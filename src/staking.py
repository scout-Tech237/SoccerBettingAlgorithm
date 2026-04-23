def fixed_percentage_stake(bankroll, stake_percentage=0.01):
    """
    Stake a fixed percentage of bankroll.
    Example: 1% of bankroll.
    """
    return bankroll * stake_percentage


def kelly_fraction(decimal_odds, win_probability):
    """
    Kelly fraction formula:
    f = (bp - q) / b

    where:
    b = odds - 1
    p = win probability
    q = 1 - p
    """
    b = decimal_odds - 1
    p = win_probability
    q = 1 - p

    if b <= 0:
        return 0.0

    f = (b * p - q) / b
    return max(0.0, f)


def kelly_stake(
    bankroll,
    decimal_odds,
    win_probability,
    fraction=0.5,
    max_stake_pct=0.03
):
    """
    Half-Kelly by default, with a max stake cap.
    Example:
    - fraction=0.5 means half-Kelly
    - max_stake_pct=0.03 means max 3% of bankroll
    """
    raw_kelly = kelly_fraction(decimal_odds, win_probability)
    adjusted_kelly = raw_kelly * fraction
    adjusted_kelly = min(adjusted_kelly, max_stake_pct)

    return bankroll * adjusted_kelly