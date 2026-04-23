import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
fixtures_path = project_root / "data" / "live_fixtures.csv"

df = pd.read_csv(fixtures_path)

print("=" * 70)
print("LIVE FIXTURES")
print("=" * 70)
print(df.to_string(index=False))