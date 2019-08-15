from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from flightbooking.apps.authentication.models import User
from flightbooking.apps.profiles.models import Profile


class TestProfile(APITestCase):
    """
    Tests profile creation.
    """

    def setUp(self):
        self.register_url = reverse('authentication:user-register')
        self.get_all_url = reverse('profiles:get-profiles')
        username = 'chomba'
        self.get_profiles_url = reverse('profiles:profiles', kwargs={'username': username})
        self.login_url = reverse('authentication:user-login')

        self.user = {
            'user': {
                'username': 'chariss',
                'email': 'chariss@gmail.com',
                'password': 'charissU1@_}'
            }
        }
        self.user2 = {
            'user': {
                'username': 'chomba',
                'email': 'chomba@gmail.com',
                'password': 'chombaU1;>?+&'
            }}

        self.login = {
            'user': {
                'username': 'chomba1',
                'email': 'chomba2@gmail.com',
                'password': 'chombaU1^&*'
            }}
        # self.client.post(self.register_url, self.user, format="json")
        self.client.post(self.register_url, self.user2, format="json")


    def activate_user(self, email=None):
        email = self.login['user']['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

    def test_create_profile(self):
        """
        Tests whether a new profile object is created on registration
        """
        resp = self.client.post(self.register_url, self.user, format="json")
        current_users = User.objects.count()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), current_users)
        self.assertEqual(Profile.objects.count(), current_users)

    def test_get_all_profiles(self):
        self.client.post(self.register_url, self.login, format="json")
        self.activate_user()
        response = self.client.post(self.login_url, self.login, format="json")
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        res = self.client.get(self.get_all_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_profiles_unauthenticated(self):
        res = self.client.get(self.get_all_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_profile(self):
        self.client.post(self.register_url, self.login, format="json")
        self.activate_user()
        response = self.client.post(self.login_url, self.login, format="json")
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        res = self.client.get(self.get_profiles_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_single_profile_unauthenticated(self):
        res = self.client.get(self.get_profiles_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_profile_bio(self):
        self.client.post(self.register_url, self.login, format="json")
        self.activate_user()
        response = self.client.post(self.login_url, self.login, format="json")
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        res = self.client.put(self.get_profiles_url, data={'bio': 'This is some bio'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

