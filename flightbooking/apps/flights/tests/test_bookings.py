import json
import random
import string

from rest_framework import status
from rest_framework.reverse import reverse
from flightbooking.apps.authentication.tests.test_auth import AuthenticatedTestCase
from flightbooking.apps.flights.tests.test_flights import BaseFlightsTestCase


class BaseBookingsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.booking = {
            "booking": {
                "flight_seat": "First Class"
            }
        }

        self.flight = {
            "flight": {
                "name": "Boeing 12ABC",
                "destination": "South Africa",
                "departure_date": "2019-12-12",
                "departure_time": "09:30[:00[.000000]]"
            }
        }
        self.url_flights = reverse("flights:flights-list")

    def url_list(self, flight_id):
        return reverse("flights:bookings", kwargs={"flight_id": flight_id})

    def create_flight(self, flight=None):
        if flight is None:
            flight = self.flight
        response = self.client.post(
            self.url_flights, data=flight, format="json")

        return json.loads(response.content)

    def create_booking(self, flight_id, booking=None):
        if booking is None:
            booking = self.booking
        return self.client.post(self.url_list(flight_id), data=booking, format="json")

    def url_retrieve(self, flight_id, pk):
        return reverse("flights:booking", kwargs={"flight_id": flight_id, "pk": pk})


class CreateBookingsTestCase(BaseBookingsTestCase):
    """
    Test for the bookings creation
    """

    def test_active_user_can_create_booking(self):
        flight_id = self.create_flight()['flight_id']
        response = self.create_booking(flight_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_create_booking_without_logging_in(self):
        self.logout()
        flight_id = 1
        response = self.create_booking(flight_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_booking_without_flight_seat(self):
        self.booking['booking']['flight_seat'] = ''
        flight_id = self.create_flight()['flight_id']
        response = self.create_booking(flight_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_booking_without_destination(self):
        self.booking['booking']['flight_seat'] = ''
        flight_id = self.create_flight()['flight_id']
        response = self.create_booking(flight_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            b'{"flight_seat":["The booking must have a flight seat"]}', response.content)


class GetBookingsTestCase(BaseBookingsTestCase):

    def get_all_bookings(self):
        response = self.client.get(self.url_list, data=None, format="json")
        return json.loads(response.content)['data']['booking']

    def get_single_booking(self, flight_id, pk):
        return self.client.get(self.url_retrieve(flight_id, pk), data=None, format="json")

    def test_user_can_get_created_booking(self):
        flight_id = self.create_flight()['flight_id']
        booking = self.create_booking(flight_id)
        booking_id = json.loads(booking.content)['booking_id']
        response = self.get_single_booking(flight_id, booking_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_get_created_booking(self):
        flight_id = self.create_flight()['flight_id']
        booking = self.create_booking(flight_id)
        booking_id = json.loads(booking.content)['booking_id']
        self.logout()
        response = self.get_single_booking(flight_id, booking_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdatebookingTestCase(BaseBookingsTestCase):

    def update_booking(self, booking, flight_id, booking_id):
        return self.client.put(self.url_retrieve(flight_id, booking_id), data=booking, format="json")

    def test_can_update_booking_flight_seat(self):
        flight_id = self.create_flight()['flight_id']
        booking = self.create_booking(flight_id)
        booking_id = json.loads(booking.content)['booking_id']
        self.booking['booking']['flight_seat'] = "Window Seat"
        response = self.update_booking(
            self.booking, flight_id=flight_id, booking_id=booking_id)
        self.assertIn(str.encode(
            self.booking['booking']['flight_seat']), response.content)

    def test_unauthenticated_user_cannot_edit_a_booking(self):
        flight_id = self.create_flight()['flight_id']
        booking = self.create_booking(flight_id)
        booking_id = json.loads(booking.content)['booking_id']
        self.logout()

        response = self.update_booking(
            self.booking, flight_id=flight_id, booking_id=booking_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_details_for_non_existing_booking(self):
        booking_id = 4
        flight_id = 1

        response = self.update_booking(self.booking, flight_id, booking_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeletebookingTestCase(BaseBookingsTestCase):
    def delete_booking(self, flight_id, booking_id):
        return self.client.delete(self.url_retrieve(flight_id, booking_id), data=None, format="json")

    def test_delete_booking(self):
        flight_id = self.create_flight()['flight_id']
        booking = self.create_booking(flight_id)
        booking_id = json.loads(booking.content)['booking_id']

        response = self.delete_booking(flight_id, booking_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            b'{"message":"The booking has been deleted"}', response.content)

    def test_cannot_delete_a_booking_that_does_not_exist(self):
        flight_id = self.create_flight()['flight_id']
        booking = self.create_booking(flight_id)
        booking_id = 7

        response = self.delete_booking(flight_id, booking_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_delete_booking(self):
        flight_id = self.create_flight()['flight_id']
        booking = self.create_booking(flight_id)
        booking_id = json.loads(booking.content)['booking_id']
        self.logout()

        response = self.delete_booking(flight_id, booking_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
