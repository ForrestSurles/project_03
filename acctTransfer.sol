pragma solidity ^0.5.5;

// Define a new contract named `AccountTransfer`
contract AccountTransfer {

    address payable ethAcct;
    address payable mktAcct;
    uint128 public ethBalance;
    uint128 public mktBalance;
    uint128 public fees;        // TODO: Calculation and passing in of the fees

    // Define functions: deposit/withdraw/set accounts/fallback

    function ethToMkt(uint128 amount) public {

        // Verify account balance capable of payment
        require(ethAcct.balance >= amount + fees, "Insufficient funds.");

        // Transfer from the ethereum acct to the market account
        mktBalance += amount - fees;
    }

    function mktToEth(uint128 amount) public {

        // Verify account balance capable of payment
        require(mktAcct.balance >= amount + fees, "Insufficient funds.");

        // Transfer from the ethereum acct to the market account
        ethBalance += amount - fees;
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

    // default fallback function enabling reception of funds outside deposit function
    function() external payable {}
}
