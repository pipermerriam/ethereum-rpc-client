import json
import numbers
import requests

from eth_rpc_client.utils import (
    wait_for_transaction,
    wait_for_block,
    get_max_gas,
)


def get_transaction_params(_from=None, to=None, gas=None, gas_price=None,
                           value=0, data=None):
    params = {}

    if _from is None:
        raise ValueError("No default from address specified")

    params['from'] = _from

    if to is None and data is None:
        raise ValueError("A `to` address is only optional for contract creation")
    elif to is not None:
        params['to'] = to

    if gas is not None:
        params['gas'] = hex(gas)

    if gas_price is not None:
        params['gasPrice'] = hex(gas_price)

    if value is not None:
        params['value'] = hex(value).rstrip('L')

    if data is not None:
        params['data'] = data

    return params


def construct_filter_args(from_block=None, to_block=None, address=None,
                          topics=None):
    params = {}
    if from_block is not None:
        params["fromBlock"] = from_block
    if to_block is not None:
        params["toBlock"] = to_block
    if address is not None:
        params["address"] = address
    if topics is not None:
        params["topics"] = topics
    return(params)


class Client(object):
    _nonce = 0

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.session()

    def get_nonce(self):
        self._nonce += 1
        return self._nonce

    @property
    def default_from_address(self):
        return self.get_coinbase()

    def make_rpc_request(self, method, params):
        response = self.session.post(
            "http://{host}:{port}/".format(host=self.host, port=self.port),
            data=json.dumps({
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": self.get_nonce(),
            })
        )
        data = response.json()
        if data and 'error' in data:
            raise ValueError(data)
        return data

    def get_coinbase(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_coinbase
        """
        response = self.make_rpc_request("eth_coinbase", [])
        return response['result']

    def get_gas_price(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gasprice
        """
        response = self.make_rpc_request("eth_gasPrice", [])
        return int(response['result'], 16)

    def get_balance(self, address, block="latest"):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getbalance
        """
        response = self.make_rpc_request("eth_getBalance", [address, block])
        return int(response['result'], 16)

    def get_code(self, address, block="latest"):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getcode
        """
        response = self.make_rpc_request("eth_getCode", [address, block])
        return response['result']

    def call(self, _from=None, to=None, gas=None, gas_price=None, value=0,
             data=None, block="latest"):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_call
        """
        if _from is None:
            _from = self.default_from_address

        params = [
            get_transaction_params(_from, to, gas, gas_price, value, data),
            block,
        ]
        response = self.make_rpc_request("eth_call", params)
        return response['result']

    def send_transaction(self, _from=None, to=None, gas=None, gas_price=None,
                         value=0, data=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sendtransaction
        """
        if _from is None:
            _from = self.default_from_address

        params = get_transaction_params(_from, to, gas, gas_price, value, data)

        response = self.make_rpc_request("eth_sendTransaction", [params])
        return response['result']

    def get_transaction_receipt(self, txn_hash):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionreceipt
        """
        response = self.make_rpc_request("eth_getTransactionReceipt", [txn_hash])
        return response['result']

    def get_transaction_by_hash(self, txn_hash):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionbyhash
        """
        response = self.make_rpc_request("eth_getTransactionByHash", [txn_hash])
        return response['result']

    def get_block_number(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_blocknumber<F37>
        """
        response = self.make_rpc_request("eth_blockNumber", [])
        return int(response['result'], 16)

    def get_block_by_hash(self, block_hash, full_transactions=True):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblockbyhash
        """
        response = self.make_rpc_request("eth_getBlockByHash", [block_hash, full_transactions])
        return response['result']

    def get_block_by_number(self, block_number, full_transactions=True):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblockbynumber
        """
        if isinstance(block_number, numbers.Number):
            block_number_as_hex = hex(block_number)
        else:
            block_number_as_hex = block_number
        response = self.make_rpc_request(
            "eth_getBlockByNumber", [block_number_as_hex, full_transactions],
        )
        return response['result']

    def get_accounts(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_accounts
        """
        response = self.make_rpc_request("eth_accounts", [])
        return response['result']

    get_max_gas = get_max_gas
    wait_for_transaction = wait_for_transaction
    wait_for_block = wait_for_block

    def new_filter(self, from_block=None, to_block=None, address=None, topics=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_newfilter
        Create a new filter object to be notified of changes in the
        state of the EVM through the logs.
        This command returns a filter ID that can be referenced by
        other commands to get log information.
        """
        params = construct_filter_args(from_block, to_block, address, topics)
        response = self.make_rpc_request("eth_newFilter", [params])
        return(response['result'])

    def new_block_filter(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_newblockfilter
        """
        response = self.make_rpc_request("eth_newBlockFilter", [])
        return(response['result'])

    def new_pending_transaction_filter(self):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_newpendingtransactionfilter
        """
        response = self.make_rpc_request("eth_newPendingTransactionFilter", [])
        return(response['result'])

    def uninstall_filter(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_uninstallfilter
        Removes a filter by ID
        """
        if isinstance(filter_id, numbers.Number):
            filt_hex = hex(filter_id)
        else:
            filt_hex = filter_id

        response = self.make_rpc_request("eth_uninstallFilter", [filt_hex])
        return(response['result'])

    def get_filter_changes(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getfilterchanges
        """
        if isinstance(filter_id, numbers.Number):
            filt_hex = hex(filter_id)
        else:
            filt_hex = filter_id
        response = self.make_rpc_request("eth_getFilterChanges", [filt_hex])
        return(response['result'])

    def get_filter_logs(self, filter_id):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getfilterlogs
        """
        if isinstance(filter_id, numbers.Number):
            filt_hex = hex(filter_id)
        else:
            filt_hex = filter_id
        response = self.make_rpc_request("eth_getFilterLogs", [filt_hex])
        return(response['result'])

    def get_logs(self, from_block=None, to_block=None, address=None, topics=None):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getlogs
        """
        params = construct_filter_args(from_block, to_block, address, topics)
        response = self.make_rpc_request("eth_getLogs", [params])
        return(response['result'])
