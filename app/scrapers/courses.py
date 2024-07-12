import requests
from bs4 import BeautifulSoup

# from app.utils.constants import BASE_URL, TERM_URL
from app.utils.logger import get_logger

BASE_URL = "https://classes.usc.edu/"
TERM_URL = "term-20243/"

logger = get_logger(__name__)


class CourseParser:

    # scrape section info by department
    def scrape_department(self, dep: str) -> dict:
        """
        Scrapes the department page for course information.

        Args:
            dep (str): The department code.

        Returns:
            dict: A dictionary containing the found sections and their capacities.
        """
        # get website code
        response = requests.get(BASE_URL + TERM_URL + "classes/" + dep)
        soup = BeautifulSoup(response.text, "lxml")

        # use BeautifulSoup to parse website code
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
            except:
                logger.warning("Error parsing course.")

        return found_sections
