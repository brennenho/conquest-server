from typing import Iterable
from app.database.postgres_client import PostgresClient
from app.scrapers.courses import CourseParser
from app.alerts.mail import send_course_alert


class AlertManager:

    @staticmethod
    async def check_sections():
        client = PostgresClient()
        parser = CourseParser()
        watchlist = client.get_watchlist()
        print(watchlist)
        departments = {}
        sections = set()
        notifiedSections = set()

        for entry in watchlist:
            print(entry)
            id = entry[1]
            dep = entry[2]
            if dep not in departments:
                departments[dep] = parser.scrape_deparment(dep)

            seats = departments[dep][id]
            if seats[0] < seats[1]:
                notifiedSections.add(id)
                email = entry[3]
                # send_course_alert(email, id, seats[1] - seats[0])
                print(
                    f"Alerting {email} about section {id} having {seats[1] - seats[0]} seats."
                )

        for section in notifiedSections:
            client.delete_from_watchlist(section)
            pass
