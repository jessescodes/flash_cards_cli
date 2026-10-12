# flash_card_cli.database.py

import sqlite3


class DataBase:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                easiness REAL NOT NULL,
                interval INTEGER NOT NULL,
                timestamp REAL NOT NULL
            );
        """)

    def insert_card(
        self, front: str, back: str, easiness: float, interval: int, timestamp: float
    ) -> int:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO cards (front, back, easiness, interval, timestamp) VALUES (?, ?, ?, ?, ?)",
                (front, back, easiness, interval, timestamp),
            )
            if isinstance(cursor.lastrowid, int):
                return cursor.lastrowid
            else:
                raise TypeError("Database failed to generate ro ID for card")

    def get_all_cards(self) -> list[tuple]:
        cursor = self.conn.execute(
            "SELECT id, front, back, easiness, interval, timestamp FROM cards"
        )
        return cursor.fetchall()
