import requests
import json

url = "https://www.ratemyprofessors.com/graphql"

payload = "{\"query\":\"query TeacherSearchPaginationQuery(\\n  $count: Int!\\n  $cursor: String\\n  $query: TeacherSearchQuery!\\n) {\\n  search: newSearch {\\n    ...TeacherSearchPagination_search_1jWD3d\\n  }\\n}\\n\\nfragment TeacherSearchPagination_search_1jWD3d on newSearch {\\n  teachers(query: $query, first: $count, after: $cursor) {\\n    didFallback\\n    edges {\\n      cursor\\n      node {\\n        ...TeacherCard_teacher\\n        id\\n        __typename\\n      }\\n    }\\n    pageInfo {\\n      hasNextPage\\n      endCursor\\n    }\\n    resultCount\\n    filters {\\n      field\\n      options {\\n        value\\n        id\\n      }\\n    }\\n  }\\n}\\n\\nfragment TeacherCard_teacher on Teacher {\\n  id\\n  legacyId\\n  avgRating\\n  numRatings\\n  ...CardFeedback_teacher\\n  ...CardSchool_teacher\\n  ...CardName_teacher\\n  ...TeacherBookmark_teacher\\n}\\n\\nfragment CardFeedback_teacher on Teacher {\\n  wouldTakeAgainPercent\\n  avgDifficulty\\n}\\n\\nfragment CardSchool_teacher on Teacher {\\n  department\\n  school {\\n    name\\n    id\\n  }\\n}\\n\\nfragment CardName_teacher on Teacher {\\n  firstName\\n  lastName\\n}\\n\\nfragment TeacherBookmark_teacher on Teacher {\\n  id\\n  isSaved\\n}\\n\",\"variables\":{\"count\":10,\"cursor\":\"YXJyYXljb25uZWN0aW9uOjc=\",\"query\":{\"text\":\"\",\"schoolID\":\"U2Nob29sLTEzODE=\",\"fallback\":true,\"departmentID\":null}}}"
headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Authorization': 'Basic dGVzdDp0ZXN0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json',
  'Cookie': 'ccpa-notice-viewed-02=true; cid=5QXcDf7gCd-20240308',
  'Origin': 'https://www.ratemyprofessors.com',
  'Referer': 'https://www.ratemyprofessors.com/search/professors/1381?q=*',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
