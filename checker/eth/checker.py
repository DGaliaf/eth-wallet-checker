from web3 import Web3, HTTPProvider

class Checker:
    def __init__(self, *args):
        self.web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/a58ece92356243b48d1447a6bb733eb7'))