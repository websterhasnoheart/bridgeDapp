// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;
//To be completed : 1. Functions 2. Linear release - WTF academy
contract Bridge {
    address owner;
    address contractor;
    address admin;
    uint public projectBudget;
    mapping(address => uint) public balanceOf;
    mapping(address => mapping(address => uint)) public allowance;
    string public name = "Dapp - Bridge";
    string public symbol = "BRG";
    uint public decimals = 18;

    event PaymentSuccessed(string _message, address sender, address receiver, uint amount);
    event PaymentFailed(string _message);
    event SignatureRequestFromOwner(string _message);
    event SignatureRequestFromContractor(string _message);
    event ProjectCompletion(string _message);
    event ProjectTermination(string _message);
    

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyContractor() {
        require(msg.sender == contractor, "Not contractor");
        _;
    }

    function setParameter(address _owner, address _contractor, uint _projectBudget) external {
        owner = _owner;
        contractor = _contractor;
        projectBudget = _projectBudget;
    }

    function deposit() public payable {
        
    }

    function transfer(address receiver, uint amount) public payable returns (bool success) {
        balanceOf[msg.sender] -= amount;
        balanceOf[receiver] += amount;
        emit PaymentSuccessed('Transfer has been processed', msg.sender, receiver, amount);
        return true;
    }

    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }

    function withdrawal(uint amount) public onlyOwner returns(bool success) {
        address payable to = payable(msg.sender);
        if (amount < getContractBalance()) {
            to.transfer(amount);
            emit PaymentSuccessed('withdrawal has been successfully processed', admin, to, amount); 
            return success;
        } else {
            revert();
        }
    }

    function withdrawalContractBalance(address payable receiver) public onlyOwner returns(bool success) {
        receiver.transfer(getContractBalance());
        emit PaymentSuccessed('withdrawal has been successfully processed', admin, receiver, getContractBalance());
        return success;
    }

    function terminateProject() public onlyOwner returns (bool terminated) {

    }


    function release(uint amount) public onlyContractor returns (bool success) {

    }
}