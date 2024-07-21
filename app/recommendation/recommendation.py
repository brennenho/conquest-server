from app.database.postgres_client import PostgresClient
import itertools


class CourseSearcher:
    def sort_schedules(self, schedules: list):
        def start_to_end_time(sections: list[str]):
            classes = {
                "M": (2400, -1),
                "T": (2400, -1),
                "W": (2400, -1),
                "H": (2400, -1),
                "F": (2400, -1),
            }
            for section in sections:
                for day in section[7]:
                    classes[day] = (
                        min(classes[day][0], self.extract_time(section)),
                        max(
                            classes[day][1], self.extract_time(section, by_start=False)
                        ),
                    )
            longest_day = 0
            days_with_class = 5
            for item in classes.values():
                if item[0] == 2400:
                    days_with_class -= 1
                longest_day = max(item[1] - item[0], longest_day)
            return longest_day << days_with_class

        schedules.sort(key=start_to_end_time)
        schedules = [[course[1] for course in group] for group in schedules]
        return schedules

    def get_recommendations(self, selected_courses: list):
        if len(selected_courses) == 0:
            return []
        courses = self.get_scheduled_courses(selected_courses)
        combinations = self.get_course_combonations(courses)
        combinations = self.get_potential_schedules(combinations)
        schedules = []
        for combo in combinations:
            timeClient = TimeClient()
            potential_schedule: list = []
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
                if time_conflict:
                    break
            if not time_conflict:
                schedules.append(potential_schedule)
        return self.sort_schedules(schedules)

    def get_potential_schedules(self, combo: list):
        if len(combo) == 0:
            return {}
        combinations = []
        for combos in combo:
            classes: dict[str, dict[str, set]] = {}
            for section in combos:
                # If the course is not registered yet
                if not classes.get(section[2]):
                    classes[section[2]] = {}
                    required_types = self.get_required_course_types(section[2]).values()
                    course = classes.get(section[2])
                    # Instantiate the required course types here
                    if course == {}:
                        for _ in required_types:
                            for types in _:
                                course.update({types: set()})
                # Add the section to the right course and course type
                course_name = classes.get(section[2])
                if isinstance(course_name, dict):
                    course_name_type = course_name.get(section[8])
                    if isinstance(course_name_type, set):
                        course_name_type.add(section)
            # Get one of each required course type and append it as a possible schedule
            courses = {}
            for key, value in classes.items():
                values = value.values()
                combo = list(itertools.product(*values))
                courses.update({key: combo})
            class_lists = [courses[key] for key in courses]
            combination: list = list(itertools.product(*class_lists))
            for combo in combination:
                combinations.append(combo)
        return combinations

    def get_course_combonations(self, courses: list):
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

    def get_scheduled_courses(self, selected: list):
        courses = []
        for course in selected:
            courses.append(self.get_course_divisions(course))
        return courses

    def get_course_divisions(self, course: str) -> list:
        client = PostgresClient()
        result = client.search_course(course)
        if len(result) == 0:
            return [None]
        possible_combonations: list = []
        combo: list = []
        for section in result:
            if len(combo) == 0:
                combo.append(section)
            elif (
                "Lec" in section[8] and len(set([section[8] for section in combo])) == 1
            ):
                combo.append(section)
            elif (
                "Lec" in section[8] and len(set([section[8] for section in combo])) != 1
            ):
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

    def extract_time(self, list, by_start=True, ignore_quiz=True):
        try:
            if ignore_quiz and list[8] == "Qz":
                return 0
            key = 5 if by_start else 6
            return int(list[key].replace(":", ""))
        except Exception:
            return 0


class TimeClient:
    @staticmethod
    def _check_time_overlap(
        start_time1: str, end_time1: str, start_time2: str, end_time2: str
    ) -> bool:
        """
        Check if two time intervals overlap.

        Args:
            start_time1 (str): Start time of the first interval in HH:MM format.
            end_time1 (str): End time of the first interval in HH:MM format.
            start_time2 (str): Start time of the second interval in HH:MM format.
            end_time2 (str): End time of the second interval in HH:MM format.

        Returns:
            bool: True if the intervals overlap, False otherwise.
        """
        min1, max1 = int(start_time1.replace(":", "")), int(end_time1.replace(":", ""))
        min2, max2 = int(start_time2.replace(":", "")), int(end_time2.replace(":", ""))
        return not ((max2 - min1) * (min2 - max1) >= 0)

    @staticmethod
    def days_to_bitmask(days: str) -> int:
        """
        Convert a string of days into a bitmask representation.

        Args:
            days (str): A string representing days (e.g., "MWF" for Monday, Wednesday, and Friday).

        Returns:
            int: Bitmask representation of the days.
        """
        days_map = {
            "M": 1 << 0,
            "T": 1 << 1,
            "W": 1 << 2,
            "H": 1 << 3,
            "F": 1 << 4,
        }
        bitmask = 0
        for day in days:
            bit = days_map.get(day, 0)
            bitmask |= bit
        return bitmask

    def overlaps(self, booked_sections: list, new_section: list) -> bool:
        """
        Check if a new section overlaps with any of the booked sections.

        Args:
            booked_sections (list): List of booked sections.
            new_section (list): New section to be checked for overlap.

        Returns:
            bool: True if there is an overlap, False otherwise.
        """
        try:
            new_days = new_section[7]
            new_start_time = new_section[5]
            new_end_time = new_section[6]

            if not new_days or not new_start_time or not new_end_time:
                return True

            new_days_bitmask = self.days_to_bitmask(new_days)

            if not booked_sections:
                return False

            for section in booked_sections:
                existing_days_bitmask = self.days_to_bitmask(section[7])
                existing_start_time = section[5]
                existing_end_time = section[6]

                if new_days_bitmask & existing_days_bitmask:
                    # Overlapping days
                    if self._check_time_overlap(
                        existing_start_time,
                        existing_end_time,
                        new_start_time,
                        new_end_time,
                    ):
                        return True
        except Exception as e:
            print(f"Error checking overlap: {e}")

        return False
