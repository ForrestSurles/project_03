pragma solidity ^0.5.5;

// Define a new contract named `AccountTransfer`
contract AccountTransfer {

    address payable firmAcct;
    address payable ethAcct;
    address payable mktAcct;
    uint128 public mktBalance;
    uint128 public ethBalance;
    uint128 public fees;        // TODO: Calculation and passing in of the fees
    
    // Question: How does the program know where to transfer from; how do we code it?
    // Question: Python Streamlit application to call solidity application. How to call, compile, and deploy solidity file?

    function ethToMkt(uint amount, uint128 gasFee, uint128 transferFee) public {

        // Verify account balance capable of payment
        require(ethAcct.balance >= amount + fees, "Insufficient funds.");
        
        //Transfer transaction fee
        gasFee = 133;             //133 GWEI
        transferFee = 11000000;        //0.011 ETH = 11000000 GWEI
        fees = gasFee + transferFee;
        
        // Call the `transfer` function of the `ethAcct` and pass it the `transferAmount` to transfer as an argument.
        transferAmount = amount - fees;
        mktAcct.transfer(transferAmount);
        
        // Call the `transfer` function of the `firmAcct` and pass it the `fees` to transfer as an argument.
        firmAcct.transfer(fees);

        // Transfer from the ethereum acct to the market account
        mktBalance = mktAcct.balance;
        
    }

    function mktToEth(uint amount, uint128 gasFee, uint128 transferFee) public {

        // Verify account balance capable of payment
        require(mktAcct.balance >= amount + fees, "Insufficient funds.");
        
        //Transfer transaction fee
        gasFee = 133;             //133 GWEI
        transferFee = 11000000;        //0.011 ETH = 11000000 GWEI
        fees = gasFee + transferFee;
        
        // Call the `transfer` function of the `ethAcct` and pass it the `transferAmount` to transfer as an argument.
        transferAmount = amount - fees;
        ethAcct.transfer(transferAmount);
        
        // Call the `transfer` function of the `firmAcct` and pass it the `fees` to transfer as an argument.
        firmAcct.transfer(fees);

        // Transfer from the ethereum acct to the market account
        ethBalance = ethAcct.balance;
        
    }
