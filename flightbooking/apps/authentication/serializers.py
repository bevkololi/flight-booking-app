import re

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from .models import User, BlacklistedToken
from flightbooking.apps.profiles.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, error_messages={
        "required": "Email is required"
    })
    password = serializers.CharField(
        required=True, max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def validate_username(self, data):
        candidate_name = data
        try:
            if int(candidate_name):
                raise serializers.ValidationError(
                    {"username": ["Username cannot be numbers only"]})
        except ValueError:
            pass
        if candidate_name == "":
            raise serializers.ValidationError(
                {"username": ["Username is required!"]})
        elif User.objects.filter(username=candidate_name):
            raise serializers.ValidationError(
                {"username": ["Username already exists"]})
        elif len(candidate_name) < 4:
            raise serializers.ValidationError(
                {"username": ["Username should be more than 4 characters!"]})
        elif len(candidate_name) > 128:
            raise serializers.ValidationError(
                {"username": ["Username should not be longer than 128 characters"]})
        return data

    def validate_email(self, data):
        candidate_email = data
        if candidate_email == "":
            raise serializers.ValidationError(
                {"email": ["Email is required!"]})
        elif User.objects.filter(email=candidate_email):
            raise serializers.ValidationError(
                {"email": ["User with provided email exists! Please login!"]})
        return data
        
    def validate_password(self, data):
        candidate_password = data
        if candidate_password == "":
            raise serializers.ValidationError({
                "password": ["Password is required!"]})
        elif len(candidate_password) < 8:
            raise serializers.ValidationError({
                "password": ["Password should be at least eight (8) characters long!"]})
        elif len(candidate_password) > 128:
            raise serializers.ValidationError({
                "password": ["Password should not be longer than (128) characters long!"]})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=512, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        # if not user.is_active:
        #     raise serializers.ValidationError(
        #         'This user has been deactivated.'
        #     )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LogoutSerializer(serializers.ModelSerializer):
    """Performs logout serializer"""
    token = serializers.CharField(max_length=500)
