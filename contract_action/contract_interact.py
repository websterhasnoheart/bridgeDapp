from web3 import Web3
from dotenv import load_dotenv, set_key, find_dotenv
import os
import json
from web3.gas_strategies.rpc import rpc_gas_price_strategy
import time

with open('./compiled_code.json', 'r') as compiled_contract:
    compiled_code = json.load(compiled_contract)
    bytecode = compiled_code["contracts"]["bridge.sol"]["Bridge"]["evm"]["bytecode"]["object"]
    abi = json.loads(
        compiled_code["contracts"]["bridge.sol"]["Bridge"]["metadata"]
        )["output"]["abi"]
    

def deposit(amount):
    # 1. Add web3 provider
    web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PRODIVER")))
    # 2. Get address variables
    contract_address = os.getenv("CONTRACT_ADDRESS")
    private_key = os.getenv("OWNER_PRIVATE_KEY")
    wallet_address = os.getenv("OWNER_WALLET")
    print(f'Depositing {amount} eth into the smart contract, the contract address is {contract_address}')
    
    # 3. Set gas price startegy
    web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
    
    # 4. estimate gas to send transaction
    estimate_gas = web3.eth.estimateGas({
        'to':   contract_address, 
        'from': wallet_address, 
        'value': bytes(amount, encoding='utf-8')})
    
    # 5. Sign tx with private key
    tx_create = web3.eth.account.sign_transaction(
        {
            "nonce" : web3.eth.get_transaction_count(wallet_address),
            "gasPrice" : web3.eth.generate_gas_price(),
            'gas' : estimate_gas,
            "to" : contract_address,
            "value" : web3.toWei(amount, "ether"),
        }, private_key,
    )
    # 6. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Transaction has been successfully processed : {tx_receipt.transactionHash.hex()}\n')
    

def get_balance():
    web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PRODIVER")))
    contract_address = os.getenv("CONTRACT_ADDRESS")
    print(f'Reading data stored in smart contract at address {contract_address}')
    contract_instance = web3.eth.contract(address=contract_address, abi=abi)
    balance = contract_instance.functions.getBalance().call()
    balance = Web3.fromWei(balance, "ether")
    print(f'The current balance of the contract is : {balance} eth\n')


def withdrawal_funds():
    # 1. Add web3 network provider
    web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PRODIVER")))
    # 2. Get address variables
    contract_address = os.getenv("CONTRACT_ADDRESS")
    private_key = os.getenv("OWNER_PRIVATE_KEY")
    wallet_address = os.getenv("OWNER_WALLET")
    print(f"Withdrawing funds from the contract to owner's wallet..")
    
    # 3. build contract and transaction instance
    contract_instance = web3.eth.contract(address = contract_address, abi = abi)
    transaction_instance = contract_instance.functions.withdrawal().buildTransaction(
        {   
            'gasPrice' : web3.eth.gas_price,
            'from' : wallet_address,
            'nonce' : web3.eth.get_transaction_count(wallet_address)
        }
    )    
    # 4. Send transaction
    tx_create = web3.eth.account.sign_transaction(transaction_instance, private_key)
    # 5. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }\n')
    

def terminateProject():
    # 1. Add web3 connection
    web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PRODIVER")))
    # 2. Get address variables
    contract_address = os.getenv("CONTRACT_ADDRESS")
    private_key = os.getenv("OWNER_PRIVATE_KEY")
    wallet_address = os.getenv("OWNER_WALLET")
    print(f"Terminating the smart contract and returning funds from the contract to owner's wallet..")
    
    # 3. build contract and transaction instance
    contract_instance = web3.eth.contract(address = contract_address, abi = abi)
    transaction_instance = contract_instance.functions.terminate().buildTransaction(
        {   
            'gasPrice' : web3.eth.gas_price,
            'from' : wallet_address,
            'nonce' : web3.eth.get_transaction_count(wallet_address)
        }
    )    
    # 4. Send transaction
    tx_create = web3.eth.account.sign_transaction(transaction_instance, private_key)
    # 5. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }\n')
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    os.environ["LOGINED"] = "false"
    set_key(dotenv_file, "LOGINED",  os.environ["LOGINED"])

def release_payment():
    # 1. Add web3 connection
    web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PRODIVER")))
    time_stamp = time.time()
    deploy_time = float(os.getenv("DEPLOY_TIME"))
    payment_frequency = float(os.getenv("PAYMENT_FREQUENCY"))
    if time_stamp - deploy_time < payment_frequency:
        print(f"\nYour progress payment is not arrived yet, please come back later!\n")
    else:
        # 2. Get address variables
        contract_address = os.getenv("CONTRACT_ADDRESS")
        contractor_private_key = os.getenv("CONTRACTOR_PRIVATE_KEY")
        wallet_address = os.getenv("CONTRACTOR_WALLET")
        print(f'Distributing progress payment to contract wallet {wallet_address}')
        
        # Build contract and transaction instance
        contract_instance = web3.eth.contract(address = contract_address, abi = abi)
        transaction_instance = contract_instance.functions.release().buildTransaction(
            {   
                'gasPrice' : web3.eth.gas_price,
                'from' : wallet_address,
                'nonce' : web3.eth.get_transaction_count(wallet_address)
            }
        )
        
        # Send transaction
        tx_create = web3.eth.account.sign_transaction(transaction_instance, contractor_private_key)
        
        # Send tx and wait for recipt
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }\n')
    