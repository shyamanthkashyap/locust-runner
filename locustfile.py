from locust import HttpUser, task, between
import json

with open("config.json") as f:
    config = json.load(f)

class APILoadTest(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_endpoints(self):
        for api in config["apis"]:
            method = api.get("method", "GET").upper()
            endpoint = api["url"]
            body = api.get("body", {})
            headers = api.get("headers", {})

            try:
                if method == "GET":
                    self.client.get(endpoint, headers=headers, verify=False)
                elif method == "POST":
                    self.client.post(endpoint, json=body, headers=headers, verify=False)
                elif method == "PUT":
                    self.client.put(endpoint, json=body, headers=headers, verify=False)
                elif method == "DELETE":
                    self.client.delete(endpoint, headers=headers, verify=False)
            except Exception as e:
                print(f"Error calling {endpoint}: {e}")
