def headers(token):
    return { 'Authorization': f'Token {token}', 'content-type': 'application/json'}

user_data = {
	"user": {
                "username": "beverly1",
                "password": "password1U@#}",
                "email": "beverly1@gmail.com"
            }
}

flight_data = {
	"flight": {
		"name": "LA Flight",
		"destination": "LA",
		"departure_date": "2019-08-21",
		"departure_time": "09:30[:00[.000000]]"
	}
}