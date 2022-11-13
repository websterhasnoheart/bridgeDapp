from web3 import Web3
from dotenv import load_dotenv
import os
import json

with open('./compiled_code.json', 'r') as compiled_contract:
    compiled_code = json.load(compiled_contract)
    bytecode = compiled_code["contracts"]["bridge.sol"]["Bridge"]["evm"]["bytecode"]["object"]
    abi = json.loads(
        compiled_code["contracts"]["bridge.sol"]["Bridge"]["metadata"]
        )["output"]["abi"]
    

contract_address = os.getenv("CONTRACT_ADDRESS")

def deposit(amount):
    pass

def get_balance():
    web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PRODIVER")))
    contract_address = os.getenv("CONTRACT_ADDRESS")
    print(f'Reading data stored in smart contract at address {contract_address}')
    contract_instance = web3.eth.contract(address=contract_address, abi=abi)
    balance = contract_instance.functions.getBalance().call()
    balance = Web3.fromWei(balance, "ether")
    print(f'The current balance of the contract is : {balance} eth')


def withdrawal_funds(amount):
    pass

def terminateProject():
    pass

def release_payment():
    pass  