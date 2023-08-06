import aiohttp
from json import loads,dumps
from base64 import b64encode
from http.client import HTTPSConnection

class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes, 'Content-Encoding' : 'gzip'}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)

class AsyncRestClient:

    domain = "https://api.dataforseo.com"

    def __init__(self, username, password, session: aiohttp.ClientSession):
        self.username = username
        self.password = password
        self.session = session
        base64_bytes = b64encode(
            ("%s:%s" % (self.username, self.password)).encode("ascii")
        ).decode("ascii")
        self.headers = {'Authorization': 'Basic %s' % base64_bytes,
                        'Content-Encoding': 'gzip'}

    async def get(self, path):
        path = self.domain+path
        async with self.session.get(path, headers=self.headers) as resp:
            return await resp.json(content_type=None)

    async def post(self, path, data):
        path = self.domain+path
        async with self.session.post(path, json=data, headers=self.headers) as resp:
            return await resp.json(content_type=None)
