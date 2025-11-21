from api.client import BaseClient

# Module-level docstring:
# This module provides a BookingAPI client that wraps the RESTful Booker API endpoints.
# It extends BaseClient to reuse common HTTP methods (get, post, put, patch, delete)
# and offers convenience methods for auth, booking CRUD, and health checks.

class BookingAPI(BaseClient):
    """
    BookingAPI client.

    Inherits:
        BaseClient: provides low-level HTTP methods (get, post, put, patch, delete).

    Purpose:
        Provide convenient, well-documented methods for interacting with the booking API:
        - create authentication token
        - create, retrieve, update, partially update, delete bookings
        - perform a health check (ping)
    """

    def create_token(self, username: str, password: str):
        """
        Create an authentication token for a user.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.

        Returns:
            The response from BaseClient.post. Depending on BaseClient, this may be a
            requests.Response or a parsed JSON/dict containing the token.
        """
        # Send credentials to the auth endpoint to receive a token
        return self.post("/auth", {
            "username": username,
            "password": password
        })

    def create_booking(self, booking_data: dict):
        """
        Create a new booking.

        Args:
            booking_data (dict): Booking payload expected by the API (e.g., firstname, lastname,
                                 totalprice, depositpaid, bookingdates, additionalneeds).

        Returns:
            The response from BaseClient.post for the /booking endpoint (created booking).
        """
        # Post booking payload to create a new booking
        return self.post("/booking", booking_data)

    def get_booking(self, booking_id: int):
        """
        Retrieve a booking by ID.

        Args:
            booking_id (int): The ID of the booking to retrieve.

        Returns:
            The response from BaseClient.get for the /booking/{id} endpoint (booking details).
        """
        # Fetch booking details
        return self.get(f"/booking/{booking_id}")

    def update_booking(self, booking_id: int, booking_data: dict):
        """
        Replace an existing booking with new data.

        Args:
            booking_id (int): The ID of the booking to update.
            booking_data (dict): Full booking payload to replace the existing booking.

        Returns:
            The response from BaseClient.put for the /booking/{id} endpoint.
        """
        # Perform a full update (PUT) of the booking resource
        return self.put(f"/booking/{booking_id}", booking_data)

    def partial_update(self, booking_id: int, data: dict):
        """
        Partially update an existing booking.

        Args:
            booking_id (int): The ID of the booking to partially update.
            data (dict): Partial fields to update (e.g., {"firstname": "NewName"}).

        Returns:
            The response from BaseClient.patch for the /booking/{id} endpoint.
        """
        # Perform a partial update (PATCH) of the booking resource
        return self.patch(f"/booking/{booking_id}", data)

    def delete_booking(self, booking_id: int):
        """
        Delete a booking by ID.

        Args:
            booking_id (int): The ID of the booking to delete.

        Returns:
            The response from BaseClient.delete for the /booking/{id} endpoint.
        """
        # Delete the booking resource
        return self.delete(f"/booking/{booking_id}")

    def health_check(self):
        """
        Check API health/status.

        Returns:
            The response from BaseClient.get for the /ping endpoint. Useful in tests to
            verify the service is reachable.
        """
        # Simple ping endpoint to verify service availability
        return self.get("/ping")
