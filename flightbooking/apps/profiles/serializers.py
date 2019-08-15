from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes and deserializes Profile instances.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.ImageField(default=None)
    passport = serializers.ImageField(default=None)

    class Meta:
        model = Profile
        fields = ['username', 'image', 'passport']
