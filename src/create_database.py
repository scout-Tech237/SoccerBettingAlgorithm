import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
db_path = project_root / "database" / "betting_model.db"
schema_path = project_root / "database" / "schema.sql"

conn = sqlite3.connect(db_path)

with open(schema_path, "r", encoding="utf-8") as file:
    schema_sql = file.read()

conn.executescript(schema_sql)
conn.commit()
conn.close()

print(f"Database created successfully at: {db_path}")