from web3 import Web3
from decimal import Decimal

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
owner_wallet = '0x1A7398E7D7964B1552c5AbF0674060CD02C84E53'
private_key = '28fd1d38d6002514d9493cf4fe7d88a52dd888e0c6e4a15384a13e99106adde0'
contract_address = '0x790a46cA3d7eac18beAb3aA3CbD9F3a040C65401'
value = 2
account_from = {
    'private_key': private_key,
    'address': owner_wallet,
}

nonce = web3.eth.getTransactionCount(account_from['address'])

# # Build a transaction in a dict
# tx = {
#     'nonce': nonce,
#     'to': contract_address,
#     'value': web3.toWei(5, 'ether'),
#     'gas': 2000000,
#     'gasPrice': web3.toWei('50', 'gwei')
# }

# # sign transaction
# signed_tx = web3.eth.account.sign_transaction(tx, private_key)

# # send transaction
# tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# # get transaction hash
# print(web3.toHex(tx_hash))

Incrementer = web3.eth.contract(address=contract_address, abi=abi)
increment_tx = Incrementer.functions.transfer(owner_wallet, web3.toWei(5, 'ether')).buildTransaction(
    {
        'from': account_from['address'],
        'nonce': web3.eth.get_transaction_count(account_from['address']),
        'chainId' : 1337,
        'gasPrice' : web3.eth.gas_price
    }
)


tx_create = web3.eth.account.sign_transaction(increment_tx, account_from['OWNER_PRIVATE_KEY'])

# 7. Send tx and wait for receipt
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')