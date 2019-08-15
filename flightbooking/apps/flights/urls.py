from django.urls import path, include
from rest_framework.routers import DefaultRouter

from flightbooking.apps.flights.views import FlightAPIView, BookingAPIView, BookingUpdateDestroy

app_name = "flights"
router = DefaultRouter()
router.register('flights', FlightAPIView, base_name="flights")

urlpatterns = [
    path('', include(router.urls)),
    path('flights/<flight_id>/bookings/', BookingAPIView.as_view(), name='bookings'),
    path('flights/<flight_id>/bookings/<pk>', BookingUpdateDestroy.as_view(), name='booking'),
]
