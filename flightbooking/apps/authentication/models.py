from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

import jwt
import os
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models


class UserManager(BaseUserManager):
    """
    create user and superuser functions
    """
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username')
        if email is None:
            raise TypeError('Users must have an email address')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers should have a password')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def token(self):
        """
        Generates the token and allows the token
        to be called by `user.token`
        :return string
        """
        token = jwt.encode(
            {
                "id": self.pk,
                "username": self.get_full_name,
                "email": self.email,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(minutes=int(os.getenv('TIME_DELTA')))
            },
            settings.SECRET_KEY, algorithm='HS256').decode()
        return token


class BlacklistedToken(models.Model):
    """this class stores blacklisted token"""

    token = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
