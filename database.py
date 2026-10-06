import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "instance" / "trip_planner.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL
                    CHECK (length(trim(destination)) > 0),
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                budget NUMERIC NOT NULL CHECK (budget > 0),
                max_travelers INTEGER NOT NULL
                    CHECK (max_travelers > 0),
                status TEXT NOT NULL DEFAULT 'PLANNED'
                    CHECK (
                        status IN (
                            'PLANNED',
                            'ONGOING',
                            'COMPLETED',
                            'CANCELLED'
                        )
                    ),
                CHECK (end_date > start_date)
            )
        """)
        connection.commit()
    finally:
        connection.close()