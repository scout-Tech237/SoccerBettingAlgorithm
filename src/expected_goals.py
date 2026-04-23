from data_loader import load_team_stats, load_league_averages

TEAM_STATS = load_team_stats()
LEAGUE_AVERAGES = load_league_averages()


def calculate_expected_goals(home_team, away_team, league):

    if home_team not in TEAM_STATS:
        raise ValueError(f"Missing team stats for {home_team}")

    if away_team not in TEAM_STATS:
        raise ValueError(f"Missing team stats for {away_team}")

    if league not in LEAGUE_AVERAGES:
        raise ValueError(f"Missing league averages for {league}")

    home_stats = TEAM_STATS[home_team]
    away_stats = TEAM_STATS[away_team]
    league_avg = LEAGUE_AVERAGES[league]

    league_home_goals = league_avg["home_goals"]
    league_away_goals = league_avg["away_goals"]

    home_attack_strength = home_stats["home_goals_scored"] / league_home_goals
    away_defense_weakness = away_stats["away_goals_conceded"] / league_home_goals

    away_attack_strength = away_stats["away_goals_scored"] / league_away_goals
    home_defense_weakness = home_stats["home_goals_conceded"] / league_away_goals

    expected_home_goals = league_home_goals * home_attack_strength * away_defense_weakness
    expected_away_goals = league_away_goals * away_attack_strength * home_defense_weakness

    return round(expected_home_goals, 3), round(expected_away_goals, 3)