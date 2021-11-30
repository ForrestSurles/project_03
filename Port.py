#Import the Python libraries
from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import streamlit as st
import yfinance as yf

#Display the resukts of the Smart Risk Movement Accounts
st.image('https://image.cnbcfm.com/api/v1/image/106962967-1634709558798-gettyimages-1235570383-porzycki-cryptocu210928_npbUe.jpeg?v=1635185551', width=350)


st.markdown("### Smart Risk Movements")
st.markdown("This application assists client portfolio management by calculating transaction fees associated with transferring between Ethereum and a fund before enabling the client to initiate the transfer. The application then automates the transfer of the amount between Etherum and a fund.")

options = st.selectbox("Which account would you like to transfer from?",
        ["Account 1", "Account 2"])

fee_agreement = st.selectbox("Are you aware of the fee associated with every transaction?",
        ["I am aware of the transfer fee.", "I am not aware of the transfer fee."])


st.markdown("### Ethereum Stock Performance Dataframe")

# Download the Stock data & Generate the dataframe for Ethereum
(ETH_df) = yf.download('ETH-USD', 
                      start='2020-01-01', 
                      end='2021-11-24', 
                      progress=False)

st.dataframe(ETH_df)

st.markdown("### Ethereum Stock Performance Plot")
#Plot the Closing values & Moving Average for Ethereum
mov_avg_ETH= st.text_input("Ethereum days Moving Average:", "50")
'Moving Average Days_ETH: ', mov_avg_ETH
ETH_df["mov_avg_close"] = ETH_df['Close'].rolling(window=int(mov_avg_ETH),min_periods=0).mean()
st.line_chart(ETH_df[["mov_avg_close","Close"]])

st.markdown("### Vanguard Index Fund Dataframe")
# Download the Stock data & Generate the dataframe for the Vanguard Index Fund (VOO)

(VOO_df) = yf.download('VOO', 
                      start='2020-01-01', 
                      end='2021-11-24', 
                      progress=False)

st.dataframe(VOO_df)

st.markdown("### Vanguard Index Fund Performance Plot")
#Plot the Closing values & Moving Average for VOO

mov_avg_VOO= st.text_input("Vanguard 500 Index Fund days Moving Average:", "50")
'Moving Average Days_VOO: ', mov_avg_VOO
VOO_df["mov_avg_close"] = VOO_df['Close'].rolling(window=int(mov_avg_VOO),min_periods=0).mean()
st.line_chart(VOO_df[["mov_avg_close","Close"]])

#Extract results from the ETH_Price,ipynb file
# Complete imports
#Import libraries from PyPortfolioOpt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
#Import modules for plotting
import copy
from pypfopt import risk_models, exceptions
from pypfopt import EfficientFrontier, CLA
from pypfopt import plotting
import scipy.cluster.hierarchy as sch
import warnings

#Get the stock tickers
tickers = ["ETH-USD", "VOO"]

#Set portfolio start date
stockStartDate = '2021-07-18'

#Set portfolio end date
today = datetime.today().strftime('%Y-%m-%d')

#Dataframe to store adjusted close price of the stock
st.stocks_df = pd.DataFrame()

for stock in tickers:
    st.stocks_df[stock] = web.DataReader(stock, data_source='yahoo', start= stockStartDate, end = today)['Adj Close']  

st.markdown("### Stocks Daily Returns")
#Review dataframe
st.stocks_df


# Calculate the daily returns based off the Closing price
#Create daily returns DF for Ethereum & VOO

st.markdown("### Stocks Daily Returns")
st.stocks_daily_returns_df = st.stocks_df.pct_change()
st.stocks_daily_returns_df

#Assign weights for stocks
weights = np.array([0.50, 0.50])

st.markdown("### Annual Portfolio Return")
annual_portfolio_return = np.sum(st.stocks_daily_returns_df.mean() * weights) * 252
st.write(annual_portfolio_return)

#Generate the annualized covariance matrix
st.markdown("###  Annual Portfolio Co-Variance Matrix")
stocks_annual_cov_matrix = st.stocks_daily_returns_df.cov() * 252
st.write(stocks_annual_cov_matrix)

#Generate the Portfolio 
st.markdown("### Annual Portfolio Volatility")
portfolio_variance = np.dot(weights.T, np.dot(stocks_annual_cov_matrix, weights))
st.write(portfolio_variance)

st.markdown("### Calculate the Efficient Portfolio weights with ETH & VOO for a risk of 30%")
st.markdown("### Total Starting Portfolio Value= $1,000,000")
#Asset clasifcation for Efficient Risk Portfolio
# Plot the Markov Efficient Frontier for Efficient Risk
#Portfolio Optimization
#Calculate he expected returns, annualized sample covarinace matrix of asset returns

#Portfolio Optimization
#Calculate he expected returs, annualized sample covarinace matrix of asset returns
mu = expected_returns.mean_historical_return(st.stocks_df)
S = risk_models.sample_cov(st.stocks_df)

#Optimize for the max Sharpe Ratio
ef = EfficientFrontier(mu, S)
weights = ef.efficient_risk(0.30)
cleaned_weights = ef.clean_weights()

ef.save_weights_to_file("weights.txt")  # saves to file
st.write(cleaned_weights)
mu = expected_returns.mean_historical_return(st.stocks_df)
S = risk_models.sample_cov(st.stocks_df)

#Optimize for the Efficient Risk
ef = EfficientFrontier(mu, S)
ef.add_constraint(lambda w: sum(w[0:]) == 1)

#Get the Discrete Allocation  of each share per stock (Efficient Risk; Volatility =  30%
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(st.stocks_df)
weights = cleaned_weights

da = DiscreteAllocation(weights, latest_prices, total_portfolio_value= 1000000)

allocation, leftover = da.lp_portfolio()

st.write('Discrete Allocation:', allocation)
st.write('Funds Balance: ${:.2f}'. format(leftover))




