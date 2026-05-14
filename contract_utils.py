import os
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

load_dotenv()

RPC_URL = "https://evmrpc-testnet.0g.ai"
CHAIN_ID = 16602

# We'll deploy this soon
CHARACTER_REGISTRY_ADDRESS = "0x602083006b0f25c9a0128A0D772Be1bB8f8Bc94f"


class ContractUtils:
    def __init__(self):
        self.private_key = os.getenv("PRIVATE_KEY")
        if not self.private_key:
            raise ValueError("❌ PRIVATE_KEY not found in .env")

        self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
        self.account = Account.from_key(self.private_key)

    def get_character_contract(self):
        abi = [
            {"inputs": [{"internalType": "string", "name": "name", "type": "string"},
                        {"internalType": "string", "name": "personality", "type": "string"},
                        {"internalType": "string", "name": "backstory", "type": "string"}], "name": "createCharacter",
             "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "nonpayable",
             "type": "function"},
            {"inputs": [{"internalType": "uint256", "name": "characterId", "type": "uint256"}], "name": "getCharacter",
             "outputs": [
                 {"internalType": "string", "name": "name", "type": "string"},
                 {"internalType": "string", "name": "personality", "type": "string"},
                 {"internalType": "string", "name": "backstory", "type": "string"},
                 {"internalType": "address", "name": "creator", "type": "address"},
                 {"internalType": "uint256", "name": "createdAt", "type": "uint256"}
             ], "stateMutability": "view", "type": "function"}
        ]
        return self.w3.eth.contract(address=CHARACTER_REGISTRY_ADDRESS, abi=abi)

    def send_transaction(self, function):
        tx = function.build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 800000,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': CHAIN_ID
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt, tx_hash.hex()