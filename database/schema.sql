DROP TABLE IF EXISTS odds;
DROP TABLE IF EXISTS matches;

CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT NOT NULL,
    league TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_goals INTEGER,
    away_goals INTEGER
);

CREATE TABLE odds (
    odds_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    market_type TEXT NOT NULL,
    selection_name TEXT NOT NULL,
    decimal_odds REAL NOT NULL,
    FOREIGN KEY(match_id) REFERENCES matches(match_id)
);