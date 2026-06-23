import datetime
import sqlite3 as sql
from typing import Any

from loguru import logger

from config import DB_NAME


class Database:
    def __init__(self):
        self.db_name: str = DB_NAME
        self.connection: sql.Connection | None = None
        self.cursor: sql.Cursor | None = None

    def connect(self):
        self.connection: sql.Connection = sql.connect(self.db_name)
        if self.connection:
            logger.info(f"Connected to {self.db_name}")
        else:
            raise ConnectionError(f"Failed to connect to {self.db_name}")

        self.cursor: sql.Cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS mails (title TEXT, id TEXT, date DATETIME, run_date DATETIME, status TEXT, PRIMARY KEY (title, id))"
        )

    def exists_mail(self, title: str, id: str) -> bool:
        if not self.connection:
            raise ConnectionError("Database connection is not established.")

        cursor: sql.Cursor = self.connection.cursor()
        cursor.execute("SELECT 1 FROM mails WHERE title = ? AND id = ?", (title, id))
        value: Any = cursor.fetchone()
        if value is not None:
            logger.info(f"Mail found in Database: {title} - {id}")
        else:
            logger.info(f"Mail not found in Database: {title} - {id}")

        return value is not None

    def add_mail(self, title: str, id: str, date: datetime.datetime):
        if not self.connection:
            raise ConnectionError("Database connection is not established.")

        cursor: sql.Cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO mails (title, id, date, run_date) VALUES (?, ?, ?, DATETIME('now'))",
            (title, id, date),
        )
        self.connection.commit()
        logger.info(f"Mail added to Database: {title} - {id}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        logger.info(f"Disconnected from {self.db_name}")

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Database connection is not established.")

        cursor: sql.Cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()
