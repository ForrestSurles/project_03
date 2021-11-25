# Project_03

# Smart Movements

---

## Introduction:

### Project Description:

We will be creating an application to manage a client's investment between Ethereum and an account denominated in USD that represents an investment fund. This application will allow the user to transfer funds between accounts annd see the fees associated with the transfer and currency conversion, then to execute a transfer if desired. The application will then transfer the amount beteen the options as selected. The application utilizes Python with web3 to execute the transfer while allowing the user to have a clean interface with Streamlit.

### Project Objective:

We will be create an application that utilizes Python with web3 to execute a transfer between two accounts, one being an Ethereum account and one an account denominated in USD that represents an investment fund, while allowing the user to have a clean interface with Streamlit. We will create a smart contract that can execute transactions between accounts.

### User Stories:

As a client, I want a clean and easy to understand interface.

As a client, I want to know the fees associated with a transfer of my money between different assets before I initiate the transfer.

As a financial manager, I want to save time and money by automating the transfer of my client's assets so an employee can utilize their time more effectively.

### Nest Steps:

A next step is to have the Python code call the functions in the smart contract to execute the transfer with our Solidity code, while allowing the user to have a clean interface with Streamlit. In addition, we can use our code for risk and return measurement, displaying the statistics on the Streamlit application before the user executes their decision.

---

## Technologies

This project leverages python 3.7, Solidity, Streamlit, and Ganache.

---

## Installation Guide

Before running the application first install the following dependencies:

```python
  pip install web3
  pip install python-dotenv
  pip install mkdocs
  pip install pandas
  pip install DateTime
  pip install matplotlib
  pip install PyPortfolioOpt
  pip install numpy
  pip install scipy
  pip install pytest-warnings
```

---

## Usage

To use the Smart Risk Movements application:

Clone the project_03 repository from GitHub:

'git clone https://github.com/ForrestSurles/project_03.git'

Review the app.py, acctTransfer.sol, smart_movements.ipynb, and ETH_Price.ipynb files.

Run the app.py program.

---

## Contributors

John P Weldon

Email: johnpweldon01@gmail.com

Ashley Guidot

Email: ashleyguidot@gmail.com

Forrest Surles

Email: forrest.surles@gmail.com

Vishwanath Subramanian

Email: vishkast203@gmail.com

---

## License

MIT

---
