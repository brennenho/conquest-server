import requests
import json
from app.utils.constants import (
    RMP_BASE_URL,
    RMP_PAYLOAD_HEADER,
    RMP_PAYLOAD_PART_1,
    RMP_PAYLOAD_PART_2,
    RMP_PAYLOAD_PART_3,
    RMP_PAYLOAD_PART_4,
    RMP_DEPARTMENT_IDS,
    RMP_FIRST_PAYLOAD_PART_1,
    RMP_FIRST_PAYLOAD_PART_2,
)


class RmpParser:
    """
    Scrapes ratemyprofessor using graphql api payloads to load more professors a once.

    Defaults total number to scrape as 10 entries per scrape.
    """

    def __init__(self) -> None:
        self.payload = ""
        self.cursor = str
        self.parsed_department = False
        self.headers = RMP_PAYLOAD_HEADER

    def export_as_json(self):
        """Exports all professors at USC"""
        json_object = json.dumps(
            self.scrape_all_professors(), indent=4, ensure_ascii=False
        )
        with open("professors.json", "w") as outfile:
            outfile.write(json_object)

    def scrape_all_professors(self) -> dict:
        """Parses all professor at USC

        Returns:
            dict: json with the format of {teacher_firstname+teacher_last_name : {department, id, legacyid, rating}}
        """
        found_professors = {}
        self.parsed_department = False
        for departmentID in RMP_DEPARTMENT_IDS:
            professor_by_department = {}
            professor_by_department.update(self.setup_scrape(departmentID=departmentID))
            while not self.parsed_department:
                professor_by_department.update(
                    self.scrape_professors(departmentID=departmentID, count=100)
                )
            found_professors.update(professor_by_department)
        return found_professors

    def setup_scrape(self, departmentID: str) -> dict:
        """scrapes the first 8 professors on ratemyprofessor when it first loads

        Raises:
            RuntimeError: unable to send request to requested URL

        Returns:
            dict: formatted json for professor information. See parse_json() for more information.
        """
        first_payload = (
            f"{RMP_FIRST_PAYLOAD_PART_1}{departmentID}{RMP_FIRST_PAYLOAD_PART_2}"
        )
        response = requests.request(
            "POST", RMP_BASE_URL, headers=self.headers, data=first_payload
        )
        if response.status_code == 200:
            return self.parse_json(response.json())
        else:
            raise RuntimeError("Error parsing first setup of scrapes")

    def scrape_professors(self, departmentID: str, count: int = 10) -> dict:
        """scrapes professor data from ratemyprofessor

        Args:
            count (int, optional): The number of professor entries to scrape. Defaults to 10.

        Raises:
            RuntimeError: unable to scrape the next batch of professors

        Returns:
            dict: Formatted json file for professor information. See parse_json() for more information.
        """
        self.payload = f"{RMP_PAYLOAD_PART_1}{count}{RMP_PAYLOAD_PART_2}{self.cursor}{RMP_PAYLOAD_PART_3}{departmentID}{RMP_PAYLOAD_PART_4}"
        response = requests.request(
            "POST", RMP_BASE_URL, headers=self.headers, data=self.payload
        )
        if response.status_code == 200:
            return self.parse_json(response.json())
        else:
            raise RuntimeError("Error parsing first setup of scrapes")

    def parse_json(self, json: dict) -> dict:
        """parses graphql responses from ratemyprofessor to give streamline format to store

        Args:
            json (dict): json response file from the graphql response

        Returns:
            dict: json with the format of {teacher_firstname+teacher_last_name : {department, id, legacyid, rating}}
        """
        professor_profiles = {}
        try:
            for edge in json["data"]["search"]["teachers"]["edges"]:
                # gathering information about each entry
                node = edge["node"]
                prof_rating = node["avgRating"]
                first_name = node["firstName"]
                last_name = node["lastName"]
                prof_legacyid = node["legacyId"]
                prof_department = node["department"]
                prof_profile = {
                    "department": prof_department,
                    "first_name": first_name,
                    "last_name": last_name,
                    "rating": str(prof_rating),
                }
                # Setting the key to which to access the profile of each professor, can change if needed
                professor_profiles[str(prof_legacyid)] = prof_profile
            # making sure we keep a bookmark to where we last searched
            self.cursor = json["data"]["search"]["teachers"]["pageInfo"]["endCursor"]
            self.parsed_department = not json["data"]["search"]["teachers"]["pageInfo"][
                "hasNextPage"
            ]
            return professor_profiles
        except Exception:
            return {}
