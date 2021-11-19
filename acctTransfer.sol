pragma solidity ^0.5.5

// Define a new contract named `AccountTransfer`
contract AccountTransfer {

    address payable accountOne;
    address payable accountTwo;
    uint128 public contractBalance;

    // Define functions: deposit/withdraw/set accounts/fallback

    function withdraw(uint128 amount, address payable sourceAcct) public {

        // Verify authorized account
        require(sourceAcct == accountOne || sourceAcct == accountTwo, "Unverified account.");

        // Verify account balance capable of payment
        require(sourceAcct.balance >= amount, "Insufficient funds.");

        // Establish balance of the contract (transaction)
        contractBalance = address(this).balance;
    }

    function deposit() public payable {

        // TODO: Verify logic of this assignment with both desposit/withdraw functions
        // Establish balance of the contract (transaction)
        contractBalance = address(this).balance;
    }

    function setAccounts(address payable acct1, address payable acct2) public {

        sourceAcct = acct1
        destAcct = acct2
    }
