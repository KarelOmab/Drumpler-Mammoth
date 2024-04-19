import json

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
            self.request_dict = json.loads(request_raw)
        elif isinstance(request_raw, dict):
            self.request_dict = request_raw
        else:
            raise ValueError("request_raw must be either a JSON string or a dictionary")

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