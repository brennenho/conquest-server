from app.database.postgres_client import PostgresClient
class Reccomendations:
    def check_time_overlap(self, start_time1, end_time1, start_time2, end_time2):
        """
        returns boolean whether these times overlap or not, True if overlap
        """
        min1 = int(start_time1.replace(":", ""))
        max1 = int(end_time1.replace(":", ""))
        min2 = int(start_time2.replace(":", ""))
        max2 = int(end_time2.replace(":", ""))

        return not ((max2 - min1) * (min2 - max1) >= 0)
    def recommend_courses(self, courses: list):
        def search_courses(courses: list):
            def search_course(course):
                client = PostgresClient()
                result = client.search_course(course)
                if len(result) == 0:
                    return [None]
                return result

            result = []
            for course in courses:
                result.append(search_course(course))
            return result
        PLACE_HOLDER_START, PLACE_HOLDER_END = "00:00", "00:00"
        times = []
        response = search_courses(courses)
        for course in response:
            types = set()
            days = {'M':[], 'T': [], 'W': [], 'H': [], 'F': []}
            for section in course:
                if (self.check_time_overlap(PLACE_HOLDER_START, PLACE_HOLDER_END, section[5], section[6]) or (section[-1] in types)):
                    continue
                place_holder_start = section[5]
                place_holder_end = section[6]
                types.add(section[-1])
                times.append(section)
        return times
