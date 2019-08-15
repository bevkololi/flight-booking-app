import os

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from requests.exceptions import HTTPError

from .renderers import UserJSONRenderer


from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, LogoutSerializer
)
from flightbooking.apps.profiles.serializers import ProfileSerializer
from .models import User, BlacklistedToken
from flightbooking.apps.profiles.models import Profile
from rest_framework import authentication


class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.validate_username(user["username"])
        serializer.validate_email(user["email"])
        serializer.validate_password(user["password"])

        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=user['email'])

        resp = ProfileSerializer(user.profile).data
        resp['token'] = serializer.data['token']

        return Response(resp, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=user, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """this class logs out a user"""

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def delete(self, request):
        token = authentication.get_authorization_header(request).split()[
            1].decode()
        data = request.data
        data['token'] = token
        if BlacklistedToken.objects.filter(token=token).first():
            return Response({"success": "You have already logged out"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Succesfully logged out"}, status=status.HTTP_200_OK)


class UsersAPIView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    queryset = Profile.objects.all()
