// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract test {
    address public contractOwner;
    event Log(uint amount);
    error CallFailed();
    constructor () payable {
        contractOwner = msg.sender;
    }

    function deposit(uint amount) public payable {
    (bool success,) = msg.sender.call{value: amount}("");
    if(!success){
        revert CallFailed();
        }
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}