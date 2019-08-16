from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from flightbooking.apps.authentication.models import User
from .models import Profile
from .serializers import ProfileSerializer
from .renderers import ProfileJSONRenderer


class ProfileListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def get(self, request, *args, **kwargs):
        try:
            queryset = Profile.objects.all().exclude(user=request.user)
        except Profile.DoesNotExist:
            raise Http404
        serializer = self.serializer_classes(queryset, many=True)
        return Response({'profiles': serializer.data}, status=status.HTTP_200_OK)


class ProfileGetView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def get_object(self, username):
        try:
            return Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, username):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise Http404
        serializer = self.serializer_classes(profile)
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        profile = self.get_object(username)
        serializer = self.serializer_classes(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
