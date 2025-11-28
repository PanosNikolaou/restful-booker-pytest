# Restful Booker API Automation Framework

## Overview
A professionally structured end-to-end API automation framework for the Restful Booker service using Python and pytest. The framework demonstrates modern API testing practices: OOP API clients, test isolation, configuration management, and extensible reporting.

## Objectives
- Validate API functionality via real HTTP requests
- Demonstrate a complete CRUD booking flow
- Provide a reusable API client abstraction
- Produce human-friendly reports for CI and local runs

## Technology Stack
- Python 3.10+
- pytest
- requests
- pydantic (for models/validation)
- pytest-html (optional, for HTML reports)
- allure-pytest (optional, for Allure reports)

## Prerequisites
- Git
- Python 3.10+
- Optional: Allure CLI for serving Allure reports

## Quickstart (local)
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Detailed Workflow
This section explains how the test harness works end-to-end so you can understand, extend, or troubleshoot the framework.

Overview
- All shared test fixtures, helpers and reporting hooks live in `conftest.py`.
- Tests in `tests/` consume fixtures via pytest's dependency injection.
- Real HTTP requests are performed with `requests` through a small wrapper fixture that records request/response details for debugging and reporting.

Key fixtures and responsibilities
- `base_url` (session scope)
  - Provides the API base URL. Defaults to `https://restful-booker.herokuapp.com`. Override by setting the `BASE_URL` environment variable.

- `token` (session scope)
  - Performs authentication by POSTing to `{BASE_URL}/auth` with credentials from `BOOKER_USER` and `BOOKER_PASS` (defaults `admin`/`password123`).
  - Calls `resp.raise_for_status()` so authorization failures stop the session early.
  - Caches the token for the whole test session to avoid repeated auth calls.

- `auth_headers` (function scope)
  - Builds headers used for protected operations that require authentication. Returns a dict such as:
    `{"Content-Type": "application/json", "Cookie": "token=<token>"}`
  - Important: the token is passed as a cookie (not a bearer header) because the API expects `Cookie: token=<token>`.

- `random_booking` (function scope)
  - Produces realistic booking payloads using `Faker` (firstname, lastname, price, dates, etc.).

- `api_request` (function scope)
  - Returns a helper function `_api_request(method, url, **kwargs)` which calls `requests.request(method, url, **kwargs)` and returns the `Response` object.
  - Before and after sending the HTTP request it formats a human-readable text block containing:
    - Request line (METHOD URL)
    - Request headers and body
    - Response status, headers and body
  - The helper appends those text blocks to `request.node.crud_logs` (a list) on the current pytest node. This preserves ordered call logs for each test.
  - Note: `api_request` does not automatically inject auth headers. Tests should pass `headers=auth_headers` for endpoints that require the auth cookie.

Pytest HTML integration
- If `pytest-html` is installed, the project attaches the recorded `request/response` blocks to the test's HTML report via the `pytest_runtest_makereport` hook.
- Each recorded API call is added as an HTML extra field (text) so you can inspect full request/response details per test in the generated report.

Example end-to-end test flow
- `test_full_crud_flow` (example in `tests/test_e2e_booking_flow.py`):
  1. CREATE — POST `/booking` with `random_booking` JSON. Expect HTTP 200 and extract `bookingid` from the response.
  2. READ — GET `/booking/{bookingid}`. Expect HTTP 200 and verify contents.
  3. UPDATE — PUT `/booking/{bookingid}` with updated JSON and `headers=auth_headers` (cookie token). Accept 200 or 201.
  4. VERIFY — GET `/booking/{bookingid}` and assert the update took effect.
  5. DELETE — DELETE `/booking/{bookingid}` with `headers=auth_headers`. Accept 200, 201, or 204 as success.

Design notes and rationale
- Token lifecycle: authentication is performed once per session and cached to speed up test runs. Tests remain deterministic as long as the external service state is managed.
- Logging: saving request/response blocks into `request.node.crud_logs` keeps debug info close to the test and allows attaching it to reports without changing test assertions.
- Explicit auth: tests decide where to include `auth_headers`. This makes it obvious which calls are protected and keeps `api_request` lightweight.

Environment variables and configuration
- BASE_URL — API base URL (default `https://restful-booker.herokuapp.com`)
- BOOKER_USER — username for `/auth` (default `admin`)
- BOOKER_PASS — password for `/auth` (default `password123`)

Running tests and generating reports
- Run the full test suite:
  ```bash
  pytest -q
  ```

