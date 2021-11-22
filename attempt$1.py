from logging import warning
import os
import json
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
from eth_keys.datatypes import Signature
from web3 import Web3

load_dotenv()
node_provider = os.environ['NODE_PROVIDER_LOCAL']
web3_connection = Web3(Web3.HTTPProvider(node_provider))

def connect_remix():
    return web3_connection.isConnected()

contract_abi = json.loads(os.environ['CONTRACT_ABI'])
contract_bytecode = os.environ['CONTRACT_BYCODE']

def get_nonce(ETH_address):
    return web3_connection.eth.get_transaction_count(ETH_address)

def contract_deploy(mktBalance, amount_ETH, owner, signature):
    AccountTransfer = web3_connection.eth.contract(abi=contract_abi, btyecode=contract_bytecode)
    transaction_body = {
            'nonce':get_nonce(owner), 
            'value':web3_connection.toWei(amount_ETH, 'ether')
    }
    deployment = AccountTransfer.constructor(mktBalance).buildTransaction(transaction_body)
    signed_transaction = web3_connection.eth.account.sign_transaction(deployment, signature)
    result = web3_connection.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return result