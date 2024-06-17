import os
import requests

MAILGUN_API_URL = "https://api.mailgun.net/v3/brennen.dev/messages"

# use mailgun api to send emails


def send_watchlist_confirmation(email: str, section: str) -> requests.Response:
    return requests.post(
        MAILGUN_API_URL,
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={
            "from": "Conquest <conquest@brennen.dev>",
            "to": [f"{email}"],
            "subject": f"You're watching {section}",
            "text": f"Hello! You're now watching section {section}.",
        },
    )


def send_course_alert(email: str, section: str, seats: int) -> requests.Response:
    return requests.post(
        MAILGUN_API_URL,
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={
            "from": "Conquest <conquest@brennen.dev>",
            "to": [f"{email}"],
            "subject": f"Heads up: section {section} has available seats!",
            "text": f"Hello! Section {section} now has {seats} available seats. \n This section has been removed from your watchlist. Visit WebReg to re-add it.",
        },
    )
