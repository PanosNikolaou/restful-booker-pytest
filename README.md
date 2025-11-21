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
