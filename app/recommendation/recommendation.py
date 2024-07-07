from app.database.postgres_client import PostgresClient
import itertools
class CourseSearcher:

    def get_recommendations(self, selected_courses: list):
        courses = self.search_courses(selected_courses)
        combinations = self.all_combonations(courses)
        combinations = self.section_combination(combinations)
        schedules = []
        for combo in combinations:
            timeClient = TimeClient()
            potential_schedule = []
            time_conflict = False
            for course in combo:
                for section in course:
                    if len(potential_schedule) == 0:
                        potential_schedule.append(section)
                        continue
                    if not timeClient.overlaps(potential_schedule, section):
                        potential_schedule.append(section)
                    else:
                        time_conflict = True
                        break
                if (time_conflict):
                    break
            if not time_conflict:
                schedules.append(potential_schedule)
        return schedules
    def section_combination(self, combo: list):
        if len(combo) == 0:
            return {}
        combinations = []
        for combos in combo:
            classes = dict()
            for section in combos:
                if not classes.get(section[2]):
                    classes[section[2]] = {}
                    required_types = (self.get_required_course_types(section[2]).values())
                    course = classes.get(section[2])
                    for _ in required_types:
                        for types in _:
                            course.update({types:set()})
                classes.get(section[2]).get(section[8]).add(section)
            courses = {}
            for key, value in classes.items():
                values = value.values()
                combo = list(itertools.product(*values))
                courses.update({key: combo})
            class_lists = [courses[key] for key in courses]
            combination = list(itertools.product(*class_lists))
            for combo in combination:
                combinations.append(combo)
        return combinations
    def all_combonations(self, courses: list):
        if len(courses) == 0:
            return []
        if len(courses) == 1:
            return courses[0]
        combinations = courses[0]
        for i in range(1, len(courses)):
            combinations = list(itertools.product(combinations, courses[i]))
            combinations = [list(itertools.chain(*combo)) for combo in combinations]
        combinations = [combo for combo in combinations]
        return combinations
        
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
            elif "Lec" in section[8] and len(set([section[8] for section in combo])) == 1:
                combo.append(section)
            elif "Lec" in section[8] and len(set([section[8] for section in combo])) != 1:
                possible_combonations.append(combo)
                combo = []
                combo.append(section)
            else:
                combo.append(section)
        if len(combo) != 0:
            possible_combonations.append(combo)
        return possible_combonations

    def get_required_course_types(self, course: str):
        client = PostgresClient()
        sections = client.search_course(course)
        required_sections = set()
        for section in sections:
            required_sections.add(section[8])
        return {course: required_sections}

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
