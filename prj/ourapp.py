import pandas as pd
import streamlit as st

st.markdown("### Smart Risk Movements")
st.markdown("This application assists client portfolio management by calculating transaction fees associated with transferring between Ethereum and a fund before enabling the client to initiate the transfer. The application then automates the transfer of the amount between Etherum and a fund.")

options = st.selectbox("Which account would you like to transfer from?",
                        ["Account 1", "Account 2"])

fee_agreement = st.selectbox("Are you aware of the fee associated with every transaction?",
                        ["I am aware of the transfer fee.", "I am not aware of the transfer fee."])






st.markdown("Contributors: John P Weldon, Ashley Guidot, Forrest Surles, Vishwanath Subramanian")