from app.database.postgres_client import PostgresClient
from app.scrapers.courses import CourseParser


class AlertManager:
    def check_sections(self):
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
            if seats[0] < seats[1]:
                print(f"Section {id} has available seats!")
                # email = section[2]
                # send_email(email, id)
