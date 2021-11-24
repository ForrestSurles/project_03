import os
import json
import pandas as pd
import streamlit as st

from decimal import Decimal
from dotenv import load_dotenv
from web3 import Web3, middleware
from web3.gas_strategies.time_based import *
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware

# ======================================================================
# STREAMLIT INTERFACE
# ======================================================================

# contributors
sidebar_msg = f"Contributors:\n\n"
sidebar_msg += f"- John P Weldon\n"
sidebar_msg += f"- Ashley Guidot\n"
sidebar_msg += f"- Forrest Surles\n"
sidebar_msg += f"- Vishwanath Subramanian"

st.sidebar.write(sidebar_msg)
st.image('./cover_image.jpeg', width=700)
st.markdown("### Smart Risk Movements")
st.markdown("This application assists client portfolio management by calculating transaction fees associated with transferring between Ethereum and a fund before enabling the client to initiate the transfer. The application then automates the transfer of the amount between Etherum and a fund.")

# query acct address / print input verification
address_one = st.text_input("Market Account Address:")
st.write(address_one)

# query acct private key for processing
priv_key = st.text_input("Enter your Private Key:", type="password")

# amount of ether to transfer 
amount_transfer = Web3.toWei(
        Decimal(st.number_input("How much would you like to transfer?:")),
        'ether'
)

# select acct
options = st.selectbox(
        "Which account would you like to transfer from?",
        ["Market Account", "Ethereum Account"]
)

# declare transaction fees
st.markdown("The fee associated with this transaction is 55,000 GWEI.")

# clarify intent from user
fee_agreement = st.selectbox(
        "Would you like to proceed with transaction?",
        ["Yes", "No"]
)

# ======================================================================
# PREPARE FOR TRANSACTION
# ======================================================================

# Load environment variables
load_dotenv()
PRIVATE_KEY_ONE = os.getenv("PRIVATE_KEY_1")

# smart contract bytecode/abi for local execution
bytecode = json.load(open('bytecode.json'))['object']
abi = json.load(open('abi.json'))

# connect to blockchain network
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# set desired transaction time amount (in seconds)
strategy = construct_time_based_gas_price_strategy(15)
# set gas price
w3.eth.setGasPriceStrategy(strategy)

our_contract = w3.eth.contract(abi=abi, bytecode=bytecode)


# provide firm wallet address to receive transaction fee
address_two = '0xb1fB7f3c3D78DcB6B68D07ade463ca3Cd63fB373'

# address two private key
PRIVATE_KEY_TWO = os.getenv("PRIVATE_KEY_2")

# if user agrees to fees and executes proceed to further if else statement
if fee_agreement == 'Yes' and st.button('Execute'):

        # Getting nonce
        # Using toHex for easier visability when deployed
        gasPrice = 55000 #gwei

        if options == "Market Account":

                nonce = Web3.toHex(w3.eth.getTransactionCount(address_one))

                tr = {'to': address_two, 
                        'from': address_one,
                        'value': Web3.toHex(amount_transfer), 
                        'gasPrice': Web3.toHex(gasPrice), 
                        'nonce': nonce,
                        'data': "0x" + bytecode,
                        'gas': 5000000,
                        }
                signed = w3.eth.account.sign_transaction(tr, priv_key)
        else:

                nonce = Web3.toHex(w3.eth.getTransactionCount(address_two))

                tr = {'to': address_one, 
                        'from': address_two,
                        'value': Web3.toHex(amount_transfer), 
                        'gasPrice': Web3.toHex(gasPrice), 
                        'nonce': nonce,
                        'data': "0x" + bytecode,
                        'gas': 5000000,
                        }
                signed = w3.eth.account.sign_transaction(tr, PRIVATE_KEY_TWO)
        
        tx = w3.eth.sendRawTransaction(signed.rawTransaction)    
        tx_receipt = w3.eth.waitForTransactionReceipt(tx)

        # Complete transaction
        our_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        st.write('Transaction Complete.')
