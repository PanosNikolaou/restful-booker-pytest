import requests

class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def set_token(self, token: str):
        self.session.headers.update({
            "Cookie": f"token={token}",
            "Content-Type": "application/json"
        })

    def get(self, endpoint: str):
        return self.session.get(f"{self.base_url}{endpoint}")

    def post(self, endpoint: str, payload: dict):
        return self.session.post(f"{self.base_url}{endpoint}", json=payload)

    def put(self, endpoint: str, payload: dict):
        return self.session.put(f"{self.base_url}{endpoint}", json=payload)

    def patch(self, endpoint: str, payload: dict):
        return self.session.patch(f"{self.base_url}{endpoint}", json=payload)

    def delete(self, endpoint: str):
        return self.session.delete(f"{self.base_url}{endpoint}")
