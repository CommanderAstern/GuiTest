from web3 import Web3, EthereumTesterProvider
from web3.middleware import geth_poa_middleware
import json
import os
import pandas as pd
from dotenv import load_dotenv

w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai.infura.io/v3/c87232efea3046708a204b8abf889cb3'))
w3.isConnected()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
addressContract = "0xF21a8dfb7F01792802d4a0d0C9905e01fc5A9672"

abi = json.load(open('abi.json'))
contract_instance = w3.eth.contract(address=addressContract, abi=abi)

load_dotenv()
privateKey = os.getenv('PRIVATE_KEY')
# account = w3.eth.account.privateKeyToAccount(privateKey)
from_account = w3.eth.account.from_key(privateKey).address

df = pd.read_csv('batteries.csv')
for i in df.index[:-2]:
    nonce = w3.eth.getTransactionCount(from_account)
    gas = contract_instance.functions.addNewBatteryToStation(1,df.loc[i, 'ipfs'],df.loc[i, 'rfid']).estimateGas()
    tx = contract_instance.functions.addNewBatteryToStation(1,df.loc[i, 'ipfs'],df.loc[i, 'rfid']).buildTransaction({
        'chainId': 80001,
        'nonce': nonce,
    })
    gas = w3.eth.estimateGas(tx)
    tx['gas'] = gas
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(tx_hash.hex())
    # get transaction receipt to get contract address
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)
    print("\n"*5)

for i in df.index[-2:]:
    nonce = w3.eth.getTransactionCount(from_account)
    gas = contract_instance.functions.addNewBatteryToUser(from_account,df.loc[i, 'ipfs'],df.loc[i, 'rfid']).estimateGas()
    tx = contract_instance.functions.addNewBatteryToUser(from_account,df.loc[i, 'ipfs'],df.loc[i, 'rfid']).buildTransaction({
        'chainId': 80001,
        'nonce': nonce,
    })
    gas = w3.eth.estimateGas(tx)
    tx['gas'] = gas
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(tx_hash.hex())
    # get transaction receipt to get contract address
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)
    print("\n"*5)