from app.database.postgres_client import PostgresClient
from app.scrapers.courses import CourseParser
from app.alerts.mail import send_course_alert
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AlertManager:

    @staticmethod
    async def check_sections():
        client = PostgresClient()
        parser = CourseParser()
        watchlist = client.get_watchlist()
        departments = {}
        notifiedSections = set()

        for entry in watchlist:
            id = entry[1]
            dep = entry[2]
            if dep not in departments:
                departments[dep] = parser.scrape_deparment(dep)

            seats = departments[dep][id]
            if seats[0] < seats[1]:
                notifiedSections.add(id)
                email = entry[3]
                # send_course_alert(email, id, seats[1] - seats[0])
                logger.info(
                    f"Mock alert to {email} about section {id} having {seats[1] - seats[0]} seats."
                )

        for section in notifiedSections:
            client.delete_from_watchlist(section)
