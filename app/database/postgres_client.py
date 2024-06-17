import os
import json
import psycopg2

from app.utils.logger import get_logger
import app.database.queries as Queries

logger = get_logger(__name__)


class PostgresClient:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port="5432",
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute(Queries.CREATE_TABLE)
            self.conn.commit()
        except psycopg2.OperationalError as e:
            raise Exception("Unable to connect to Postgres.")

    def add_to_watchlist(self, section_id: str, department: str, email: str):
        self.cursor.execute(Queries.ADD_TO_WATCHLIST, (section_id, department, email))
        self.conn.commit()

    def get_watchlist(self):
        try:
            self.cursor.execute(Queries.GET_WATCHLIST)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            logger.error(f"Error fetching watchlist: {e}")
            return []

    def delete_from_watchlist(self, section_id: str):
        self.cursor.execute(Queries.DELETE_FROM_WATCHLIST, (section_id,))
        self.conn.commit()

    def delete_email_from_watchlist(self, section_id: str, email: str):
        self.cursor.execute(
            Queries.DELETE_EMAIL_FROM_WATCHLIST,
            (section_id, email),
        )
        self.conn.commit()

    def search_watchlist(self, section_id: str, email: str):
        self.cursor.execute(Queries.SEARCH_WATCHLIST, (section_id, email))
        return self.cursor.fetchone()

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except AttributeError:
            logger.warning(
                "PostgresClient attempted to close a non-existent connection."
            )
