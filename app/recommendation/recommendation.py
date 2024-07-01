from app.database.postgres_client import PostgresClient


class CourseSearcher:

    def get_recommendations(self, selected_courses: list):
        courses = self.search_courses(selected_courses)
        required_types = []
        for course in selected_courses:
            required_types.append(self.get_required_course_types(course))
        required_courses = dict(zip(selected_courses, required_types))
        courselist = dict(zip(selected_courses, [[]] * len(selected_courses)))
        
        for course in courses:
            for combo in course:
                for section in combo:
                    ...
        return courses

    def search_courses(self, selected: list):
        courses = []
        for course in selected:
            courses.append(self.get_course_combonations(course))
        return courses

    def get_course_combonations(self, course: str) -> list:
        client = PostgresClient()
        result = client.search_course(course)
        if len(result) == 0:
            return [None]
        possible_combonations = []
        combo = []
        for section in result:
            if len(combo) == 0:
                combo.append(section)
            elif "Lec" in section[8] and len(set(combo)) == 1:
                combo.append(section)
            elif "Lec" in section[8] and len(set(combo)) != 1:
                possible_combonations.append(self.sort_sections(combo))
                combo = []
                combo.append(section)
            else:
                combo.append(section)
        if len(combo) != 0:
            possible_combonations.append(self.sort_sections(combo))
        return possible_combonations

    def get_required_course_types(self, course: str):
        client = PostgresClient()
        sections = client.search_course(course)
        required_sections = set()
        for section in sections:
            required_sections.add(section[8])
        return required_sections

    def sort_sections(self, sections: list):
        def extract_time(list):
            try:
                return int(list[5].replace(":", ""))
            except Exception:
                return 0

        sections.sort(key=extract_time)
        return sections


class TimeClient:
    def __check_time_overlap(
        self, start_time1: str, end_time1: str, start_time2: str, end_time2: str
    ):
        """
        returns boolean whether these times overlap or not, True if overlap
        """
        min1 = int(start_time1.replace(":", ""))
        max1 = int(end_time1.replace(":", ""))
        min2 = int(start_time2.replace(":", ""))
        max2 = int(end_time2.replace(":", ""))

        return not ((max2 - min1) * (min2 - max1) >= 0)

    def daysToBitmask(self, days: str):
        daysMap: dict = {
            "M": 1 << 0,
            "T": 1 << 1,
            "W": 1 << 2,
            "H": 1 << 3,
            "F": 1 << 4,
        }
        bitmask = 0
        for i in days:
            bitmask |= daysMap.get(i)
        return bitmask

    def overlaps(self, booked_sections: list, new_section: list) -> bool:
        try:
            days = new_section[7]
            newStartTime = new_section[5]
            newEndTime = new_section[6]
            if not days or not newStartTime or not newEndTime:
                return None
            newDaysBitmask = self.daysToBitmask(days)
            if len(booked_sections) == 0:
                return False
            for section in booked_sections:
                existingDaysBitmask = self.daysToBitmask(section[7])
                existingStartTime = section[5]
                existingEndTime = section[6]
                if (newDaysBitmask & existingDaysBitmask) != 0:
                    # Overlapping days
                    if self.__check_time_overlap(
                        existingStartTime, existingEndTime, newStartTime, newEndTime
                    ):
                        return True
        except Exception as e:
            print(e)
        return False
