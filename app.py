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
st.markdown("### Smart Movements")

desc_msg = f'This application assists client portfolio management by '
desc_msg += f'calculating transaction fees associated with transferring '
desc_msg += f'between ETH and market accounts '
desc_msg += f'before then initiating the transfer.\n\n'
st.markdown(desc_msg)

# query acct address / print input verification
address_mkt = st.text_input("Market Account Address:")
st.write(address_mkt)

# query acct private key for processing
mkt_acct_key = st.text_input("Enter Private Key:", type="password")

# query amount of ether to transfer 
amount_transfer = Web3.toWei(
        Decimal(st.number_input("How much would you like to transfer?:")),
        'ether'
)

# query transfer source acct
options = st.selectbox(
        "Which account would you like to transfer from?",
        ["Market Account", "Ethereum Account"]
)

# state transaction fees
st.markdown("The fee associated with this transaction is 55,000 GWEI.")

# query clarification of intent
fee_agreement = st.selectbox(
        "Would you like to proceed with transaction?",
        ["Yes", "No"]
)

# ======================================================================
# PREPARE FOR TRANSACTION
# ======================================================================

# Load environment variables
load_dotenv()
PRIVATE_KEY_FIRM = os.getenv("PRIVATE_KEY_FIRM")

# provide firm wallet address to receive transaction fee
address_firm = os.getenv("FIRM_ADDRESS")

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

deployed_contract = w3.eth.contract(abi=abi, bytecode=bytecode)


# fees are agreed to, and button is clicked
if fee_agreement == 'Yes' and st.button('Execute'):

        # gas price ceiling for transaction (in wei)
        gasPrice = 55000 

        # direction of transfer logic
        if options == "Market Account":

                # retrieve nonce for originating acct
                nonce = Web3.toHex(w3.eth.getTransactionCount(address_mkt))

                # set transaction parameters
                tr = {'to': address_firm, 
                        'from': address_mkt,
                        'value': Web3.toHex(amount_transfer), 
                        'gasPrice': Web3.toHex(gasPrice), 
                        'nonce': nonce,
                        'data': "0x" + bytecode,
                        'gas': 5000000,
                        }
                
                # validate transaction with private key
                signed = w3.eth.account.sign_transaction(tr, mkt_acct_key)
        else:

                # retrieve nonce for originating acct
                nonce = Web3.toHex(w3.eth.getTransactionCount(address_firm))

                # set transaction parameters
                tr = {'to': address_mkt, 
                        'from': address_firm,
                        'value': Web3.toHex(amount_transfer), 
                        'gasPrice': Web3.toHex(gasPrice), 
                        'nonce': nonce,
                        'data': "0x" + bytecode,
                        'gas': 5000000,
                        }

                # validate transaction with private key
                signed = w3.eth.account.sign_transaction(tr, PRIVATE_KEY_FIRM)
        
        # initiate transfer
        tx = w3.eth.sendRawTransaction(signed.rawTransaction)    
        tx_receipt = w3.eth.waitForTransactionReceipt(tx)

        # update contract with new balance 
        deployed_contract = w3.eth.contract(
                address=tx_receipt.contractAddress,
                abi=abi
        )

        # declare completion
        st.write('Transaction Complete.')
