import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from flightbooking.apps.authentication.models import User
from flightbooking.apps.authentication.test_helper import make_user


class AuthenticationTestCase(APITestCase):
    """
    Extend this class in order to use the helper functions to login and sign up a user
    """

    def setUp(self):
        self.user = {
            "user": {
                "username": "beverly",
                "password": "password1U@#}",
                "email": "beverly@gmail.com"
            }
        }

    def register(self, user=None):
        if user is None:
            user = self.user
        return self.client.post(reverse("authentication:user-register"), data=user, format="json")


    def activate_user_make_staff(self, email=None):
        email = self.user['user']['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()


    def login(self, user=None):
        if user is None:
            user = self.user
        return self.client.post(reverse("authentication:user-login"), data=user, format="json")



class AuthenticatedTestCase(AuthenticationTestCase):
    """
    Extend this class in order to perform tests for an authenticated user
    """

    def setUp(self):
        super().setUp()
        """
        Register the user for further authentication
        :return:
        """
        self.register_and_login()

    def register_and_login(self, user=None):
        self.register(user)
        self.verify_user(None if user is None else user['user']['email'])
        self.login(user)

    def logout(self):
        """
        Unset the HTTP Authorization header whenever you need to use an unauthenticated user
        :return:
        """
        self.client.credentials(HTTP_AUTHORIZATION="")

    def login(self, user=None):
        """
        Login the user to the system and also set the authorization headers
        :param user:
        :return:
        """
        response = super().login(user)  # login the user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + (json.loads(response.content))['user']['token'])
        return response

    def get_current_user(self, email=None):
        return User.objects.get(email=email or self.user['user']['email'])

    def verify_user(self, email=None):
        """
        Verify the user
        :param email:
        :return:
        """
        if email is None:
            email = self.user['user']['email']
        user = User.objects.get(email=email)
        user.is_verified = True
        user.is_active = True
        user.is_staff = True
        user.save()

    def authenticate_another_user(self):
        """
        Helper method to authenticate another user
        :return:
        """
        self.register_and_login(user={"user": make_user()})

    def unverify_user(self, email=None):
        """
        Unverify a user's account in order to perform some tests
        :param email:
        :return:
        """
        if email is None:
            email = self.user['user']['email']
        user = User.objects.get(email=email)
        user.is_verified = False
        user.save()

    def get_authenticated_user(self):
        response = self.client.get(reverse("authentication:user-retrieve-update"))
        if response.status_code == 200:
            return User.objects.get(email=json.loads(response.content)['user']['email'])
        return None


class RegistrationViewTestCase(AuthenticationTestCase):
    """
    Tests if a user can be registered successfully with username, email and password
    """

    def test_user_can_register(self):
        """"
        Tests if user can register successfully
        """
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(json.loads(res.content)['user']['token'])
        self.assertEqual(json.loads(res.content)['user']['email'], self.user['user']['email'])

    def test_user_cannot_register_twice(self):
        """
        Test a user cannot register twice.
        """

        # registering a new user
        self.register()
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'{"user": {"username": ["Username already exists"]}}', res.content)

    def test_signup_without_username(self):
        """
        Test if a user can register without a username
        """
        self.user["user"]["username"] = ""
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Username is required!', res.content)

    def test_signup_with_username_shorter_than_4_chars(self):
        """
        Test if a user can register with a password shorter than 4 characters
        """
        self.user["user"]["username"] = "bev"
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'{"user": {"username": ["Username should be more than 4 characters!"]}}', res.content)

    def test_signup_with_username_longer_than_128_chars(self):
        """
        Test if a user can register with a password longer than 128 characters
        """
        self.user["user"]["username"] = """beverly is a very awesome team player
                                           so you should know her my friend because
                                           it is critical for you existence critical
                                           for you existence critical for you existencecritical
                                           for you existence"""
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'{"user": {"username": ["Username should not be longer than 128 characters"]}}', res.content)

    def test_signup_without_email(self):
        """
        Test if a user can register without an email
        """
        self.user["user"]["email"] = ""
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Email is required!', res.content)

    def test_signup_with_invalid_email(self):
        """
        Test if user cann register with invalid email
        """
        self.user["user"]["email"] = "beverly@gmail"
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'{"user": {"email": ["Enter a valid email address."]}}', res.content)

    def test_signup_without_password(self):
        """
        Test if a user can register without a password
        """
        self.user["user"]["password"] = ""
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Password is required!', res.content)

    def test_signup_with_password_shorter_than_8_chars(self):
        """
        Test if a user can register with a password with less than 4 characters
        """
        self.user["user"]["password"] = "short"
        res = self.register()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            b'{"user": {"password": ["Password should be at least eight (8) characters long!"]}}',
            res.content)



class LoginViewTestCase(AuthenticationTestCase):
    """
    Test for authentication in username and password login
    """

    def test_user_cannot_login_before_registering(self):
        """
        Test user cannot login before registering
        """
        res = self.login()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'A user with this email and password was not found.', res.content)

    def test_user_can_login(self):
        """
        Test user can login successfully
        """
        self.register()
        self.activate_user_make_staff()
        res = self.login()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(json.loads(res.content)['user']['token'])

    def test_no_token_header(self):
        self.register()
        self.client.credentials(HTTP_AUTHORIZATION="Token")
        res = self.login()
        self.assertIn(b'Invalid token header. No credentials provided', res.content)

    def test_invalid_token(self):
        self.register()
        self.client.credentials(HTTP_AUTHORIZATION="Token akljdflk i adfjadf ajdfl")
        res = self.login()
        self.assertIn(b'Invalid token header. Token string should not contain spaces', res.content)
