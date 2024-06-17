
import requests
from bs4 import BeautifulSoup


class CourseParser:

    def scrape_deparment(self):
        response = requests.get("https://www.ratemyprofessors.com/search/professors/1381")
        soup = BeautifulSoup(response.text, "lxml")
        courses = soup.find_all('script')
        found_sections = []
        for course in courses:
            if "window.__RELAY_STORE__" in course.text: 
                scores = self.parseRating(course.text)
                id = self.parseID(course.text)
                return {id[i]:scores[i] for i in range(len(scores))}
        return "No ratings found"
    
    def parseRating(self, html: str):
        scores_found = []
        while (html.find('avgRating') != -1):
            rating = html[html.find('avgRating')+11:html.find('numRatings')-2]
            html = html[html.find('numRatings')+3:]
            scores_found.append(rating)
        return scores_found
    
    def parseID(self, html: str):
        id_found = []
        while (html.find('legacyId') != -1):
            rating = html[html.find('legacyId')+10:html.find('avgRating')-2]
            html = html[html.find('avgRating')+3:]
            id_found.append(rating)
        return id_found
            
        

x = CourseParser()
print(x.scrape_deparment())
       
