import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime, timezone

DB_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DB_DIR / "carbon_intensity.db"


def init_db() -> None:
    """Create DB + table if it doesn't exist."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS carbon_intensity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                ts_utc TEXT NOT NULL,
                carbon_gco2_per_kwh REAL NOT NULL
            )
            """
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_ci_location_ts ON carbon_intensity(location, ts_utc)"
        )
        conn.commit()


def insert_reading(location: str, carbon_gco2_per_kwh: float, ts_utc: Optional[str] = None) -> None:
    """Insert one carbon intensity reading."""
    if ts_utc is None:
        ts_utc = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO carbon_intensity (location, ts_utc, carbon_gco2_per_kwh)
            VALUES (?, ?, ?)
            """,
            (location, ts_utc, float(carbon_gco2_per_kwh)),
        )
        conn.commit()


def lowest_intensity_times(location: str, limit: int = 3) -> List[Tuple[str, float]]:
    """
    Return the lowest carbon-intensity readings for a given location.
    Output: list of (ts_utc, carbon_gco2_per_kwh)
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT ts_utc, carbon_gco2_per_kwh
            FROM carbon_intensity
            WHERE location = ?
            ORDER BY carbon_gco2_per_kwh ASC
            LIMIT ?
            """,
            (location, int(limit)),
        )
        rows = cur.fetchall()

    return [(r[0], float(r[1])) for r in rows]