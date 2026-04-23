import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
results_path = project_root / "data" / "results.csv"


def load_results():
    return pd.read_csv(results_path)


def selection_won(selection_name, home_goals, away_goals):
    """
    Return True if the selection wins, otherwise False.
    """
    if selection_name == "1X":
        return home_goals >= away_goals

    if selection_name == "HOME_DNB":
        return home_goals > away_goals

    if selection_name == "OVER_1_5":
        return (home_goals + away_goals) >= 2

    if selection_name == "UNDER_4_5":
        return (home_goals + away_goals) <= 4

    if selection_name == "BTTS_YES":
        return home_goals >= 1 and away_goals >= 1

    if selection_name == "BTTS_NO":
        return not (home_goals >= 1 and away_goals >= 1)

    return False


def evaluate_best_combo(best_combo):
    """
    Check whether the best combo won or lost using results.csv.
    """
    if best_combo is None:
        return {
            "status": "NO_BET"
        }

    results_df = load_results()
    leg_results = []

    for leg in best_combo["legs"]:
        match_name = f"{leg['home_team']} vs {leg['away_team']}"
        result_row = results_df[results_df["match"] == match_name]

        if result_row.empty:
            leg_results.append({
                "match": match_name,
                "selection": leg["selection_name"],
                "result_found": False,
                "won": False
            })
            continue

        home_goals = int(result_row.iloc[0]["home_goals"])
        away_goals = int(result_row.iloc[0]["away_goals"])

        won = selection_won(leg["selection_name"], home_goals, away_goals)

        leg_results.append({
            "match": match_name,
            "selection": leg["selection_name"],
            "result_found": True,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "won": won
        })

    combo_won = all(leg["won"] for leg in leg_results if leg["result_found"])
    all_results_found = all(leg["result_found"] for leg in leg_results)

    return {
        "status": "EVALUATED" if all_results_found else "PARTIAL",
        "combo_won": combo_won if all_results_found else None,
        "legs": leg_results
    }