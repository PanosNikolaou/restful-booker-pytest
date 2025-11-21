import pytest
from api.booking_api import BookingAPI
from config.config import BASE_URL, USERNAME, PASSWORD

@pytest.fixture(scope="session")
def api():
    return BookingAPI(BASE_URL)

@pytest.fixture(scope="session")
def auth_token(api):
    response = api.create_token(USERNAME, PASSWORD)
    token = response.json()["token"]
    api.set_token(token)
    return token

def test_full_crud_flow(api, auth_token):
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-10",
            "checkout": "2025-01-15"
        },
        "additionalneeds": "Breakfast"
    }

    create_response = api.create_booking(booking_data)
    assert create_response.status_code == 200

    booking_id = create_response.json()["bookingid"]

    assert api.get_booking(booking_id).status_code == 200
    assert api.update_booking(booking_id, booking_data).status_code == 200
    assert api.partial_update(booking_id, {"lastname": "Smith"}).status_code == 200
    assert api.delete_booking(booking_id).status_code == 201
