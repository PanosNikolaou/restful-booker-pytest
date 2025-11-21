"""
Data models for the RESTful Booker API.

This module defines Pydantic models used to validate and document booking-related
payloads exchanged with the API. Use these models in tests or client code to
ensure payloads conform to the expected schema.

Note about __init__.py:
    The package-level __init__.py file is intentionally empty in this project.
    An empty __init__.py simply marks the directory as a Python package and
    avoids side-effects during import. Keeping it empty is a recommended practice
    when no package initialization logic is required.
"""

from pydantic import BaseModel

class BookingDates(BaseModel):
    """
    Booking date range.

    Attributes:
        checkin (str): Check-in date as an ISO-8601 date string (e.g. "2023-01-01").
        checkout (str): Check-out date as an ISO-8601 date string (e.g. "2023-01-05").
    """
    # Date the guest checks in (ISO date string)
    checkin: str
    # Date the guest checks out (ISO date string)
    checkout: str

class Booking(BaseModel):
    """
    Full booking payload.

    Attributes:
        firstname (str): Guest's first name.
        lastname (str): Guest's last name.
        totalprice (int): Total price for the booking in the API's currency unit.
        depositpaid (bool): Whether a deposit has been paid.
        bookingdates (BookingDates): Nested booking dates object with checkin/checkout.
        additionalneeds (str): Optional free-text for additional requirements (e.g. "Breakfast").
    """
    # Guest personal details
    firstname: str
    lastname: str

    # Booking financials and flags
    totalprice: int
    depositpaid: bool

    # Nested model representing the booking period
    bookingdates: BookingDates

    # Any optional additional requirements for the booking
    additionalneeds: str
