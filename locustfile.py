from locust import HttpUser, task, between
import json

# Load config
with open("config.json") as f:
    config = json.load(f)

class APILoadTest(HttpUser):
    wait_time = between(1, 2)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def test_endpoints(self):
        for api in config["apis"]:
            method = api.get("method", "GET").upper()
            endpoint = api["url"]
            body = api.get("body", {})

            if method == "GET":
                self.client.get(endpoint, verify=False)
            elif method == "POST":
                self.client.post(endpoint, json=body, verify=False)
            elif method == "PUT":
                self.client.put(endpoint, json=body, verify=False)
            elif method == "DELETE":
                self.client.delete(endpoint, verify=False)
