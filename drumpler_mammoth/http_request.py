import requests
import json
from .config import Config

class HttpRequest:
    def __init__(self, id, job_id, source_ip, user_agent, method, request_url, request_raw, custom_value):
        self.id = id
        self.job_id = job_id
        self.source_ip = source_ip
        self.user_agent = user_agent
        self.method = method
        self.request_url = request_url
        self.custom_value = custom_value

        # Ensure request_raw is correctly handled
        if isinstance(request_raw, str):
            self.request_json = json.loads(request_raw)
        elif isinstance(request_raw, dict):
            self.request_json = request_raw
        else:
            raise ValueError("request_raw must be either a JSON string or a dictionary")

    def mark_as_handled(self):
        headers = {
            'Authorization': f'Bearer {Config.AUTHORIZATION_KEY}',
            'Content-Type': 'application/json'  # Indicate JSON payload
        }
        payload = {
            'is_handled': 1  # Assuming setting `is_handled` to 1 marks it as handled
        }

        try:
            response = requests.put(f"{Config.DRUMPLER_URL}/request/{self.id}", json=payload, headers=headers)
            if response.status_code == 200:
                return f"Request {self.id} marked as handled successfully."
            else:
                # Attempt to extract and print a more descriptive error message
                try:
                    error_message = response.json().get('message', 'No error message provided.')
                except ValueError:  # If response is not in JSON format
                    error_message = response.text
                return f"Failed to mark request {self.id} as handled: {response.status_code}, Error: {error_message}"
        except requests.exceptions.RequestException as e:
            return f"Error marking request {self.id} as handled: {e}"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def job_id(self):
        return self._job_id

    @id.setter
    def job_id(self, value):
        self._job_id = value

    @property
    def source_ip(self):
        return self._source_ip

    @source_ip.setter
    def source_ip(self, value):
        self._source_ip = value

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def request_url(self):
        return self._request_url

    @request_url.setter
    def request_url(self, value):
        self._request_url = value

    @property
    def request_raw(self):
        return self._request_raw

    @request_raw.setter
    def request_raw(self, value):
        self._request_raw = value

    @property
    def request_json(self):
        return self._request_json

    @request_json.setter
    def request_json(self, value):
        self._request_json = value