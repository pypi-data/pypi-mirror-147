import requests


class Client:
    def __init__(self, token) -> None:
        self.token = token

    def request(self, method: str, route: str, **kwargs) -> requests.Response:
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = "Bearer " + self.token
        response = getattr(requests, method)(route, **kwargs)
        if response.status_code == 401:
            raise Exception("Not authorized! Please verify if your token is correct and if you have access to this service.")
        if not response:
            raise Exception(
                f"[Error] Cannot query server for route {route}. {response.content}")
        return response
