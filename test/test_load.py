"""
This is a load test module for testing the REST API.

Usage -
    1. locust --host=http://localhost:8089 -f test_performance.py
    2. Use the web browser - http://localhost:8089
    3. Start the test by specifying number of users to simulate and users/sec
"""
# Third Party Library
from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    """ This class will test user behavior. """

    @task
    def get_load_test(self):
        """ Load Test GET API. """
        self.client.get("http://localhost:9090/query?number=12409283353")

    @task
    def post_load_test(self):
        """ Load Test POST API. """
        data = {"number": "(412)1231234", "context": "Testing", "name": "Sudhakar"}
        self.client.post("http://localhost:9090/query?number=", {"Content-Type" : "application/json", "charset" : "utf-8"}, data)

class WebsiteUser(HttpLocust):
    """ Website User is the master class for testing load. """
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 15000
