import json
import requests
import time

from app.utils.constants import CLASS_API_BASE, SEMESTER
from app.utils.logger import get_logger


class CourseClient:
    def get_department(self, dep: str):
        start = time.time()
        response = requests.get(CLASS_API_BASE + dep + "/" + SEMESTER)
        print(json.loads(response.text))
        print(time.time() - start)
        return response.text
