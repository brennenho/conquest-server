import json
import requests

from app.utils.constants import CLASS_API_BASE, SEMESTER, COURSE_DEPT_ACRONYMS
from app.utils.logger import get_logger


class CourseClient:
    def get_all_departments(self):
        course_data = []
        for dept in COURSE_DEPT_ACRONYMS:
            course_data.append(self.get_department(dept))
        return course_data

    def get_instructor_name(self, json):
        try:
            json = json["instructor"]
            if isinstance(json, list):
                for professor in json:
                    return {
                        "first_name": professor["first_name"],
                        "last_name": professor["last_name"],
                    }
            elif isinstance(json, dict):
                return {
                    "first_name": json["first_name"],
                    "last_name": json["last_name"],
                }
        except KeyError:
            return {
                "first_name": "",
                "last_name": "",
            }

    def get_start_end_time(self, json):
        try:
            return {
                "start_time": json["start_time"],
                "end_time": json["end_time"],
            }
        except KeyError:
            return {
                "start_time": "TBA",
                "end_time": "TBA",
            }

    def get_section_days(self, json):
        try:
            return {
                "days": json["day"],
            }
        except KeyError:
            return {"days": "TBA"}

    def parse_course_data_list(self, json, course):
        foundSection = []
        for section in json:
            foundSectionDetail = {
                "class_type": section["type"],
                "instructor": [],
                "section_id": section["id"],
            }
            foundSectionDetail["instructor"].append(self.get_instructor_name(section))
            foundSectionDetail.update(self.get_start_end_time(section))
            foundSectionDetail.update(self.get_section_days(section))
            foundSectionDetail.update(
                {
                    "class_name": f"{course["CourseData"]['prefix']}{course["CourseData"]['number']}"
                }
            )
            # individual section for each class
            foundSection.append(foundSectionDetail)
        return foundSection

    def parse_course_data_dict(self, json, course):
        section = json
        foundSection = []
        foundSectionDetail = {
            "section_id": section["id"],
            "class_type": section["type"],
            "instructor": [],
        }
        foundSectionDetail["instructor"].append(self.get_instructor_name(section))
        foundSectionDetail.update(self.get_start_end_time(section))
        foundSectionDetail.update(self.get_section_days(section))
        foundSectionDetail.update(
            {
                "class_name": f"{course["CourseData"]['prefix']}{course["CourseData"]['number']}"
            }
        )
        # individual section for each class
        foundSection.append(foundSectionDetail)
        return foundSection

    def get_department(self, dep: str):
        response = requests.get(CLASS_API_BASE + dep + "/" + SEMESTER)
        departmentCourses = []
        for course in json.loads(response.text)["OfferedCourses"]["course"]:
            if isinstance(course, str):
                continue
            courseData = course["CourseData"]
            if isinstance(courseData["SectionData"], list):
                departmentCourses.append(
                    self.parse_course_data_list(courseData["SectionData"], course)
                )
            elif isinstance(courseData["SectionData"], dict):
                departmentCourses.append(
                    self.parse_course_data_dict(courseData["SectionData"], course)
                )
        return departmentCourses
