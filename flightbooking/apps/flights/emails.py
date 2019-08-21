from django.core.mail import send_mail
import os
import datetime
from flightbooking.apps.flights.models import Flight, Booking


def send_reminder_email():
    from_email = os.getenv("EMAIL_HOST_SENDER")
    emails = get_people_with_bookings_tomorrow()
    send_mail(
        'Flight Booking Reminder',
        'Hello, this is just a polite reminder that you booked a flight with us for tomorrow. Please arrive on time.',
        from_email, emails,
        fail_silently=False)


def get_people_with_bookings_tomorrow():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    tomorrows_travellers_queryset = Booking.objects.filter(flight__departure_date=tomorrow)
    print_queryset = Booking.objects.filter(flight__departure_date='2019-08-22').query
    print(print_queryset)
    tomorrows_travellers = [i.traveller.email for i in tomorrows_travellers_queryset]
    return tomorrows_travellers


def get_people_with_bookings_for_flightid_one_and_given_date():
    travellers = Booking.objects.filter(flight__flight_id='1', flight__departure_date='2019-08-21')
    no_of_travellers = len(travellers)
    print({"No of travellers for that flight and day is: {}".format(no_of_travellers)})
    return no_of_travellers
