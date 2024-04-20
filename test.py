import os
import random

import locust
from locust import HttpUser, task, between


class Tests(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_get_columns(self):
        response = self.client.get("/")
        if response.status_code == 200:
            data = response.json()
            print("Received Data ", data)
        else:
            print("Error in fetching columns ", response.status_code)

    @task
    def test_fetch_data(self):
        # columns = ["Type", "Delivery Status", "Typ", "Department Name", "Order Country"]
        columns = ["Type", "Delivery Status", "Department Name", "Order Country"]
        selected_col = random.choice(columns)
        data = {"column": selected_col, "page": 1, "limit": 20}
        response = self.client.post('http://127.0.0.1:5000/fetch_data', json=data)
        if response.status_code == 200:
            print("Fetched Data for column ", data['column'])
        else:
            print("Error in fetching data")

    @task
    def test_fetch_rows(self):
        column = "Type"
        # opts = ["DEBIT", "CASH", "PAYMENT", "CREDIT", "Cr"]
        opts = ["DEBIT", "CASH", "PAYMENT", "CREDIT"]
        selected_option = random.choice(opts)
        data = {"column": column, "data": selected_option, "page": 1, "limit": 20}
        response = self.client.post('http://127.0.0.1:5000/fetch_rows', json=data)
        if response.status_code == 200:
            print("Fetched Rows for Column and Option ", data['column'], " ", data['data'])
        else:
            print("Error in fetching data")


if __name__ == "__main__":
    host = 'http://127.0.0.1:5000/'
    web_ui = True
    users = int(os.environ.get("LOCUST_USERS", 10))
    run_time = int(os.environ.get("LOCUST_RUN_TIME", 60))
    options = {"host": host, "users": users, "web_ui": web_ui, "run_time": run_time}
    locust.main(**options)