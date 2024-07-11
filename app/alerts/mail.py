import os
import requests

from app.utils.constants import MAILGUN_API_URL, SERVER_EMAIL

# Visit https://www.mailgun.com/ to generate an API key
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

# Mailgun API is limited to 100 emails/day on the free tier
# Will need to upgrade plan or setup a mail service to scale

# TODO: use HTML templates for emails


def send_watchlist_confirmation(email: str, section: str) -> requests.Response:
    """
    Send an email to the user confirming that they are now watching a section.
    """
    return requests.post(
        MAILGUN_API_URL,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Conquest <{SERVER_EMAIL}>",
            "to": [f"{email}"],
            "subject": f"You're watching {section}",
            "text": f"Hello! You're now watching section {section}.",
        },
    )


def send_course_alert(email: str, section: str, seats: int) -> requests.Response:
    """
    Send an email to the user alerting them that a section has available seats.
    """
    return requests.post(
        MAILGUN_API_URL,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Conquest <{SERVER_EMAIL}>",
            "to": [f"{email}"],
            "subject": f"Heads up: section {section} has available seats!",
            "text": f"Hello! Section {section} now has {seats} available seats. \n This section has been removed from your watchlist. Visit WebReg to re-add it.",
        },
    )


def send_password(email: str, password: str) -> requests.Response:
    """
    Send an email to the user with a one-time password.
    """
    return requests.post(
        MAILGUN_API_URL,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Conquest <{SERVER_EMAIL}>",
            "to": [f"{email}"],
            "subject": f"One-time password: {password}",
            "text": f"Hello! Your one-time password is {password}. This password will expire in 10 minutes.",
        },
    )
