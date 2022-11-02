// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Bridge {
    //Variables
    address payable owner;
    address payable contractor;
    uint public projectBudget;
    uint256 public immutable startTime;
    uint256 public immutable interval;
    string public name;
    string public symbol;
    mapping(address => uint) public balanceOf;
    mapping(address => uint) public releasedToken;
    
    //Events
    event PaymentSuccessful(string _message, address sender, address receiver, uint amount);
    event PaymentFailed(string _message);

    //Error
    error CallFailed();

    //Constructor
    constructor(
            string memory _name, 
            string memory _symbol,
            address payable _owner,
            address payable _contractor, 
            uint256 _projectBudget,
            uint256 PaymentInterval
    ) payable {
            owner = _owner;
            contractor = _contractor;
            name = _name;
            symbol = _symbol;
            startTime = block.timestamp;
            projectBudget = _projectBudget;
            interval = PaymentInterval;
            require(_contractor != address(0));
            require(projectBudget != 0);
    }

    //Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyContractor() {
        require(msg.sender == contractor, "Not contractor");
        _;
    }

    //Functions
    receive() external payable {
        //Used for receiving ETH from other address/contract
    }

    function transfer(address payable _to, uint256 amount) public payable{
        //Transfer funds to different address
        (bool success,) = _to.call{value: amount}("");
        if(!success){
            revert CallFailed();
        }
    }

    function getBalance() view public returns(uint) {
        //Returns the balance of contract
        return address(this).balance;
    }

    function withdrawal() public onlyOwner returns (bool success) {
        //This function is used for withdrawaling project funds when project is completed or terminated.
        owner.transfer(getBalance());
        return success;
    }

    function terminateProject() public onlyOwner returns (bool success) {
        //Terminate project and smart contract, all funds will be transferred to owner's wallet
        selfdestruct(owner);
        return success;
    }

    function vestedAmount(uint256 timestamp) public view returns(uint256) {
        if (timestamp < startTime) {
            return 0;
        } else if (timestamp > startTime + interval) {
            return projectBudget;
        } else {
            return projectBudget * (timestamp - startTime) / interval;
        }
    }

    function release() public onlyContractor {
        uint256 releaseable = vestedAmount(block.timestamp);
        releasedToken[contractor] += releaseable;
        emit PaymentSuccessful("Progress payment has been made", address(this), contractor, releaseable);
        contractor.transfer(releaseable);
    }
}

