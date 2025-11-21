"""
Pytest test-support utilities.

Provides:
- an autouse fixture that wraps requests.Session.request to record API calls for each test,
  storing the details on the pytest node for later consumption by reporting hooks.
- a pytest_runtest_makereport hook that appends captured API-call HTML to pytest-html reports.

Note about __init__.py:
    The project package __init__.py files are intentionally empty; they exist solely
    to mark directories as importable packages and avoid executing package-level logic.
"""

import time
import json
import html as html_lib
from typing import List, Dict, Any
import pytest
import requests

# try to import pytest_html extras; if not available, we'll skip attaching HTML
try:
    from pytest_html import extras
except Exception:
    extras = None

@pytest.fixture(autouse=True)
def record_api_calls(request):
    """
    Autouse fixture that wraps requests.Session.request and records each API call.
    Stores the list on the test node as `_api_calls`.
    """
    calls: List[Dict[str, Any]] = []
    original_request = requests.Session.request

    def _safe_text(obj):
        try:
            if obj is None:
                return ""
            if isinstance(obj, (dict, list)):
                return json.dumps(obj, indent=2, ensure_ascii=False)
            return str(obj)
        except Exception:
            return "<unserializable>"

    def _wrap_request(self, method, url, *args, **kwargs):
        start = time.time()
        resp = None
        exc = None
        try:
            resp = original_request(self, method, url, *args, **kwargs)
            return resp
        except Exception as e:
            exc = e
            raise
        finally:
            duration = time.time() - start
            # gather request info
            req_body = kwargs.get("json") if "json" in kwargs else kwargs.get("data", "")
            req_headers = kwargs.get("headers", {}) or {}
            # gather response info
            if resp is not None:
                try:
                    resp_text = resp.text
                except Exception:
                    resp_text = "<non-text response>"
                status = getattr(resp, "status_code", None)
                resp_headers = dict(getattr(resp, "headers", {}) or {})
            else:
                resp_text = "<no response due to exception>" if exc else "<no response>"
                status = None
                resp_headers = {}
            calls.append({
                "method": method,
                "url": url,
                "status": status,
                "duration": duration,
                "request_body": _safe_text(req_body),
                "request_headers": dict(req_headers),
                "response_body": _safe_text(resp_text),
                "response_headers": resp_headers,
                "exception": str(exc) if exc else ""
            })

    # patch
    requests.Session.request = _wrap_request

    # Clarification: record_api_calls attaches its list to `request.node._api_calls` so
    # pytest hooks can read it after the test run and include the info in reports.
    # Attach to node BEFORE yielding so pytest_runtest_makereport can access it
    try:
        request.node._api_calls = calls
    except Exception:
        pass

    yield calls

    # restore
    requests.Session.request = original_request

    # clean up attribute (optional)
    try:
        del request.node._api_calls
    except Exception:
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to append API call details to the pytest-html report for the 'call' phase.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    calls = getattr(item, "_api_calls", None)
    if not calls:
        return

    if extras is None:
        # pytest-html not installed, skip attaching HTML
        return

    def esc(s):
        return html_lib.escape(str(s or ""))

    # Build a compact HTML table
    rows = []
    for c in calls:
        rows.append(
            "<tr>"
            f"<td style='white-space:nowrap'><strong>{esc(c['method'])}</strong></td>"
            f"<td style='max-width:600px;word-break:break-all'>{esc(c['url'])}</td>"
            f"<td>{esc(c['status'])}</td>"
            f"<td>{esc(round(c['duration'], 3))}s</td>"
            f"<td><details><summary>request</summary><pre>{esc(c['request_headers'])}\n\n{esc(c['request_body'])}</pre></details></td>"
            f"<td><details><summary>response</summary><pre>{esc(c['response_headers'])}\n\n{esc(c['response_body'])}</pre></details></td>"
            f"</tr>"
        )

    html = (
        "<div><h3>API calls</h3>"
        "<table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse'>"
        "<thead><tr><th>Method</th><th>URL</th><th>Status</th><th>Duration</th><th>Request</th><th>Response</th></tr></thead>"
        "<tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )

    # Use the new 'extras' attribute when available; fall back to deprecated 'extra'
    current_extras = getattr(report, "extras", None)
    if current_extras is None:
        # fallback for older pytest-html versions
        current_extras = getattr(report, "extra", None) or []
        use_attr = "extra"
    else:
        use_attr = "extras"

    current_extras.append(extras.html(html))

    if use_attr == "extras":
        report.extras = current_extras
    else:
        report.extra = current_extras
