pragma solidity ^0.5.5;

// Define a new contract named `AccountTransfer`
contract AccountTransfer {

    address payable ethAcct;
    address payable mktAcct;
    address payable firmAcct;
    uint public ethBalance;
    uint public mktBalance;
    uint public totalRequired;
    uint public gasFee = 133; //133 GWEI
    uint public conversionFee = 11000000; //0.011 ETH = 11000000 GWEI
    uint public fees = gasFee + conversionFee;
    
    // TODO: Python Streamlit application to call solidity application. Call, compile, and deploy solidity file.
    
    /*
    Define a `public` function named `setAccounts` that receive two `address payable` arguments named `account1` and `account2`.
    */
    function setAccounts() public{

        // Set the values of `mktAcct` and `firmAcct`
        mktAcct = account1;
        firmAcct = account2;
    }

    function ethToMkt(uint amount) public {

        //Calculate totalRequired
        totalRequired = amount + fees

        // Verify account balance capable of payment
        require(ethBalance >= totalRequired, "Insufficient funds.");
        
        // Call the `transfer` function of the `mktAcct` and pass it the `amount` to transfer as an argument.
        mktAcct.transfer(amount);
        
        // Call the `transfer` function of the `firmAcct` and pass it the `fees` to transfer as an argument.
        firmAcct.transfer(fees);

        // Call the `mktBalance` variable and set it equal to the balance of the `mktAcct.balance`
        mktBalance = mktAcct.balance;
        
        // Call the `ethBalance` variable and set it equal to the balance of the contract by using `address(this).balance` to reflect the new balance of the contract.
        ethBalance = address(this).balance;
        
    }
    
    function deposit() public payable {

    }

    mktToEth(uint amount) public {

        //Calculate totalRequired
        totalRequired = amount + fees

        // Verify account balance capable of payment
        require(mktBalance >= totalRequired, "Insufficient funds.");
        
        // Call the `deposit` function of the `mktAcct` and pass it the `amount` to transfer to the 'ethAcct' as an argument.
        mktAcct.deposit(amount);
        
        // Call the `transfer` function of the `firmAcct` and pass it the `fees` to transfer as an argument.
        firmAcct.transfer(fees);

        // Call the `mktBalance` variable and set it equal to the balance of the `mktAcct.balance`
        mktBalance = mktAcct.balance;
        
        // Call the `ethBalance` variable and set it equal to the balance of the contract by using `address(this).balance` to reflect the new balance of the contract.
        ethBalance = address(this).balance;
        
    }
