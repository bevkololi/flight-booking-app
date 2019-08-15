from django.db import models

from flightbooking.settings import AUTH_USER_MODEL
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    image = CloudinaryField("image")
    passport = CloudinaryField("image")


    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.username