import os
import json
import psycopg2

from app.utils.logger import get_logger
import app.database.queries as Queries

logger = get_logger(__name__)


class PostgresClient:

    def __init__(self):
        # attempt to establish connection to Postgres
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port="5432",
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute(Queries.CREATE_TABLE_WATCHLIST)
            self.conn.commit()
            self.cursor.execute(Queries.CREATE_TABLE_PROFESSORLIST)
            self.conn.commit()
        except psycopg2.OperationalError as e:
            raise Exception("Unable to connect to Postgres.")

    def search_professor(
        self, first_name: str, last_name: str, department: str
    ) -> list:
        self.cursor.execute(
            Queries.SEARCH_PROFESSOR,
            (first_name, last_name, department.lower(), department.lower()),
        )
        return self.cursor.fetchone()

    def add_professor(
        self,
        first_name: str,
        last_name: str,
        legacy_id: str,
        department: str,
        rating: str,
    ) -> None:
        data = (legacy_id, first_name, last_name, department, rating)
        self.cursor.execute(Queries.ADD_TO_PROFESSORLIST, data)
        self.conn.commit()

    def add_to_watchlist(self, section_id: str, department: str, email: str) -> None:
        self.cursor.execute(Queries.ADD_TO_WATCHLIST, (section_id, department, email))
        self.conn.commit()

    def get_watchlist(self) -> list:
        try:
            self.cursor.execute(Queries.GET_WATCHLIST)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            logger.error(f"Error fetching watchlist: {e}")
            return []

    def delete_from_watchlist(self, section_id: str) -> None:
        self.cursor.execute(Queries.DELETE_FROM_WATCHLIST, (section_id,))
        self.conn.commit()

    def delete_email_from_watchlist(self, section_id: str, email: str) -> None:
        self.cursor.execute(
            Queries.DELETE_EMAIL_FROM_WATCHLIST,
            (section_id, email),
        )
        self.conn.commit()

    def search_watchlist(self, section_id: str, email: str) -> list:
        self.cursor.execute(Queries.SEARCH_WATCHLIST, (section_id, email))
        return self.cursor.fetchone()

    def search_by_email(self, email: str) -> list:
        self.cursor.execute(Queries.SEARCH_BY_EMAIL, (email,))
        return self.cursor.fetchall()

    def __del__(self) -> None:
        try:
            self.cursor.close()
            self.conn.close()
        except AttributeError:
            logger.warning(
                "PostgresClient attempted to close a non-existent connection."
            )
