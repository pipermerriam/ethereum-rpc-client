import pytest

from ethereum import tester


def test_get_block_by_hash(rpc_server, rpc_client, eth_coinbase):
    block_number = rpc_client.get_block_number()
    assert block_number == 0

    to_addr = "0x" + tester.encode_hex(tester.accounts[1])
    txn_hash = rpc_client.send_transaction(_from=eth_coinbase, to=to_addr, value=100)
    assert txn_hash

    block_number = rpc_client.get_block_number()

    block = rpc_client.get_block_by_number(block_number)
    assert block