- Run a single test (useful for debugging):
  ```bash
  pytest tests/test_e2e_booking_flow.py::test_full_crud_flow -q
  ```

- Create an HTML report (pytest-html):
  ```bash
  pip install pytest-html
  pytest --html=report.html --self-contained-html -q
  ```
  The HTML will include recorded API calls when pytest-html is available.

- Create Allure results (optional):
  ```bash
  pip install allure-pytest
  pytest --alluredir=allure-results
  allure serve allure-results
  ```

Using a custom stylesheet (assets/style.css)
- `assets/style.css` is provided to customize the generated HTML report look-and-feel.
- `pytest-html` supports `--self-contained-html` which embeds CSS into the report. If you prefer to inject a local stylesheet, add `--css=assets/style.css` to the pytest command if your pytest-html version supports it, or copy/merge the file into the generated HTML as a post-processing step in CI.

Notes, caveats and best practices
- These are integration tests that call a live endpoint. Flakiness can come from network issues or the external environment. Use CI environment variables and retries where appropriate.
- Do not commit secrets. Use environment variables or your CI secret manager for `BOOKER_USER` and `BOOKER_PASS`.
- Tests are written to be descriptive and intentionally accept multiple success status codes where the API may return different valid responses (e.g., 200 vs 201).
- If you need isolated unit tests for the API wrapper, add tests that mock `requests` (e.g., `responses` or `requests-mock`) and assert client behavior without hitting the network.

## Test matrix & configuration
- Project config is controlled via `pytest.ini`.
- Use `filterwarnings` in pytest.ini to manage test-time warnings.
- Add environment-specific settings or secrets via CI variables or a dedicated config module (do not commit secrets).

## Generating Reports

### HTML Report (pytest-html)
1. Install:
   ```bash
   pip install pytest-html
   ```
2. Run and produce an HTML report:
   ```bash
   pytest --html=report.html
   ```
3. Open `report.html` in your browser.

Notes:
- The framework attaches an "API calls" section into each test's HTML report when pytest-html is installed. This shows method, url, status, duration, and collapsed request/response details.

### Allure (optional, richer reports)
1. Install:
   ```bash
   pip install allure-pytest
   ```
2. Run tests and collect Allure results:
   ```bash
   pytest --alluredir=allure-results
   ```
3. Serve the report (requires Allure CLI):
   ```bash
   allure serve allure-results
   ```

## Test structure (recommended)
- tests/ — pytest test modules (unit & e2e). Each test should be independent.
- api/ — API client classes and models (pydantic) encapsulating endpoints.
- conftest.py — fixtures (authentication, session, API call recorder, config).
- utils/ — helpers, serializers, and fixtures reuse.

## Writing tests
- Use the API client to perform actions and assertions.
- Prefer small, focused tests; combine steps only for end-to-end scenarios.
- Use fixtures for setup/teardown and to share authenticated sessions.
- Example skeleton:
  ```python
  def test_create_and_get_booking(api_client):
      # example payload used for the test
      payload = {
          "firstname": "Alice",
          "lastname": "Smith",
          "totalprice": 100,
          "depositpaid": False,
          "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-05"}
      }
      booking = api_client.create_booking(payload)
      assert booking.id is not None
      fetched = api_client.get_booking(booking.id)
      assert fetched.firstname == payload["firstname"]
  ```

## Capturing API calls in HTML report
- The project includes a fixture that records requests made through `requests.Session.request` and attaches an "API calls" HTML table to the pytest-html report.
- Ensure `pytest-html` is installed to see this section. The HTML entry shows collapsed request/response headers and bodies for easy debugging.

## Troubleshooting
- Warning about `report.extra` deprecation: the project config uses pytest's `filterwarnings` to suppress noisy deprecation warnings from old plugin behavior. If you still see warnings, run pytest with increased verbosity and check `pytest.ini` filters.
- If HTML extras do not appear: confirm `pytest-html` is installed in the active environment.
- If tests fail due to environment variables or network: verify endpoint accessibility and any required credentials.

## Extending the framework
- Add more API client methods under `api/` as new endpoints are needed.
- Add test data factories or use pydantic models for consistent payload generation.
- Integrate CI (GitHub Actions/other) to run tests and archive reports.

## Contributing
- Open issues or PRs with clear descriptions.
- Write tests for new features and ensure existing tests keep passing.
- Keep code style consistent and avoid committing secrets.

## License

MIT License
