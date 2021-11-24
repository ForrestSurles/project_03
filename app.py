from web3 import Web3, middleware
from web3.exceptions import ContractLogicError
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import *
import os
import json
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

# build streamlit interface
side_click = st.sidebar.write("Contributors: John P Weldon, Ashley Guidot, Forrest Surles, Vishwanath Subramanian")

st.image('https://image.cnbcfm.com/api/v1/image/106962967-1634709558798-gettyimages-1235570383-porzycki-cryptocu210928_npbUe.jpeg?v=1635185551', width=350)

st.markdown("### Smart Risk Movements")
st.markdown("This application assists client portfolio management by calculating transaction fees associated with transferring between Ethereum and a fund before enabling the client to initiate the transfer. The application then automates the transfer of the amount between Etherum and a fund.")

# Load .env environment variables
PRJ3_folder = os.path.expanduser('~/Dropbox/FinTech-Workspace/project_03')  # adjust yours as appropriate
load_dotenv((os.path.join(PRJ3_folder, 'prjenv.env')))
PRIVATE_KEY_ONE = os.getenv("PRIVATE_KEY_1")

# Copy bytecode from Remix to utilize smart contract locally
bytecode = json.load(open('bytecode.json'))['object']
# Copy abi from Remix
abi = json.load(open('abi.json'))

# connect to blockchain network
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# query input from user to initiate transaction

# wallet address
mkt_account_input = st.text_input("Enter your Market Account Address:")
st.write(mkt_account_input)

# private key
priv_key_input = st.text_input("Enter your Private Key:", type="password")

# options for transaction
options = st.selectbox("Which account would you like to transfer from?",
        ["Market Account", "Eth Account"])

# give notice of transaction fees
st.markdown("The fee associated with this transaction is 21,000 GWEI.")

# clarify intent from user
fee_agreement = st.selectbox("Would you like to proceed with transaction?",
        ["Yes", "No"])