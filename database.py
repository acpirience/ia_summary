import sqlite3 as sql

from loguru import logger

DB_NAME: str = "IA_mails.db"


class Database:
    def __init__(self):
        self.db_name: str = DB_NAME
        self.connection: sql.Connection | None = None
        self.cursor: sql.Cursor | None = None

    def connect(self):
        self.connection = sql.connect(self.db_name)
        if self.connection:
            logger.info(f"Connected to {self.db_name}")
        else:
            logger.error(f"Failed to connect to {self.db_name}")
            return
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS mails (title TEXT, id TEXT, date DATETIME, PRIMARY KEY (title, id))"
        )

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
