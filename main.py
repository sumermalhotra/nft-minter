from dotenv import load_dotenv
load_dotenv();

import os
import json
import time
import settings
import requests
from web3 import Web3

def get_abi(contract_address):
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={os.getenv('ETHERSCAN_KEY')}"
    response = requests.get(url)
    return json.loads(response.json()['result'])

def get_nonce():
    global web3
    return web3.eth.getTransactionCount(os.getenv("WALLET_ADDRESS"))

def get_status():
    global nft_contract
    return nft_contract.functions[settings.CHECK_FUNCTION]().call()

def estimate_gas_limit(func, value):
    return int(func.estimateGas({
        'from': os.getenv("WALLET_ADDRESS"),
        'value': value,
        'nonce': get_nonce(),
    }))

def submit_tx(tx):
    global web3
    signed_txn = web3.eth.account.sign_transaction(
        tx, private_key=os.getenv("PRIVATE_KEY"))
    h = web3.eth.sendRawTransaction(
        signed_txn.rawTransaction).hex()

def build_tx(func, value=0):
    return func.buildTransaction({
        'from': os.getenv("WALLET_ADDRESS"),
        'value': value,
        'nonce': get_nonce(),
        'gasPrice': settings.GAS_PRICE,
        'gas': estimate_gas_limit(func, value),
    })

def mint_nft():
    global nft_contract
    mint_function = nft_contract.functions.mint(settings.TO_MINT)
    tx = build_tx(
        mint_function, 
        int(settings.TO_MINT * settings.PRICE_PER_NFT * 10 ** 18))
    submit_tx(tx)

if __name__ == "__main__":
    web3 = Web3(Web3.HTTPProvider(os.getenv('ETH_HTTP_URL')))
    nft_contract = web3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_abi(settings.CONTRACT_ADDRESS)
    )

    while not get_status(nft_contract):
        print("Status still false...")
        time.sleep(settings.POLL_INTERVAL)

    mint_nft(nft_contract)