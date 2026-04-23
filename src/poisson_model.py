from math import exp, factorial


def poisson_pmf(k: int, lam: float) -> float:
    """
    Calculate Poisson probability of scoring exactly k goals
    when expected goals = lam.
    """
    return (exp(-lam) * (lam ** k)) / factorial(k)


def build_score_matrix(lambda_home: float, lambda_away: float, max_goals: int = 6):
    """
    Build a matrix of score probabilities.
    matrix[h][a] = probability that home scores h and away scores a
    """
    matrix = []

    for home_goals in range(max_goals + 1):
        row = []
        for away_goals in range(max_goals + 1):
            p_home = poisson_pmf(home_goals, lambda_home)
            p_away = poisson_pmf(away_goals, lambda_away)
            row.append(p_home * p_away)
        matrix.append(row)

    return matrix


def calculate_market_probabilities(score_matrix):
    """
    Derive market probabilities from the score matrix.
    """
    size = len(score_matrix)

    p_home_win = 0.0
    p_draw = 0.0
    p_away_win = 0.0
    p_over_15 = 0.0
    p_under_45 = 0.0
    p_btts_yes = 0.0

    for h in range(size):
        for a in range(size):
            p = score_matrix[h][a]

            if h > a:
                p_home_win += p
            elif h == a:
                p_draw += p
            else:
                p_away_win += p

            if h + a >= 2:
                p_over_15 += p

            if h + a <= 4:
                p_under_45 += p

            if h >= 1 and a >= 1:
                p_btts_yes += p

    p_btts_no = 1 - p_btts_yes
    p_1x = p_home_win + p_draw
    p_x2 = p_draw + p_away_win
    p_12 = p_home_win + p_away_win

    # Draw no bet probabilities
    if (1 - p_draw) > 0:
        p_home_dnb = p_home_win / (1 - p_draw)
        p_away_dnb = p_away_win / (1 - p_draw)
    else:
        p_home_dnb = 0.0
        p_away_dnb = 0.0

    return {
        "HOME_WIN": p_home_win,
        "DRAW": p_draw,
        "AWAY_WIN": p_away_win,
        "OVER_1_5": p_over_15,
        "UNDER_4_5": p_under_45,
        "BTTS_YES": p_btts_yes,
        "BTTS_NO": p_btts_no,
        "1X": p_1x,
        "X2": p_x2,
        "12": p_12,
        "HOME_DNB": p_home_dnb,
        "AWAY_DNB": p_away_dnb
    }