# Installation + Setup

```
cd ~/Desktop
git clone git@github.com:sumermalhotra/nft-minter.git
pip3 install pipenv
pipenv install
pipenv shell
python main.py
```

# Editting settings.py

```
CONTRACT_ADDRESS = "" # Enter NFT contract address here

TO_MINT = 5 # How many NFTs you want to mint
PRICE_PER_NFT = 0.123 # Cost per NFT

CHECK_FUNCTION = "saleIsActive" # Check function to see if mint / sale has started 

POLL_INTERVAL = 2 # how long while loop should sleep for between each CHECK_FUNCTION call
GAS_PRICE = 500 * 10 ** 9 # 500 gwei # how much you should bid for gas
```

# Create .env and edit

Input keys here.
```
ETH_HTTP_URL = ""
ETHERSCAN_KEY = ""
WALLET_ADDRESS = ""
PRIVATE_KEY = ""
```