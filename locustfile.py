import random
from typing import Any, Dict

from locust import HttpUser, between, events, task


class TodoUser(HttpUser):
    wait_time = between(1, 2)
    token = None
    headers: Dict[str, str] = {}

    def on_start(self):
        try:
            email = f"test{random.randint(1, 30000)}@test.com"
            password = "testingtestpassword"

            register_response = self.client.post(
                "/auth/register",
                json={
                    "email": email,
                    "password": password,
                },
            )

            if register_response.status_code not in [200, 201]:
                print(f"Registration failed: {register_response.text}")
                return

            login_response = self.client.post(
                "/auth/jwt/login",
                data={
                    "username": email,
                    "password": password,
                },
            )

            if login_response.status_code == 200:
                self.token = login_response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                print(f"Login failed: {login_response.text}")
        except Exception as e:
            print(f"Error during authentication: {str(e)}")

    @task(3)
    def get_todos(self):
        with self.client.get(
            "/todos", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get todos: {response.text}")

    @task(2)
    def create_todo(self):
        todo_data = {
            "title": f"Test Todo {random.randint(1, 1000)}",
            "description": f"Test Description {random.randint(1, 1000)}",
            "priority": random.randint(1, 5),
        }

        with self.client.post(
            "/todos", headers=self.headers, json=todo_data, catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Failed to create todo: {response.text}")

    @task(1)
    def search_todos(self):
        search_queries = ["Test", "Important", "Urgent", "Project"]
        with self.client.get(
            "/todos/search/",
            headers=self.headers,
            params={"query": random.choice(search_queries)},
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to search todos: {response.text}")

    @task(1)
    def get_top_priority_todos(self):
        with self.client.get(
            "/todos/top-priority/",
            headers=self.headers,
            params={"top_n": random.randint(1, 5)},
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get top priority todos: {response.text}")

    @task(1)
    def sort_todos(self):
        sort_fields = ["title", "priority", "created_at"]
        sort_orders = ["asc", "desc"]

        with self.client.get(
            "/todos/criteria-sort/",
            headers=self.headers,
            params={
                "sort_by": random.choice(sort_fields),
                "order": random.choice(sort_orders),
            },
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to sort todos: {response.text}")


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    print("Locust is initializing")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Load test is starting")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Load test is stopping")
