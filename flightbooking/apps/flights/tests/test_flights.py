import json
import random
import string

from rest_framework import status
from rest_framework.reverse import reverse

from flightbooking.apps.authentication.tests.test_auth import AuthenticatedTestCase


class BaseFlightsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.flight = {
                "flight": {
                    "name": "Boeing 12ABC",
                    "destination": "South Africa",
                    "departure_date": "2019-12-12",
                    "departure_time": "09:30[:00[.000000]]"
                }
        }
        self.url_list = reverse("flights:flights-list")

    def create_flight(self, flight=None):
        if flight is None:
            flight = self.flight
        response = self.client.post(self.url_list, data=flight, format="json")
        return json.loads(response.content)

    def url_retrieve(self, flight_id):
        return reverse("flights:flights-detail", kwargs={"flight_id": flight_id})


class CreateFlightsTestCase(BaseFlightsTestCase):
    """
    Test for the flights creation
    """

    def create_flight(self, flight=None):
        if flight is None:
            flight = self.flight
        return self.client.post(self.url_list, data=flight, format="json")

    def test_active_user_can_create_flight(self):
        response = self.create_flight()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_create_flight_without_logging_in(self):
        self.logout()
        response = self.create_flight()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            b"Authentication credentials were not provided.", response.content)

    def test_cannot_create_flight_without_name(self):
        self.flight['flight']['name'] = ''
        response = self.create_flight()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'The flight must have a name', response.content)

    def test_cannot_create_flight_without_destination(self):
        self.flight['flight']['destination'] = ''
        response = self.create_flight()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"The flight must have a destination", response.content)

    def test_cannot_create_flight_without_departure_date(self):
        self.flight['flight']['departure_date'] = ''
        response = self.create_flight()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Date has wrong format',
                      response.content)

    def test_name_cannot_be_more_than_255_characters(self):
        self.flight['flight']['name'] = ''.join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(256))
        response = self.create_flight()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            b'The flight name cannot be more than 255 characters', response.content)


class GetFlightsTestCase(BaseFlightsTestCase):

    def get_all_flights(self):
        response = self.client.get(self.url_list, data=None, format="json")
        return json.loads(response.content)['data']['flight']

    def get_single_flight(self, flight_id):
        return self.client.get(self.url_retrieve(flight_id), data=None, format="json")

    def test_user_can_get_created_flight(self):
        flight_id = self.create_flight()['flight_id']
        response = self.get_single_flight(flight_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_can_get_created_flight(self):
        flight_id = self.create_flight()['flight_id']
        self.logout()
        response = self.get_single_flight(flight_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateFlightTestCase(BaseFlightsTestCase):

    def update_flight(self, flight, flight_id):
        return self.client.put(self.url_retrieve(flight_id), data=flight, format="json")

    def test_can_update_flight_name(self):
        flight_id = self.create_flight()['flight_id']

        self.flight['flight']['name'] = "Boeing flight 254"
        response = self.update_flight(self.flight, flight_id=flight_id)
        self.assertIn(str.encode(
            self.flight['flight']['name']), response.content)

    def test_user_can_update_flight_destination(self):
        flight_id = self.create_flight()['flight_id']

        self.flight['flight']['destination'] = "Kansas City"
        response = self.update_flight(self.flight, flight_id=flight_id)

        self.assertIn(str.encode(
            self.flight['flight']['destination']), response.content)

    def test_user_can_update_flight_departure_time(self):
        flight_id = self.create_flight()['flight_id']

        self.flight['flight']['departure_time'] = "07:30:00"
        response = self.update_flight(self.flight, flight_id=flight_id)

        self.assertIn(str.encode(
            self.flight['flight']['departure_time']), response.content)

    def test_unauthenticated_user_cannot_edit_a_flight(self):
        flight_id = self.create_flight()['flight_id']
        self.logout()

        response = self.update_flight(self.flight, flight_id=flight_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_details_for_non_existing_flight(self):
        flight_id = 4

        response = self.update_flight(self.flight, flight_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteFlightTestCase(BaseFlightsTestCase):
    def delete_flight(self, flight_id):
        return self.client.delete(self.url_retrieve(flight_id), data=None, format="json")

    def test_delete_flight(self):
        flight_id = self.create_flight()['flight_id']

        response = self.delete_flight(flight_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            b'{"message":"The flight has successfully been deleted."}', response.content)

    def test_cannot_delete_a_flight_that_does_not_exist(self):
        flight_id = self.create_flight()['flight_id']
        self.delete_flight(flight_id)

        response = self.delete_flight(flight_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_delete_flight(self):
        flight_id = self.create_flight()['flight_id']
        self.logout()

        response = self.delete_flight(flight_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
