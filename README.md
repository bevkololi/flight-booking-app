[![Build Status](https://travis-ci.org/bevkololi/flight-booking-app.svg?branch=master)](https://travis-ci.org/bevkololi/flight-booking-app)
[![Coverage Status](https://coveralls.io/repos/github/bevkololi/flight-booking-app/badge.svg?branch=master)](https://coveralls.io/github/bevkololi/flight-booking-app?branch=master)

# flight-booking-app
A Django application to enable users to book available flights.


## How to test the application
- Clone the application
- Create and activate virtual environment
- Install requirements by running `pip install -r requirements.txt`.
- Create `.env` containing database name and password.
- Run migrations using the command `python manage.py makemigrations authentication profile flights` followed by `python manage.py makemigrations`.

### Authentication
Run the following to register and signup
```
{
	"user": {
                "username": "beverly1",
                "password": "password1U@#}",
                "email": "beverly1@gmail.com"
            }
}
```
<img width="1119" alt="Screenshot 2019-08-16 at 18 59 49" src="https://user-images.githubusercontent.com/26184534/63181122-2ca24d80-c058-11e9-8744-0eca6eff4852.png">


### Profiles
To get profile, provide the Username as an argument in the url
<img width="921" alt="Screenshot 2019-08-16 at 19 03 27" src="https://user-images.githubusercontent.com/26184534/63181400-93276b80-c058-11e9-8c6c-a6a341e6459b.png">


### Flights
<img width="806" alt="Screenshot 2019-08-16 at 19 05 40" src="https://user-images.githubusercontent.com/26184534/63181529-e00b4200-c058-11e9-8a79-dbe8a6955eaa.png">


### Bookings
<img width="870" alt="Screenshot 2019-08-16 at 19 06 32" src="https://user-images.githubusercontent.com/26184534/63181613-18128500-c059-11e9-8d40-f7b5444a40dc.png">

Ensure to include token in authorization header.
Enjoy!
