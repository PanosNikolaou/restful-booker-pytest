from api.booking_api import BookingAPI
from config.config import BASE_URL

def test_healthcheck():
    api = BookingAPI(BASE_URL)
    response = api.health_check()
    assert response.status_code == 201
