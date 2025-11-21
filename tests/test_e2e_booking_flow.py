# python
# File: `conftest.py`
import os
import json
import requests
import pytest
from faker import Faker

# optional import for pytest-html extras
try:
    from pytest_html import extras as html_extras
except Exception:
    html_extras = None

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
fake = Faker()
_token = None

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def token():
    global _token
    if _token:
        return _token
    resp = requests.post(f"{BASE_URL}/auth", json={"username": os.getenv("BOOKER_USER", "admin"),
                                                   "password": os.getenv("BOOKER_PASS", "password123")})
    resp.raise_for_status()
    _token = resp.json().get("token")
    return _token

@pytest.fixture
def auth_headers(token):
    return {"Content-Type": "application/json", "Cookie": f"token={token}"}

@pytest.fixture
def random_booking():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(50, 500),
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-05"},
        "additionalneeds": "Breakfast"
    }

@pytest.fixture
def api_request(request):
    """
    Returns a function to perform HTTP requests and record detailed
    request/response text into `request.node.crud_logs` for the current test.
    """
    def _api_request(method, url, **kwargs):
        method_u = method.upper()
        req_headers = kwargs.get("headers", {})
        req_body = kwargs.get("json", kwargs.get("data", None))
        try:
            req_body_text = json.dumps(req_body, indent=2, default=str) if isinstance(req_body, (dict, list)) else str(req_body)
        except Exception:
            req_body_text = str(req_body)

        parts = []
        parts.append(f"Request: {method_u} {url}")
        parts.append("Request headers:\n" + (json.dumps(req_headers, indent=2) if req_headers else "<empty>"))
        parts.append("Request body:\n" + (req_body_text or "<empty>"))

        resp = requests.request(method_u, url, **kwargs)

        try:
            resp_json = resp.json()
            resp_body_text = json.dumps(resp_json, indent=2)
        except Exception:
            resp_body_text = resp.text

        parts.append(f"Response status: {resp.status_code}")
        parts.append("Response headers:\n" + json.dumps(dict(resp.headers), indent=2))
        parts.append("Response body:\n" + (resp_body_text or "<empty>"))

        text = "\n\n".join(parts)

        if not hasattr(request.node, "crud_logs"):
            request.node.crud_logs = []
        request.node.crud_logs.append(text)

        return resp

    return _api_request

# attach recorded logs to pytest-html report (if pytest-html is installed)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and hasattr(item, "crud_logs") and html_extras is not None:
        extras = getattr(report, "extra", [])
        for i, txt in enumerate(item.crud_logs):
            extras.append(html_extras.text(txt, name=f"API Call {i+1}"))
        report.extra = extras

# --------------------------------------------------------------------
# Example of using `api_request` in a test (update your existing test to use this)
# File: `tests/test_e2e_booking_flow.py` (snippet)
def test_full_crud_flow(base_url, auth_headers, random_booking, api_request):
    # CREATE
    r = api_request("post", f"{base_url}/booking", json=random_booking, headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    bookingid = r.json().get("bookingid")
    assert bookingid is not None

    # READ
    r = api_request("get", f"{base_url}/booking/{bookingid}")
    assert r.status_code == 200

    # UPDATE
    updated = dict(random_booking, firstname="UpdatedName")
    r = api_request("put", f"{base_url}/booking/{bookingid}", json=updated, headers=auth_headers)
    assert r.status_code in (200, 201)

    # VERIFY
    r = api_request("get", f"{base_url}/booking/{bookingid}")
    assert r.status_code == 200
    assert r.json().get("firstname") == "UpdatedName"

    # DELETE
    r = api_request("delete", f"{base_url}/booking/{bookingid}", headers=auth_headers)
    assert r.status_code in (200, 201, 204)
