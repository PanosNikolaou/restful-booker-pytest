"""
Smoke test for the RESTful Booker API health endpoint.

This simple test verifies the API ping/health endpoint responds as expected.

Note about __init__.py:
    The tests package may include an empty __init__.py to mark it as a package
    without adding initialization logic. This is intentional to keep test import
    side-effect free.
"""

from api.booking_api import BookingAPI
from config.config import BASE_URL

def test_healthcheck():
    # Instantiate the API client and call the health-check endpoint.
    api = BookingAPI(BASE_URL)
    response = api.health_check()
    # Expectations depend on the API: assert the returned status code matches the service contract.
    assert response.status_code == 201
