from web3 import Web3
import os
from solcx import compile_standard, install_solc
from dotenv import load_dotenv, set_key, find_dotenv
import json
import time

with open('./compiled_code.json', 'r') as compiled_contract:
    compiled_code = json.load(compiled_contract)
    bytecode = compiled_code["contracts"]["bridge.sol"]["Bridge"]["evm"]["bytecode"]["object"]
    abi = json.loads(
        compiled_code["contracts"]["bridge.sol"]["Bridge"]["metadata"]
        )["output"]["abi"]

def compile():
    # Load env variables
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)

    #Load smart contract
    with open('contracts/bridge.sol', 'r') as contract:
        bridge_contract = contract.read()
    
    #Install solidity compiler
    _solc_version = os.getenv("SOLIDITY_VERSION")
    install_solc(_solc_version)

    #Compile smart contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"bridge.sol": {"content": bridge_contract}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version=_solc_version,
    )
    print("The smart contract has been successfully compiled!")
    with open("compiled_code.json", 'w') as compiled_contract:
        json.dump(compiled_sol, compiled_contract)
    

def deploy():
    #load env variables and compiled contract code
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    time_stamp = time.time()
    os.environ["DEPLOY_TIME"] = str(time_stamp)
    set_key(dotenv_file, "DEPLOY_TIME",  os.environ["DEPLOY_TIME"])
    # Create the contract in Python
    
    chain_id = int(os.getenv("CHAIN_ID"))
    wallet_address = os.getenv("OWNER_WALLET")
    private_key = os.getenv("OWNER_PRIVATE_KEY")
    owner_address = os.getenv("OWNER_WALLET")
    contractor_address = os.getenv("CONTRACTOR_WALLET")
    project_Budget = int(os.getenv("PROJECT_BUDGET"))
    payment_Times = int(os.getenv("PAYMENT_NUMBER"))
    payment_Interval = int(os.getenv("PAYMENT_FREQUENCY"))
    project_name = os.getenv("PROJECT_NAME")
    project_symbol = os.getenv("PROJECT_SYMBOL")
    
    # Build Transaction to deploy contract
    web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PRODIVER")))
    Bridge = web3.eth.contract(abi = abi, bytecode = bytecode)
    nonce = web3.eth.getTransactionCount(wallet_address)
    transaction  = Bridge.constructor(
                    _name = project_name, _symbol = project_symbol, _owner = owner_address, _contractor = contractor_address,
                    _projectBudget = project_Budget, 
                    _paymentTimes = payment_Times, 
                    _paymentInterval = payment_Interval
                    ).buildTransaction(
                        {
                        "gasPrice": web3.eth.gas_price, 
                        "chainId": chain_id, 
                        "from": owner_address, 
                        "value" : 0,
                        "nonce": nonce
                        }
                    )

    signed_tx = web3.eth.account.sign_transaction(transaction, private_key = private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print('Uploading stored value...')
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    os.environ["CONTRACT_ADDRESS"] = tx_receipt.contractAddress
    set_key(dotenv_file, "CONTRACT_ADDRESS",  os.environ["CONTRACT_ADDRESS"])
    print(f'Contract deployed at address: { tx_receipt.contractAddress }')
