import json
import os
import smtplib
from email.mime.text import MIMEText

from app.config import (
    EMAIL_FROM,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_USE_TLS,
)
from celery import Celery

app = Celery(
    "tasks", broker=os.environ.get("REDIS_URL"), backend=os.environ.get("REDIS_URL")
)


@app.task
def send_email_notification(transaction_details: dict):
    """Send an email notification about a new"""
    subject = "New Transaction Notification"
    body = f"A new transaction has been made:\n\n{json.dumps(transaction_details)}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_FROM

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            if EMAIL_USE_TLS:
                server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_FROM, [EMAIL_FROM], msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
