from web3 import Web3, HTTPProvider

class Checker:
    def __init__(self, *args):
        self.account = Web3(HTTPProvider('https://mainnet.infura.io/v3/a58ece92356243b48d1447a6bb733eb7'))

    def check_wallet(self, wallet: str) -> str:
        count = len(wallet.split('\n'))
        wallet_line = wallet.split('\n')

        temp = ""

        for i in range(count):
            for wallet in wallet_line:
                wei = self.account.eth.get_balance(f'{wallet}')
                eth = self.account.fromWei(wei, 'ether')
                temp += f'\n{eth}'

        return temp