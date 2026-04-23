import pandas as pd
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).resolve().parent.parent
reports_folder = project_root / "reports"
reports_folder.mkdir(exist_ok=True)


def get_run_date():
    return datetime.now().strftime("%Y-%m-%d")


def export_valid_selections(valid_selections):
    if not valid_selections:
        print("No valid selections to export.")
        return

    run_date = get_run_date()

    rows = []
    for item in valid_selections:
        row = item.copy()
        row["run_date"] = run_date
        rows.append(row)

    df = pd.DataFrame(rows)
    output_path = reports_folder / "valid_selections.csv"
    df.to_csv(output_path, index=False)
    print(f"Valid selections exported to: {output_path}")


def export_valid_combos(combos):
    if not combos:
        print("No valid combos to export.")
        return

    run_date = get_run_date()
    combo_rows = []

    for i, combo in enumerate(combos, start=1):
        leg1, leg2 = combo["legs"]

        combo_rows.append({
            "run_date": run_date,
            "combo_number": i,

            "leg1_match": f"{leg1['home_team']} vs {leg1['away_team']}",
            "leg1_selection": leg1["selection_name"],
            "leg1_odds": leg1["decimal_odds"],
            "leg1_model_probability": leg1["model_probability"],
            "leg1_edge": leg1["edge"],
            "leg1_ev": leg1["expected_value"],
            "leg1_confidence": leg1["confidence_score"],

            "leg2_match": f"{leg2['home_team']} vs {leg2['away_team']}",
            "leg2_selection": leg2["selection_name"],
            "leg2_odds": leg2["decimal_odds"],
            "leg2_model_probability": leg2["model_probability"],
            "leg2_edge": leg2["edge"],
            "leg2_ev": leg2["expected_value"],
            "leg2_confidence": leg2["confidence_score"],

            "combined_odds": combo["combined_odds"],
            "combined_probability": combo["combined_probability"],
            "combo_ev": combo["combo_ev"],
            "average_edge": combo["average_edge"],
            "average_confidence": combo["average_confidence"]
        })

    df = pd.DataFrame(combo_rows)
    output_path = reports_folder / "valid_combos.csv"
    df.to_csv(output_path, index=False)
    print(f"Valid combos exported to: {output_path}")


def export_best_combo(best_combo):
    if best_combo is None:
        print("No best combo to export.")
        return

    run_date = get_run_date()
    leg1, leg2 = best_combo["legs"]

    best_combo_row = {
        "run_date": run_date,

        "leg1_match": f"{leg1['home_team']} vs {leg1['away_team']}",
        "leg1_selection": leg1["selection_name"],
        "leg1_odds": leg1["decimal_odds"],
        "leg1_model_probability": leg1["model_probability"],
        "leg1_edge": leg1["edge"],
        "leg1_ev": leg1["expected_value"],
        "leg1_confidence": leg1["confidence_score"],

        "leg2_match": f"{leg2['home_team']} vs {leg2['away_team']}",
        "leg2_selection": leg2["selection_name"],
        "leg2_odds": leg2["decimal_odds"],
        "leg2_model_probability": leg2["model_probability"],
        "leg2_edge": leg2["edge"],
        "leg2_ev": leg2["expected_value"],
        "leg2_confidence": leg2["confidence_score"],

        "combined_odds": best_combo["combined_odds"],
        "combined_probability": best_combo["combined_probability"],
        "combo_ev": best_combo["combo_ev"],
        "average_edge": best_combo["average_edge"],
        "average_confidence": best_combo["average_confidence"]
    }

    df = pd.DataFrame([best_combo_row])
    output_path = reports_folder / "best_combo.csv"
    df.to_csv(output_path, index=False)
    print(f"Best combo exported to: {output_path}")