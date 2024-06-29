from app.database.postgres_client import PostgresClient


class Recommendations:
    def search_courses(self, courses: list):
        def search_course(course):
            def extract_time(list):
                try:
                    return (int(list[5].replace(":", "")))
                except Exception:
                    return 0
            client = PostgresClient()
            result = client.search_course(course)
            if len(result) == 0:
                return [None]
            result.sort(key=extract_time)
            return result
        result = []
        for course in courses:
            result.append(search_course(course))
        return result

    def __check_time_overlap(self, start_time1, end_time1, start_time2, end_time2):
        """
        returns boolean whether these times overlap or not, True if overlap
        """
        min1 = int(start_time1.replace(":", ""))
        max1 = int(end_time1.replace(":", ""))
        min2 = int(start_time2.replace(":", ""))
        max2 = int(end_time2.replace(":", ""))

        return not ((max2 - min1) * (min2 - max1) >= 0)

    def daysToBitmask(self, days: str):
        daysMap = {"M": 1 << 0, "T": 1 << 1, "W": 1 << 2, "H": 1 << 3, "F": 1 << 4}
        bitmask = 0
        for i in days:
            bitmask |= daysMap.get(i)
        return bitmask

    def overlaps(
        self,
        section_id: str,
        days: str,
        newStartTime: str,
        newEndTime: str,
        courses: list,
    ) -> dict:
        try:
            if not days or not newStartTime or not newEndTime:
                return None
            newDaysBitmask = self.daysToBitmask(days)
            if len(courses) == 0:
                return {
                    "section_id": section_id,
                    "days": newDaysBitmask,
                    "start_time": newStartTime,
                    "end_time": newEndTime,
                }
            for section in range(len(courses)):
                course = courses[section]
                existingDaysBitmask = course[1]
                existingStartTime = course[2]
                existingEndTime = course[3]
                if (newDaysBitmask & existingDaysBitmask) != 0:
                    # Overlapping days
                    if self.__check_time_overlap(
                        existingStartTime, existingEndTime, newStartTime, newEndTime
                    ):
                        return None
        except Exception as e:
            print(e)
        return {
            "section_id": section_id,
            "days": newDaysBitmask,
            "start_time": newStartTime,
            "end_time": newEndTime,
        }


# test = Recommendations()
# print(test.__search_courses("CSCI104"))
# x = [["301234", 1, "14:00", "15:00"]]
# course = test.overlaps("31231", "MTWHF", "12:00", "14:00", x)
# if course:
#     x.append(
#         [course["section_id"], course["days"], course["start_time"], course["end_time"]]
#     )
# print(x)
