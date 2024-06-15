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
        departments = {}

        for section in watchlist:
            id = section[0]
            dep = section[1]
            if dep not in departments:
                departments[dep] = parser.scrape_deparment(dep)

            seats = departments[dep][id]
            print(watchlist)
            if seats[0] < seats[1]:
                emails = [section[2]] if isinstance(section[2], str) else section[2]

                for email in emails:
                    print("Sending email to: ", email)
                    send_course_alert(email, id, seats[1] - seats[0])
                client.delete_from_watchlist(id)
