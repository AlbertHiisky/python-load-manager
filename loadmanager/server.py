import requests


class Server:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.healthy = False
        self.timeout = 1
        self.scheme = "http://"
        self.open_connections = 0

    def alive(self):
        return self.healthy

    def healthcheck(self):
        try:
            req = self.scheme + self.endpoint + '/healthcheck'
            response = requests.get(req, timeout=self.timeout)
            if response.ok:
                self.healthy = True
            else:
                self.healthy = False
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.healthy = False

    def __repr__(self):
        return "<Server: {} {} {}>".format(self.endpoint, self.healthy, self.timeout)