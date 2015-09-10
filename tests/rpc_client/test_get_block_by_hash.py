import pytest

from ethereum import tester


@pytest.mark.xfail
def test_get_block_by_hash(rpc_server, rpc_client, eth_coinbase):
    block_number = rpc_client.get_block_number()
    assert block_number == 0

    to_addr = "0x" + tester.encode_hex(tester.accounts[1])
    txn_hash = rpc_client.send_transaction(_from=eth_coinbase, to=to_addr, value=100)
    assert txn_hash

    txn_receipt = rpc_client.get_transaction_receipt(txn_hash)
    block_hash = txn_receipt['blockHash']

    block = rpc_client.get_block_by_hash(block_hash)
    assert block
