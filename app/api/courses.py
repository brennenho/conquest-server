import json
import requests

from app.utils.constants import CLASS_API_BASE, SEMESTER, COURSE_DEPT_ACRONYMS


class CourseClient:
    def get_all_departments(self) -> list:
        """
        Retrieves and returns data for all departments.

        Returns:
            list: A list of course data for all departments.
        """
        course_data = []
        for dept in COURSE_DEPT_ACRONYMS:
            course_data.append(self.get_department(dept))
        return course_data

    def get_instructor_name(self, json) -> dict:
        """
        Retrieves the first and last name of the instructor from the given JSON data.

        Args:
            json (dict): The JSON data containing the instructor information.

        Returns:
            dict: A dictionary containing the first name and last name of the instructor.
        """
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
            return {"first_name": "", "last_name": ""}
        except KeyError:
            return {
                "first_name": "",
                "last_name": "",
            }

    def get_start_end_time(self, json: dict) -> dict:
        """
        Retrieves the start and end time from the given JSON object.

        Args:
            json (dict): The JSON object containing the start and end time.

        Returns:
            dict: A dictionary containing the start and end time.
            If the start or end time is not found in the JSON object, defaults to "TBA".
        """
        try:
            if isinstance(json["start_time"], list):
                for i in range(len(json["start_time"])):
                    if not isinstance(json["start_time"][i], str):
                        json["start_time"][i] = "TBA"
            if isinstance(json["end_time"], list):
                for i in range(len(json["end_time"])):
                    if not isinstance(json["end_time"][i], str):
                        json["end_time"][i] = "TBA"
            return {
                "start_time": json["start_time"],
                "end_time": json["end_time"],
            }
        except KeyError:
            return {
                "start_time": "TBA",
                "end_time": "TBA",
            }

    def get_section_days(self, json: dict) -> dict:
        """
        Retrieves the section days from the given JSON object.

        Args:
            json (dict): A JSON object containing the section days.

        Returns:
            dict: A dictionary with the section days.
        """
        try:
            if json["day"] == {}:
                json["day"] = "TBA"
            if isinstance(json["day"], list):
                for i in range(len(json["day"])):
                    if not isinstance(json["day"][i], str):
                        json["day"][i] = "TBA"
            return {
                "days": json["day"],
            }
        except:
            return {"days": "TBA"}

    def parse_course_data_list(self, json: list, course: dict) -> list:
        """
        Parses the course data list from a JSON response and returns a list of section details.

        Args:
            json (list): The JSON response containing the course data.
            course (dict): The course information.

        Returns:
            list: A list of section details, where each key is a dict containing:
                - class_type: The type of the class.
                - instructor: A list of instructor names.
                - section_id: The ID of the section.
                - start_time: The start time of the section.
                - end_time: The end time of the section.
                - days: The days on which the section meets.
                - class_name: The name of the class.
        """
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
                    "class_name": f"{course['CourseData']['prefix']}-{course['CourseData']['number']}"
                }
            )
            # individual section for each class
            foundSection.append(foundSectionDetail)
        return foundSection

    def parse_course_data_dict(self, json: dict, course: dict) -> list:
        """
        Parses the course data dictionary and extracts relevant information for a section.

        Args:
            json (dict): The JSON response containing the course data.
            course (dict): The course information.

        Returns:
            list: A list of section details, where each key is a dict containing:
                - class_type: The type of the class.
                - instructor: A list of instructor names.
                - section_id: The ID of the section.
                - start_time: The start time of the section.
                - end_time: The end time of the section.
                - days: The days on which the section meets.
                - class_name: The name of the class.
        """
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
                "class_name": f"{course['CourseData']['prefix']}-{course['CourseData']['number']}"
            }
        )
        # individual section for each class
        foundSection.append(foundSectionDetail)
        return foundSection

    def get_department(self, dep: str) -> list:
        """
        Retrieves the courses offered by a specific department.

        Args:
            dep (str): The department code or name.

        Returns:
            list: A list of course data for the department.
        """
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
