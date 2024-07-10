def formatCourseResponse(section_info: dict) -> dict:
    """
    Format the course response from the database.
    """
    return {
        "name": section_info[2],
        "professors": " ".join(
            [
                section_info[3][1:-1].split(",")[i].replace('"', "")
                + " "
                + section_info[4][1:-1].split(",")[i].replace('"', "")
                for i in range(len(section_info[3][1:-1].split(",")))
            ]
        ),
        "start_time": section_info[5],
        "end_time": section_info[6],
        "days": section_info[7],
        "class_type": section_info[8],
    }
