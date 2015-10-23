from eth_rpc_client import Client


def test_get_code(rpc_server):
    client = Client('127.0.0.1', '8545')

    max_gas = client.get_max_gas()
    assert max_gas > 0
