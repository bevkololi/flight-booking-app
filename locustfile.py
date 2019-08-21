from locust import HttpLocust, TaskSet, task
import json
from locustMock import user_data, headers, flight_data

class UserBehavior(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def createUser(self):
        user = self.client.post('api/users/', data=json.dumps(user_data),\
            headers={'content-type': 'application/json'})
        return user.json

    def login(self):
        user = self.client.post('api/users/login/', data=json.dumps(user_data),\
            headers={'content-type': 'application/json'})
        return user.json()


    @task(1)
    def updateUserProfile(self):
        user = self.login()
        user_data['user']['passport'] = "https://res.cloudinary.com/dutpgpo9o/image/upload/v1566388286/mczuzw475cbbcnfcp5j0.jpg"
        username = user_data['user']['username']
        self.client.put(f'api/profiles/{username}/', data=json.dumps(user_data),\
            headers=headers(user['user']['token']))
    
    @task(2)
    def getFlights(self):
        user = self.login()
        self.client.get(f'api/flights/', headers=headers(user['user']["token"]))


    @task(3)
    def getBookings(self):
        user = self.login()
        self.client.get(f'api/flights/1/bookings/', headers=headers(user['user']["token"]))
      
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000