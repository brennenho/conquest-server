import requests
from bs4 import BeautifulSoup

from app.util.constants import BASE_URL, TERM_URL


class CourseParser:

    def scrape_deparment(self, dep: str):
        print(BASE_URL + TERM_URL + "classes/" + dep)
        response = requests.get(BASE_URL + TERM_URL + "classes/" + dep)
        soup = BeautifulSoup(response.text, "lxml")
        courses = soup.find_all("div", class_="course-info")
        for course in courses:
            name = course.find("a", class_="courselink").find("strong").text[:-1]
            print(name)
            sections = course.find("table").find_all("tr")[1:]
            for section in sections:
                id = section.find("td", class_="section").text
                capacity = section.find("td", class_="registered").text.split(" of ")
                s = Section(id, int(capacity[0]), int(capacity[1]))
                print(s.id, s.registered, s.total)
            break


class Section:
    def __init__(self, id="", registered=0, total=0):
        self.id = id
        self.registered = registered
        self.total = total
