from app.database.postgres_client import PostgresClient
from app.scrapers.courses import CourseParser
from app.alerts.mail import send_course_alert
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AlertManager:

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
                # send_course_alert(email, id, seats[1] - seats[0])
                logger.info(
                    f"Mock alert to {email} about section {id} having {seats[1] - seats[0]} seats."
                )

        # remove sections that have openings from watchlist
        for section in notifiedSections:
            client.delete_from_watchlist(section)
