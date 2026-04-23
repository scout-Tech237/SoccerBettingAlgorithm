import requests
from datetime import datetime, timedelta, timezone

from config_live import FOOTBALL_DATA_API_KEY
from team_name_map import normalize_team_name

BASE_URL = "https://api.football-data.org/v4"
COMPETITIONS = ["PL", "PD", "SA"]  # Premier League, La Liga, Serie A


def today_utc_range():
    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc)
    end = start + timedelta(days=2)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def fetch_matches_for_competition(code: str):
    date_from, date_to = today_utc_range()

    url = f"{BASE_URL}/competitions/{code}/matches"
    headers = {"X-Auth-Token": FOOTBALL_DATA_API_KEY}
    params = {
        "dateFrom": date_from,
        "dateTo": date_to,
        "status": "SCHEDULED"
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def normalize_matches(api_json):
    matches = []

    for match in api_json.get("matches", []):
        home = match.get("homeTeam", {}).get("name")
        away = match.get("awayTeam", {}).get("name")
        utc_date = match.get("utcDate")
        status = match.get("status")
        competition = api_json.get("competition", {}).get("name")

        if home and away:
            matches.append({
                "league": competition,
                "match_date_utc": utc_date,
                "home_team": normalize_team_name(home),
                "away_team": normalize_team_name(away),
                "status": status
            })

    return matches


def fetch_all_live_fixtures():
    all_matches = []

    for code in COMPETITIONS:
        data = fetch_matches_for_competition(code)
        all_matches.extend(normalize_matches(data))

    return all_matches


if __name__ == "__main__":
    fixtures = fetch_all_live_fixtures()
    print(f"Fetched {len(fixtures)} upcoming matches")
    for row in fixtures[:20]:
        print(row)