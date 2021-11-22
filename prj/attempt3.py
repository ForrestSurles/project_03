from web3 import Web3, middleware
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import *
import os
import json

# TODO: get address one and our private key
address_one = '0x87aC8fB7F9847A6D76Eb217B40A2A91bADd3bbD6'
PRIVATE_KEY = 'e052b603f3795407be51f1e6c50dae0c826100b4a80f7de9ea62dc26105cba86'

# Copy bytecode from Remix
bytecode = json.load(open('bytecode.json'))['object']
# Copy abi from Remix
abi = json.load(open('abi.json'))

# Used the Infura website to get the below http link
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/76266a8a5a774c568a78834f49903cb1'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
w3.middleware_onion.add(middleware.simple_cache_middleware)

# web3 function that allows us to set the amount of time we want transactions to take (in secs)
strategy = construct_time_based_gas_price_strategy(15)
# Sets the gas price
w3.eth.setGasPriceStrategy(strategy)

# TODO: I need to change the name to our contract name
our_contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Getting nonce
# Using toHex for easier visability when deployed
nonce = Web3.toHex(w3.eth.getTransactionCount(address_one))
gasPrice = w3.eth.generateGasPrice()
print("gasprice: ", gasPrice)

tr = {'to': None, 
        'from': address_one,
        'value': Web3.toHex(0), 
        'gasPrice': Web3.toHex(gasPrice), 
        'nonce': nonce,
        'data': "0x" + bytecode,
        'gas': 5000000,
        }

signed = w3.eth.account.sign_transaction(tr, PRIVATE_KEY)
tx = w3.eth.sendRawTransaction(signed.rawTransaction)    
tx_receipt = w3.eth.waitForTransactionReceipt(tx)

# TODO: I need to change the name to our contract name
our_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Print a separation line
print("********")

# Print "Completed." to show this transaction has been completed
print("Completed.")