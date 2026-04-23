import requests
from datetime import datetime, timedelta, timezone

from config_live import ODDS_API_KEY
from team_name_map import normalize_team_name

BASE_URL = "https://api.the-odds-api.com/v4/sports"

SPORT_KEYS = [
    "soccer_epl",
    "soccer_spain_la_liga",
    "soccer_italy_serie_a"
]


def today_utc_window():
    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc)
    end = start + timedelta(days=2)
    return start.isoformat().replace("+00:00", "Z"), end.isoformat().replace("+00:00", "Z")


def fetch_odds_for_sport(sport_key: str):
    commence_from, commence_to = today_utc_window()

    url = f"{BASE_URL}/{sport_key}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal",
        "commenceTimeFrom": commence_from,
        "commenceTimeTo": commence_to,
        "dateFormat": "iso"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def normalize_odds(api_json, sport_key):
    rows = []

    for event in api_json:
        home_team = normalize_team_name(event.get("home_team"))
        away_team = normalize_team_name(event.get("away_team"))
        commence_time = event.get("commence_time")

        bookmakers = event.get("bookmakers", [])

        for bookmaker in bookmakers:
            book_name = bookmaker.get("title")

            for market in bookmaker.get("markets", []):
                if market.get("key") != "h2h":
                    continue

                for outcome in market.get("outcomes", []):
                    rows.append({
                        "sport_key": sport_key,
                        "commence_time": commence_time,
                        "home_team": home_team,
                        "away_team": away_team,
                        "bookmaker": book_name,
                        "market_type": "H2H",
                        "selection_name": normalize_team_name(outcome.get("name")),
                        "decimal_odds": outcome.get("price")
                    })

    return rows


def fetch_all_live_odds():
    all_rows = []

    for sport_key in SPORT_KEYS:
        data = fetch_odds_for_sport(sport_key)
        all_rows.extend(normalize_odds(data, sport_key))

    return all_rows


if __name__ == "__main__":
    odds = fetch_all_live_odds()
    print(f"Fetched {len(odds)} odds rows")
    for row in odds[:20]:
        print(row)