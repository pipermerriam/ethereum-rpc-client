from ethereum import tester


def test_get_accounts(rpc_server, rpc_client):
    accounts = rpc_client.get_accounts()

    assert len(accounts) == len(tester.accounts)

    for _a, a in zip(accounts, tester.accounts):
        assert _a == "0x" + tester.encode_hex(a)
