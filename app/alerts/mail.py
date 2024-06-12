import os
import requests

MAILGUN_API_URL = "https://api.mailgun.net/v3/brennen.dev/messages"


def send_course_alert(course: str, section: str):
    return requests.post(
        MAILGUN_API_URL,
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={
            "from": "Conquest <conquest@brennen.dev>",
            "to": ["Brennen Ho", "boho@usc.edu"],
            "subject": f"You're watching {course}",
            "text": f"Hello! You're now watching {course} section {section}.",
        },
    )
