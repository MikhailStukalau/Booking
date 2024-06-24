from email.message import EmailMessage
from app.config import settings
from pydantic import EmailStr


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Booking confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1> Confirm your reservation </h1>
            You booked the hotel from {booking["date_from"]} to {booking["date_to"]}
        """,
        subtype="html"
    )

    return email
