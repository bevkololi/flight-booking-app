from rest_framework.renderers import JSONRenderer
from rest_framework import status, viewsets, generics
from rest_framework import mixins
from django.db import models
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from flightbooking.apps.flights.models import Flight, Booking
from flightbooking.apps.flights.serializers import FlightSerializer, BookingSerializer
from flightbooking.apps.authentication.models import User
from flightbooking.apps.authentication.serializers import UserSerializer
from flightbooking.apps.profiles.models import Profile
from flightbooking.apps.profiles.serializers import ProfileSerializer
from flightbooking.apps.flights.pagination import StandardResultsSetPagination


class FlightAPIView(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'flight_id'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,)
    queryset = Flight.objects.all()
    renderer_names = ('flight', 'flights')
    serializer_class = FlightSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        flight = request.data.get('flight', {})
        serializer = self.serializer_class(data=flight, partial=True)
        serializer.validate_flightname(flight['name'])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        flight_id = kwargs['flight_id']

        flight = Flight.objects.filter(flight_id=flight_id).first()
        if flight is None:
            return Response({
                'errors': 'Flight does not exist'
            }, status.HTTP_404_NOT_FOUND)
        elif not request.user.is_staff:
            return Response({
                'errors': 'You are not allowed to modify these details'
            })
        serializer = self.serializer_class(
            flight, data=request.data.get('flight', {}), partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        flight_id = kwargs['flight_id']

        flight = Flight.objects.filter(flight_id=flight_id).first()
        if flight is None:
            return Response({
                'errors': 'Flight does not exist'
            }, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            flight, context={'request': request}
        )
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        flights = Flight.objects.all()

        page = self.paginate_queryset(flights)
        serializer = self.serializer_class(
            page,
            context={
                'request': request
            },
            many=True
        )
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(self, request, *args, **kwargs)

        return Response({'message': 'The flight has successfully been deleted.'})


    
class BookingAPIView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,)
    renderer_names = ('booking', 'bookings')
    lookup_url_kwarg = 'flight_id'
    lookup_field = 'flight__flight_id'
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        flight_id = self.kwargs['flight_id']
        try:
            flight = Flight.objects.get(flight_id=flight_id)
        except Flight.DoesNotExist:
            data = {"errors": "This flight does not exist!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            data=request.data.get('booking', {}))
        serializer.is_valid(raise_exception= True)
        serializer.save(flight=flight, traveller=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, *args, **kwargs):
        flight_id = self.kwargs['flight_id']
        try:
            flight = Flight.objects.get(flight_id=flight_id)
        except Flight.DoesNotExist:
            data = {"errors": "This flight does not exist!"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        bookings = Booking.objects.filter(flight__flight_id=flight_id)
        page = self.paginate_queryset(bookings)
        serializer = self.serializer_class(
            page,
            context={
                'request': request
            },
            many=True
        )
        return self.get_paginated_response(serializer.data)


class BookingUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset =Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,)
    renderer_names = ('booking', 'bookings')
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        flight_id = kwargs['flight_id']
        try:
            flight = Flight.objects.get(flight_id=flight_id)
        except Flight.DoesNotExist:
            return Response({
                'error': 'Flight does not exist'
            }, status.HTTP_404_NOT_FOUND)
        try:
            pk = self.kwargs.get('pk')
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            message = {"error": "Booking with this ID does not exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)

        booking = Booking.objects.filter(pk=pk).first()
        serializer = self.serializer_class(
            booking, data=request.data.get('booking', {}), partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(flight=flight, traveller=request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        flight_id= kwargs['flight_id']
        try:
            flight = Flight.objects.get(flight_id=flight_id)
        except Flight.DoesNotExist:
            return Response({
                'error': 'Flight does not exist'
            }, status.HTTP_404_NOT_FOUND)
        try:
            pk = self.kwargs.get('pk')
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            message = {"error": "Booking with this ID does not exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)
        booking = Booking.objects.filter(pk=pk).first()
        booking.delete()
        return Response({'message': 'The booking has been deleted'})