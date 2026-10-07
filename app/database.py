import sqlite3
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent
DATABASE_PATH=BASE_DIR/"instance"/"trip_planner.db"

def get_connection():
    conn=sqlite3.connect(DATABASE_PATH)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    DATABASE_PATH.parent.mkdir(parents=True,exist_ok=True)
    conn=get_connection()
    try:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS trips(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL CHECK(length(trim(destination))>0),
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            budget NUMERIC NOT NULL CHECK(budget>0),
            max_travelers INTEGER NOT NULL CHECK(max_travelers>0),
            status TEXT NOT NULL DEFAULT 'PLANNED'
                CHECK(status IN('PLANNED','ONGOING','COMPLETED','CANCELLED')),
            CHECK(end_date>start_date)
        );

        CREATE TABLE IF NOT EXISTS travelers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL CHECK(length(trim(name))>0),
            email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS trip_travelers(
            trip_id INTEGER NOT NULL,
            traveler_id INTEGER NOT NULL,
            PRIMARY KEY(trip_id,traveler_id),
            FOREIGN KEY(trip_id) REFERENCES trips(id) ON DELETE CASCADE,
            FOREIGN KEY(traveler_id) REFERENCES travelers(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            title TEXT NOT NULL CHECK(length(trim(title))>0),
            amount NUMERIC NOT NULL CHECK(amount>0),
            FOREIGN KEY(trip_id) REFERENCES trips(id) ON DELETE CASCADE
        );
        """)
        conn.commit()
    finally:
        conn.close()