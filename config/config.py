"""
Module: configuration constants for tests and API clients.

Keep secrets out of source control in real projects; this file is intended for example/demo usage.

Note about __init__.py:
    The package __init__.py is intentionally left empty so the config package is
    importable without executing package-level code. This prevents unexpected
    side-effects and keeps configuration loading explicit.
"""

BASE_URL = "https://restful-booker.herokuapp.com"  # Base URL of the RESTful Booker API used in tests
USERNAME = "admin"                                 # Default admin username used by tests/fixtures
PASSWORD = "password123"                           # Default password used by tests/fixtures
