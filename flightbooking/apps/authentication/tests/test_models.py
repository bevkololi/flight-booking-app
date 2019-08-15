from django.test import TestCase

from flightbooking.apps.authentication.models import (
    User
)


class UserModelTest(TestCase):
    """
    This tests the User model class, ability to create a user and create a super user.

    """

    def test_create_user(self):
        """
        Checks whether a user can be created with username email and password
        :return:
        """
        self.assertIsInstance(
            User.objects.create_user(username="username", email="username@mail.com", password="password"), User)

    def test_cannot_create_user_without_email(self):
        """
        Ensure a user cannot be created without an email
        :return:
        """
        with self.assertRaises(TypeError):
            User.objects.create_user(username="username", password="password", email=None)

    def test_create_superuser(self):
        """
        Ensure a superuser can be created
        :return:
        """
        user = User.objects.create_superuser(username="admin", email="admin@admin.com", password="password")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_cannot_create_superuser_without_password(self):
        """
        Ensures a superuser must have a password
        :return:
        """
        with self.assertRaises(TypeError):
            User.objects.create_superuser(username="admin", email="admin@admin.com")
