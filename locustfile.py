from locust import HttpUser, task, between, events
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
            assertion = api.get("assert", {})

            try:
                if method == "GET":
                    with self.client.get(endpoint, headers=headers, catch_response=True, verify=False) as response:
                        self._check_assertions(response, assertion)
                elif method == "POST":
                    with self.client.post(endpoint, json=body, headers=headers, catch_response=True, verify=False) as response:
                        self._check_assertions(response, assertion)
                elif method == "PUT":
                    with self.client.put(endpoint, json=body, headers=headers, catch_response=True, verify=False) as response:
                        self._check_assertions(response, assertion)
                elif method == "DELETE":
                    with self.client.delete(endpoint, headers=headers, catch_response=True, verify=False) as response:
                        self._check_assertions(response, assertion)
                else:
                    print(f"Unsupported method: {method}")

            except Exception as e:
                print(f"Error calling {endpoint}: {e}")
                events.request.fire(
                    request_type=method,
                    name=endpoint,
                    exception=e
                )

    def _check_assertions(self, response, assertion):
        response_json = {}
        try:
            response_json = response.json()
        except Exception:
            response.failure(f"Expected JSON response but got: {response.text}")
            return
            
        expected_status = assertion.get("status_code", {})
        if expected_status and response.status_code != expected_status:
            response.failure(f"Expected status {expected_status}, got {response.status_code}")

        expected_body = assertion.get("body_contains", {})
        if expected_body:
            for key, value in expected_body.items():
                if key not in response_json or response_json[key] != value:
                    response.failure(f"Expected body to contain {key}: {value}, got {response_json}")
                    return
