from web3 import Web3, middleware
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import *
import os
import json
from dotenv import load_dotenv


# TODO: get address one and our private key
address_one = '0x7AEa3A1401db009c1a9A00D990dD65BAbF49812B'
address_two = '0x278e94EdF705e7632E79918442E37EA6164989CF'

# Load .env environment variables
PRJ3_folder = os.path.expanduser('~/Desktop/prj')  # adjust yours as appropriate
load_dotenv((os.path.join(PRJ3_folder, 'prjenv.env')))
PRIVATE_KEY_ONE = os.getenv("PRIVATE_KEY_1")

# Copy bytecode from Remix
bytecode = json.load(open('bytecode.json'))['object']
# Copy abi from Remix
abi = json.load(open('abi.json'))

# Will be using Ganache for the premise of this project
ganache_url = "http://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(ganache_url))

# Check and see if you are connect by using the below code
# print(web3.isConnected())

# If this works, you can keep moving on
# Used the Infura website to get the below http link
#w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/76266a8a5a774c568a78834f49903cb1'))
#w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
#w3.middleware_onion.add(middleware.simple_cache_middleware)

# web3 function that allows us to set the amount of time we want transactions to take (in secs)
strategy = construct_time_based_gas_price_strategy(15)
# Sets the gas price
w3.eth.setGasPriceStrategy(strategy)

# TODO: I need to change the name to our contract name
our_contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Getting nonce
# Using toHex for easier visability when deployed
nonce = Web3.toHex(w3.eth.getTransactionCount(address_one))
gasPrice = 21000 #gwei
print("gasprice: ", gasPrice)

tr = {'to': address_two, 
        'from': address_one,
        'value': Web3.toHex(0), 
        'gasPrice': Web3.toHex(gasPrice), 
        'nonce': nonce,
        'data': "0x" + bytecode,
        'gas': 5000000,
        }

signed = w3.eth.account.sign_transaction(tr, PRIVATE_KEY_ONE)
tx = w3.eth.sendRawTransaction(signed.rawTransaction)    
tx_receipt = w3.eth.waitForTransactionReceipt(tx)

# TODO: I need to change the name to our contract name
our_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Print a separation line
print("********")

# Print "Completed." to show this transaction has been completed
print("Completed.")