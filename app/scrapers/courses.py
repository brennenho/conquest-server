import requests
from bs4 import BeautifulSoup

from app.utils.constants import BASE_URL, TERM_URL
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CourseParser:

    def scrape_deparment(self, dep: str):
        print(BASE_URL + TERM_URL + "classes/" + dep)
        response = requests.get(BASE_URL + TERM_URL + "classes/" + dep)
        soup = BeautifulSoup(response.text, "lxml")
        courses = soup.find_all("div", class_="course-info")
        found_sections = {}
        for course in courses:
            try:
                name = course.find("a", class_="courselink").find("strong").text[:-1]
                sections = course.find("table").find_all(
                    "tr", attrs={"data-section-id": True}
                )
                for section in sections:
                    id = section.select_one("td.section, td.section-title").text
                    capacity = section.find("td", class_="registered").text.split(
                        " of "
                    )
                    found_sections[id] = [int(capacity[0]), int(capacity[1])]
                    # found_sections.append(
                    #     Section(id, int(capacity[0]), int(capacity[1]))
                    # )
            except:
                logger.warning("Error parsing course.")

        return found_sections


class Section:
    def __init__(self, id="", registered=0, total=0):
        self.id = id
        self.registered = registered
        self.total = total
