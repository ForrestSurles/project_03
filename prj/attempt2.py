from web3 import Web3
from web3.types import SignedTx

# Will be using Ganache for the premise of this project
ganache_url = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check and see if you are connect by using the below code
# print(web3.isConnected())

# If this works, you can keep moving on

account_1 = "0x7AEa3A1401db009c1a9A00D990dD65BAbF49812B"
account_2 = "0x278e94EdF705e7632E79918442E37EA6164989CF"

# The below private key belongs to account_1
private_key_one = "76a75b9a4b0b594f92b72c4ae2600b363514c4b23415c0d6b254428c4cc7e3cc"

# Steps
    # Start with getting the nonce
    # Build transaction
    # Sign transaction
    # Send transaction
    # Get transaction hash

# Getting nonce
nonce = web3.eth.getTransactionCount(account_1)

# Build the transaction
tx = {
    # Prevents send twice
    'nonce': nonce,
    # Account we need to send transaction to
    'to': account_2,
    # Value of ether we are going to send
    # We have used the smalled amount below
    'value': web3.toWei(1, 'ether'),
    # Gas limit - Miners compensation
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei')
}

# Sign transaction
signed_tx = web3.eth.account.signTransaction(tx, private_key_one)

# Send transaction
# Result will be a hash
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# print(tx_hash)
# Above might not look as pretty, so we have provide an easy print down below
print(web3.toHex(tx_hash))