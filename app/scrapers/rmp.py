import requests
import json
import codecs

BASE_URL = "https://www.ratemyprofessors.com/graphql"
PAYLOAD_PART_1 = '{"query":"query TeacherSearchPaginationQuery(\\n  $count: Int!\\n  $cursor: String\\n  $query: TeacherSearchQuery!\\n) {\\n  search: newSearch {\\n    ...TeacherSearchPagination_search_1jWD3d\\n  }\\n}\\n\\nfragment TeacherSearchPagination_search_1jWD3d on newSearch {\\n  teachers(query: $query, first: $count, after: $cursor) {\\n    didFallback\\n    edges {\\n      cursor\\n      node {\\n        ...TeacherCard_teacher\\n        id\\n        __typename\\n      }\\n    }\\n    pageInfo {\\n      hasNextPage\\n      endCursor\\n    }\\n    resultCount\\n    filters {\\n      field\\n      options {\\n        value\\n        id\\n      }\\n    }\\n  }\\n}\\n\\nfragment TeacherCard_teacher on Teacher {\\n  id\\n  legacyId\\n  avgRating\\n  numRatings\\n  ...CardFeedback_teacher\\n  ...CardSchool_teacher\\n  ...CardName_teacher\\n  ...TeacherBookmark_teacher\\n}\\n\\nfragment CardFeedback_teacher on Teacher {\\n  wouldTakeAgainPercent\\n  avgDifficulty\\n}\\n\\nfragment CardSchool_teacher on Teacher {\\n  department\\n  school {\\n    name\\n    id\\n  }\\n}\\n\\nfragment CardName_teacher on Teacher {\\n  firstName\\n  lastName\\n}\\n\\nfragment TeacherBookmark_teacher on Teacher {\\n  id\\n  isSaved\\n}\\n","variables":{"count":'
PAYLOAD_PART_2 = ',"cursor":"'
PAYLOAD_PART_3 = '","query":{"text":"","schoolID":"U2Nob29sLTEzODE=","fallback":true,"departmentID":null}}}'


class rmpParser:
    """
    Scrapes ratemyprofessor using graphql api payloads to load more professors a once.

    Defaults total number to scrape as 10 entries per scrape.
    """

    def __init__(self) -> None:

        self.payload = str
        self.cursor = str
        self.parsed_all = False
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Basic dGVzdDp0ZXN0",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://www.ratemyprofessors.com",
            "Referer": "https://www.ratemyprofessors.com/search/professors/1381?q=*",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

    def export_as_json():
        """Exports all professors at USC"""
        x = rmpParser()
        json_object = json.dumps(
            x.scrape_all_professors(), indent=4, ensure_ascii=False
        )
        with codecs.open("professors.json", "w", "utf-8") as outfile:
            outfile.write(json_object)

    def scrape_all_professors(self) -> dict:
        """Parses all professor at USC

        Returns:
            dict: json with the format of {teacher_firstname+teacher_last_name : {department, id, legacyid, rating}}
        """
        found_professors = {}
        found_professors.update(self.setup_scrape())
        while not self.parsed_all:
            found_professors.update(self.scrape_professors(100))
        return found_professors

    def setup_scrape(self) -> dict:
        """scrapes the first 8 professors on ratemyprofessor when it first loads

        Raises:
            RuntimeError: unable to send request to requested URL

        Returns:
            dict: formatted json for professor information. See parse_json() for more information.
        """
        first_payload = '{"query":"query TeacherSearchResultsPageQuery(\\n  $query: TeacherSearchQuery!\\n  $schoolID: ID\\n  $includeSchoolFilter: Boolean!\\n) {\\n  search: newSearch {\\n    ...TeacherSearchPagination_search_1ZLmLD\\n  }\\n  school: node(id: $schoolID) @include(if: $includeSchoolFilter) {\\n    __typename\\n    ... on School {\\n      name\\n    }\\n    id\\n  }\\n}\\n\\nfragment TeacherSearchPagination_search_1ZLmLD on newSearch {\\n  teachers(query: $query, first: 8, after: \\"\\") {\\n    didFallback\\n    edges {\\n      cursor\\n      node {\\n        ...TeacherCard_teacher\\n        id\\n        __typename\\n      }\\n    }\\n    pageInfo {\\n      hasNextPage\\n      endCursor\\n    }\\n    resultCount\\n    filters {\\n      field\\n      options {\\n        value\\n        id\\n      }\\n    }\\n  }\\n}\\n\\nfragment TeacherCard_teacher on Teacher {\\n  id\\n  legacyId\\n  avgRating\\n  numRatings\\n  ...CardFeedback_teacher\\n  ...CardSchool_teacher\\n  ...CardName_teacher\\n  ...TeacherBookmark_teacher\\n}\\n\\nfragment CardFeedback_teacher on Teacher {\\n  wouldTakeAgainPercent\\n  avgDifficulty\\n}\\n\\nfragment CardSchool_teacher on Teacher {\\n  department\\n  school {\\n    name\\n    id\\n  }\\n}\\n\\nfragment CardName_teacher on Teacher {\\n  firstName\\n  lastName\\n}\\n\\nfragment TeacherBookmark_teacher on Teacher {\\n  id\\n  isSaved\\n}\\n","variables":{"query":{"text":"","schoolID":"U2Nob29sLTEzODE=","fallback":true,"departmentID":null},"schoolID":"U2Nob29sLTEzODE=","includeSchoolFilter":true}}'
        response = requests.request(
            "POST", BASE_URL, headers=self.headers, data=first_payload
        )
        if response.status_code == 200:
            return self.parse_json(response.json())
        else:
            raise RuntimeError("Error parsing first setup of scrapes")

    def scrape_professors(self, count: int = 10) -> dict:
        """scrapes professor data from ratemyprofessor

        Args:
            count (int, optional): The number of professor entries to scrape. Defaults to 10.

        Returns:
            dict: Formatted json file for professor information. See parse_json() for more information.
        """
        self.payload = (
            PAYLOAD_PART_1 + str(count) + PAYLOAD_PART_2 + self.cursor + PAYLOAD_PART_3
        )
        response = requests.request(
            "POST", BASE_URL, headers=self.headers, data=self.payload
        )
        if response.status_code == 200:
            return self.parse_json(response.json())
        else:
            print("Error scraping")

    def parse_json(self, json: dict) -> dict:
        """parses graphql responses from ratemyprofessor to give streamline format to store

        Args:
            json (dict): json response file from the graphql response

        Returns:
            dict: json with the format of {teacher_firstname+teacher_last_name : {department, id, legacyid, rating}}
        """
        professor_profiles = {}
        for edge in json["data"]["search"]["teachers"]["edges"]:
            # gathering information about each entry
            node = edge["node"]
            prof_rating = node["avgRating"]
            first_name = node["firstName"]
            last_name = node["lastName"]
            prof_id = node["id"]
            prof_legacyid = node["legacyId"]
            prof_department = node["department"]
            prof_profile = {
                "department": prof_department,
                "id": prof_id,
                "legacyid": prof_legacyid,
                "rating": prof_rating,
            }
            # Setting the key to which to access the profile of each professor, can change if needed
            professor_profiles[first_name + last_name] = prof_profile
        # making sure we keep a bookmark to where we last searched
        self.cursor = json["data"]["search"]["teachers"]["pageInfo"]["endCursor"]
        self.parsed_all = not json["data"]["search"]["teachers"]["pageInfo"][
            "hasNextPage"
        ]
        return professor_profiles
