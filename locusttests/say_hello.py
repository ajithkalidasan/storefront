from locust import HttpUser, task, between

class SayHello(HttpUser):
    @task
    def say_hello(self):
        response = self.client.get("/playground/home/")