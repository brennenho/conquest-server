import asyncio

from app.database.postgres_client import PostgresClient
from app.scrapers.courses import CourseParser
from app.alerts.mail import send_course_alert, send_password
from app.utils.logger import get_logger
from app.utils.tokens import generate_random_pass

logger = get_logger(__name__)


class AlertManager:
    _instance = None
    _passwords: dict[str, str] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    async def generate_password(self, email: str) -> str:
        """
        Generate a random one-time password for a user. Password expires after 10 minutes.

        Returns:
            str: A 6-character alphanumeric password.
        """
        if email in self._passwords:
            del self._passwords[email]
        password: str = generate_random_pass()
        self._passwords[email] = password
        send_password(email, password)
        # Schedule a task to remove the password after 10 minutes
        asyncio.get_event_loop().call_later(600, self.remove_password, email)
        return password

    def remove_password(self, email: str) -> None:
        """
        Remove a one-time password for a user.

        Returns:
            None
        """
        if email in self._passwords:
            del self._passwords[email]

    def validate_password(self, email: str, password: str) -> bool:
        """
        Validate a one-time password for a user.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        if email in self._passwords:
            if self._passwords[email] == password:
                return True
        return False

    # Checks all functions in watchlist, scraping department info when necessary
    @staticmethod
    async def check_sections() -> None:
        client = PostgresClient()
        parser = CourseParser()
        watchlist: list[str] = client.get_watchlist()
        departments: dict[str, dict[str, list[int]]] = {}
        notifiedSections = set()

        for entry in watchlist:
            id: str = entry[1]
            dep: str = entry[2]
            if dep not in departments:
                # scrape info for entire department if not already done
                departments[dep] = parser.scrape_deparment(dep)

            seats: list[int] = departments[dep][id]
            # check if there are seats available
            if seats[0] < seats[1]:
                notifiedSections.add(id)
                email: str = entry[3]
                send_course_alert(email, id, seats[1] - seats[0])
                # logger.info(
                #     f"Mock alert to {email} about section {id} having {seats[1] - seats[0]} seats."
                # )

        # remove sections that have openings from watchlist
        for section in notifiedSections:
            client.delete_from_watchlist(section)
