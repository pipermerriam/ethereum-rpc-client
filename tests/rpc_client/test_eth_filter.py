from ethereum import tester
from eth_rpc_client import Client
import re

CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = "8545"

def is_valid_filter_id(filt_id):
    """
    """
    check = re.compile("0x[\da-fA-F]+")
    m = check.match(filt_id)
    if m:
        return(True)
    else:
        return(False)


def test_new_filter(rpc_server, eth_coinbase):
    """
    """
    client = Client(CLIENT_HOST, CLIENT_PORT)

    filt_id = client.new_filter(from_block="latest", to_block="pending")
    
    assert is_valid_filter_id(filt_id)

def test_uninstall_filter(rpc_server, eth_coinbase): 
    """
    """
    client = Client(CLIENT_HOST, CLIENT_PORT)

    filt_id = client.new_filter() 
    
    assert is_valid_filter_id(filt_id)
    
    resp = client.uninstall_filter(filt_id) 
    
    assert resp == True


def test_get_filter_changes(rpc_server, eth_coinbase):
    """
    """

    client = Client(CLIENT_HOST, CLIENT_PORT)

    filt_id = client.new_filter()     
    assert is_valid_filter_id(filt_id)
    
    resp = client.get_filter_logs(filt_id)
    assert resp == []

