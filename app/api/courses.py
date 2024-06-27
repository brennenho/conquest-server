import json
import requests
import time

from app.utils.constants import CLASS_API_BASE, SEMESTER, COURSE_DEPT_ACRONYMS
from app.utils.logger import get_logger


class CourseClient:
    def get_all_departments(self):
        for dept in COURSE_DEPT_ACRONYMS:
            ...

    def get_department(self, dep: str):
        start = time.time()
        response = requests.get(CLASS_API_BASE + dep + "/" + SEMESTER)
        departmentCourses = {}
        for course in json.loads(response.text)["OfferedCourses"]["course"]:
            courseData = course["CourseData"]
            foundSection = {}
            if isinstance(courseData['SectionData'], list):
                for section in courseData["SectionData"]:
                    print(section.keys())
                    foundSection = {
                        "section_id": section['id'],
                        "days": section["day"],
                        "class_type": section["type"],
                    }
                    try:
                        foundSection.update(
                            {
                                "first_name": section["instructor"]["first_name"],
                                "last_name": section["instructor"]["last_name"],
                            }
                        )
                    except KeyError:
                        foundSection.update({"first_name": "", "last_name": ""})
                    try:
                        foundSection.update({
                            "start_time": section["start_time"],
                            "end_time": section["end_time"],
                        })
                    except KeyError:
                        foundSection.update({
                            "start_time": "TBA",
                            "end_time": "TBA",
                        })
                    foundCourse = {f"{course["CourseData"]['prefix']}{course["CourseData"]['number']}": foundSection}
                    departmentCourses.update(foundCourse)
            elif isinstance(courseData['SectionData'], dict):
                    section = courseData['SectionData']
                    print(section.keys())
                    foundSection = {
                        "section_id": section['id'],
                        "days": section["day"],
                        "class_type": section["type"],
                    }
                    try:
                        foundSection.update(
                            {
                                "first_name": section["instructor"]["first_name"],
                                "last_name": section["instructor"]["last_name"],
                            }
                        )
                    except KeyError:
                        foundSection.update({"first_name": "", "last_name": ""})
                    try:
                        foundSection.update({
                            "start_time": section["start_time"],
                            "end_time": section["end_time"],
                        })
                    except KeyError:
                        foundSection.update({
                            "start_time": "TBA",
                            "end_time": "TBA",
                        })
                        
                    foundCourse = {f"{course["CourseData"]['prefix']}{course["CourseData"]['number']}": foundSection}
                    departmentCourses.update(foundCourse)  
        return departmentCourses
