from pathlib import Path
from dotenv import load_dotenv
import os

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

if not FOOTBALL_DATA_API_KEY:
    raise ValueError("Missing FOOTBALL_DATA_API_KEY in .env")

if not ODDS_API_KEY:
    raise ValueError("Missing ODDS_API_KEY in .env")