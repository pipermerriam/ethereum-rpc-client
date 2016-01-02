import requests

from eth_client_utils import (
    JSONRPCBaseClient,
)


class Client(JSONRPCBaseClient):
    def __init__(self, host="127.0.0.1", port="8545", *args, **kwargs):
        self.host = host
        self.port = port
        self.session = requests.session()

        super(Client, self).__init__(*args, **kwargs)

    def make_request(self, method, params):
        request_data = self.construct_json_request(method, params)
        response = self.session.post(
            "http://{host}:{port}/".format(host=self.host, port=self.port),
            data=request_data,
        )
        data = response.json()
        if data and 'error' in data:
            raise ValueError(data)
        return data
