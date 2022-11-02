// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract TokenVesting {
    mapping(address => uint256) public releasedToken;
    address public immutable beneficiary;
    uint256 public immutable startTime;
    uint256 public interval;

    event tokenReleased(address indexed token, uint256 amount);

    constructor(address beneficiaryAddress, uint256 PaymentInterval) {
        require(beneficiaryAddress != address(0));
        beneficiary = beneficiaryAddress;
        startTime = block.timestamp;
        interval = PaymentInterval;
    }

    function vestedAmount()


}