import requests

# Module docstring:
# Provides a lightweight HTTP client wrapper (BaseClient) used by API-specific
# client classes. It centralizes session handling and convenience methods for
# common HTTP verbs used in the project.

class BaseClient:
    """
    Base HTTP client for interacting with a REST API.

    Attributes:
        base_url (str): Base URL for the API (trailing slash is normalized away).
        session (requests.Session): Reused HTTP session for connection pooling,
                                    default headers and cookies.
    """

    def __init__(self, base_url: str):
        """
        Initialize the BaseClient.

        Args:
            base_url (str): Base URL of the target API. Any trailing slash is removed
                            to ensure consistent endpoint concatenation.
        """
        # Normalize base_url by removing trailing slash for consistent endpoint formation
        self.base_url = base_url.rstrip('/')
        # Use a persistent session for connection reuse and shared headers/cookies
        self.session = requests.Session()

    def set_token(self, token: str):
        """
        Set an authentication token on the session headers.

        This method updates the session headers so subsequent requests include the
        token as a cookie and set Content-Type to application/json by default.

        Args:
            token (str): Authentication token value to include in request cookies.
        """
        # Store token in Cookie header and set JSON content type for requests
        self.session.headers.update({
            "Cookie": f"token={token}",
            "Content-Type": "application/json"
        })

    def get(self, endpoint: str):
        """
        Send a GET request to the given endpoint.

        Args:
            endpoint (str): Path of the endpoint (should start with a slash).

        Returns:
            requests.Response: The raw response object from requests.
        """
        # Concatenate base_url and endpoint and perform GET
        return self.session.get(f"{self.base_url}{endpoint}")

    def post(self, endpoint: str, payload: dict):
        """
        Send a POST request with a JSON payload.

        Args:
            endpoint (str): Path of the endpoint (should start with a slash).
            payload (dict): JSON-serializable body to send.

        Returns:
            requests.Response: The raw response object from requests.
        """
        # Use json= to automatically serialize the payload and set appropriate header
        return self.session.post(f"{self.base_url}{endpoint}", json=payload)

    def put(self, endpoint: str, payload: dict):
        """
        Send a PUT request with a JSON payload (full resource replacement).

        Args:
            endpoint (str): Path of the endpoint (should start with a slash).
            payload (dict): JSON-serializable body to send.

        Returns:
            requests.Response: The raw response object from requests.
        """
        return self.session.put(f"{self.base_url}{endpoint}", json=payload)

    def patch(self, endpoint: str, payload: dict):
        """
        Send a PATCH request with a JSON payload (partial resource update).

        Args:
            endpoint (str): Path of the endpoint (should start with a slash).
            payload (dict): JSON-serializable partial data to send.

        Returns:
            requests.Response: The raw response object from requests.
        """
        return self.session.patch(f"{self.base_url}{endpoint}", json=payload)

    def delete(self, endpoint: str):
        """
        Send a DELETE request to the given endpoint.

        Args:
            endpoint (str): Path of the endpoint (should start with a slash).

        Returns:
            requests.Response: The raw response object from requests.
        """
        return self.session.delete(f"{self.base_url}{endpoint}")
