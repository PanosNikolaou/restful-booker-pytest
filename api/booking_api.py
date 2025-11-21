from api.client import BaseClient

class BookingAPI(BaseClient):
    def create_token(self, username: str, password: str):
        return self.post("/auth", {
            "username": username,
            "password": password
        })

    def create_booking(self, booking_data: dict):
        return self.post("/booking", booking_data)

    def get_booking(self, booking_id: int):
        return self.get(f"/booking/{booking_id}")

    def update_booking(self, booking_id: int, booking_data: dict):
        return self.put(f"/booking/{booking_id}", booking_data)

    def partial_update(self, booking_id: int, data: dict):
        return self.patch(f"/booking/{booking_id}", data)

    def delete_booking(self, booking_id: int):
        return self.delete(f"/booking/{booking_id}")

    def health_check(self):
        return self.get("/ping")
