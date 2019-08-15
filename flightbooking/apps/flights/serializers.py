from rest_framework import serializers

from flightbooking.apps.flights.models import Flight, Booking
from flightbooking.apps.profiles.serializers import ProfileSerializer
from flightbooking.apps.profiles.models import Profile


class FlightSerializer(serializers.ModelSerializer):
    flight_id = serializers.IntegerField(required=False)
    name = serializers.CharField(
        max_length=255, allow_blank=True)
    destination = serializers.CharField(max_length=255)
    departure_date = serializers.DateField(required=False)
    departure_time = serializers.TimeField()

    class Meta:
        model = Flight
        fields = ['flight_id', 'name', 'destination', 'departure_date', 'departure_time']

    
    def create(self, validated_data):
        flight = Flight.objects.create(**validated_data)
        return flight

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate_flightname(self, data):
        if Flight.objects.filter(name=data):
            raise serializers.ValidationError(
                {'errors': "Flight name already exists"})
        return data

    


class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(required=False)
    traveller = serializers.SerializerMethodField(read_only=True)
    flight_seat = serializers.CharField(max_length=255)

    class Meta:
        model = Booking
        fields = ['booking_id', 'traveller', 'flight_seat']

    def get_traveller(self, obj):
        serializer = ProfileSerializer(
            instance=Profile.objects.get(user=obj.traveller)
        )
        return serializer.data