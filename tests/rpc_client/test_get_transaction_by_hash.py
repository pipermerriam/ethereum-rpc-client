from ethereum import tester

from eth_rpc_client import Client


def test_get_transaction_by_hash(rpc_server, eth_coinbase):
    client = Client('127.0.0.1', '8545')

    to_addr = tester.encode_hex(tester.accounts[1])

    txn_hash = client.send_transaction(
        _from=eth_coinbase,
        to=to_addr,
        value=12345,
    )

    txn = client.get_transaction_by_hash(txn_hash)

    assert txn['from'].endswith(eth_coinbase)
    assert txn['to'].endswith(to_addr)
    assert int(txn['value'], 16) == 12345
