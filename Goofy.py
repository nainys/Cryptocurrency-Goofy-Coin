from Ledger import Ledger, Block
from ecdsa import SigningKey
from transaction import CreateCoin
import hashlib
from coin import GoofyCoin, CoinId
from User import User

class Goofy():
    def __init__(self):
        self.user = User(name = "goofy")
        self.Ledger = Ledger()
        self.genesis_block_hash = self.generate_hash(self.add_genesis_block())
        self.last_block_signature = self.user.sign(
            self.genesis_block_hash.encode()
        )

    def generate_hash(self,data):
        hash_content = str(data)
        hash_function = hashlib.sha256()
        hash_function.update(hash_content)
        return hash_function.hexdigest()

    def add_genesis_block(self):
        coin = GoofyCoin(0, self.user.id, CoinId(0,0))
        return self.create_coins([coin])

    def create_coins(self, coins):
        transaction = CreateCoin(balance=coins)
        block = Block(transaction)
        return self.Ledger.add_block(block)

    def process_payment(self, payment, signatures):
        if (not self.verify_signatures(payment, signatures) ):
            print "Signature not verified"
            return None

        if (not self.Ledger.check_coins(payment.spent)):
            print "Coins not verified"
            return None

        block = Block(payment)
        return self.Ledger.add_block(block)

    def verify_signatures(self, transaction, signatures):
        for public_key, signature in signatures:
            if not self.user.verify_signature(public_key, signature, self.generate_hash(transaction)):
                return False

        users = []
        for public_key, signature  in signatures:
            user_id = self.user.get_userid(public_key)
            users.append(user_id)
        for coin in transaction.spent:
            if coin.user_id not in users:
                return False

        return True
