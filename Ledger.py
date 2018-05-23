from transaction import CreateCoin, Payment
from base64 import b64encode
from coin import CoinId
import hashlib
class Ledger():
    def __init__(self):
        self.blocks = []

    def generate_hash(self,data):
        hash_content = str(data)
        hash_function = hashlib.sha256()
        hash_function.update(hash_content)
        return hash_function.hexdigest()

    def add_block(self, block):
        if len(self.blocks) > 0:
            block.prev_hash = self.generate_hash(self.blocks[-1])
        else:
            block.prev_hash = None
        block.transaction.id = len(self.blocks)

        coin_num = 0
        for coin in block.transaction.balance:
            coin.id = CoinId(coin_num, block.transaction.id)
            coin_num += 1

        self.blocks.append(block)
        return block

    def check_Ledger(self):
        blocks = self.blocks
        if len(blocks) == 0:
            return False

        for i in range(len(blocks)):
            if blocks[i].prev_hash != self.generate_hash(blocks[i - 1]):
                return False
        return True

    def check_coin(self, coin):
        creation_id = coin.id.transaction_id
        if coin not in self.blocks[creation_id].transaction.balance:
            print('This coin was not created')
            return False

        for i in range(creation_id + 1, len(self.blocks)):
            transaction = self.blocks[i].transaction
            #If this is payment transaction and coin is spent
            if isinstance(transaction, Payment) and coin in transaction.spent:
                print('This coin is already used')
                return False

        return True

    def check_coins(self, coins):
        for coin in coins:
            if not self.check_coin(coin):
                return False
        return True


    def __str__(self):
        separator = '-' * 30
        result = separator + 'Ledger' + separator+'\n'
        for block in self.blocks:
            result += str(block) + separator
        return result

class Block():
    def __init__(self, transaction, prev_hash=None):
        self.transaction = transaction
        self.prev_hash = prev_hash

    def __str__(self):
        return 'Block: ' + str(self.transaction.id) + \
            '\nHash previous block: ' + str(self.prev_hash) + '\n' + \
            str(self.transaction)
