# app/utils.py
import requests

class MockResponse:
    def __init__(self, json_data, status_code, text=""):
        self._json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._json_data

def response_from_url(url, data):
    response = requests.post(url, json=data)
    return MockResponse(response.json(), response.status_code, response.text)