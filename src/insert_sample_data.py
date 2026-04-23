import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
db_path = project_root / "database" / "betting_model.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# First match
cursor.execute("""
INSERT INTO matches (match_date, league, home_team, away_team, home_goals, away_goals)
VALUES (?, ?, ?, ?, ?, ?)
""", ("2026-04-22", "Premier League", "Arsenal", "Brighton", None, None))
match1_id = cursor.lastrowid

odds_match_1 = [
    (match1_id, "DOUBLE_CHANCE", "1X", 1.30),
    (match1_id, "DRAW_NO_BET", "HOME_DNB", 1.45),
    (match1_id, "OVER_1_5", "OVER_1_5", 1.25),
    (match1_id, "UNDER_4_5", "UNDER_4_5", 1.22),
    (match1_id, "BTTS_YES", "BTTS_YES", 1.70),
    (match1_id, "BTTS_NO", "BTTS_NO", 2.05)
]

cursor.executemany("""
INSERT INTO odds (match_id, market_type, selection_name, decimal_odds)
VALUES (?, ?, ?, ?)
""", odds_match_1)

# Second match
cursor.execute("""
INSERT INTO matches (match_date, league, home_team, away_team, home_goals, away_goals)
VALUES (?, ?, ?, ?, ?, ?)
""", ("2026-04-22", "La Liga", "Real Sociedad", "Getafe", None, None))
match2_id = cursor.lastrowid

odds_match_2 = [
    (match2_id, "DOUBLE_CHANCE", "1X", 1.40),
    (match2_id, "DRAW_NO_BET", "HOME_DNB", 1.55),
    (match2_id, "OVER_1_5", "OVER_1_5", 1.35),
    (match2_id, "UNDER_4_5", "UNDER_4_5", 1.20),
    (match2_id, "BTTS_YES", "BTTS_YES", 1.80),
    (match2_id, "BTTS_NO", "BTTS_NO", 1.95)
]

cursor.executemany("""
INSERT INTO odds (match_id, market_type, selection_name, decimal_odds)
VALUES (?, ?, ?, ?)
""", odds_match_2)

conn.commit()
conn.close()

print("Sample data inserted successfully.")