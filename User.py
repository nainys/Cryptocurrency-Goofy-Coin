from ecdsa import SigningKey
from transaction import Payment, CreateCoin
from coin import GoofyCoin
from get_keys import Keys
import hashlib
import ecdsa

class User:
    def __init__(self, private_key=None,name=None):

        self.name = name
        if name is not None :
            private_key = Keys.load_secret_key(name)
            public_key = Keys.load_public_key(name)

        if private_key is None:
            private_key = SigningKey.generate()
            public_key = private_key.get_verifying_key()
        self.private_key = private_key
        self.public_key  = public_key
        self.id = self.get_userid(
            self.public_key
        )

    def generate_hash(self,data):
        hash_content = str(data)
        hash_function = hashlib.sha256()
        hash_function.update(hash_content)
        return hash_function.hexdigest()

    def sign(self, message):
        return self.private_key.sign(message)

    def verify_signature(self, public_key, signature, message):
        res = public_key.verify(signature, message)
        return res

    def get_userid(self, private_key):
        return self.generate_hash(private_key.to_string())

    def create_payment(self, ids,amount,Ledger, rec_id, goofy):
        spent = []
        balance = []
        self.id = ids
        my_coins = self.get_coins(Ledger)

        #for user_id, amount in payments:
        my_coins[:] = [
            coin for coin in my_coins if coin not in spent
        ]

        print "*********"
        for c in my_coins:
            print c

        print "*********"

        flag = 0
        bal = 0
        for coin in my_coins:

            if coin.value >= amount:
                print "coin value ",coin.value
                print "amount ",amount
                spent.append(coin)
                bal = coin.value - amount
                flag = 1

                coin1 = [GoofyCoin(value = amount,user_id = rec_id)]
                balance.append(
                GoofyCoin(value = bal,user_id = ids)
                )

                goofy.create_coins(coin1)
                break


        if flag == 1:
            print "Payment Successful"
        else:
            print "Insufficient balance\n"
        return Payment(balance = balance,spent =  spent)


    def get_coins(self, Ledger):
        coins = []
        for block in Ledger.blocks:
            tx = block.transaction
            print "transaction = ",tx
            for coin in tx.balance:
                # print "Coin user id = ",coin.user_id
                # print "my id = ",self.id
                if coin.user_id == self.id:
                    coins.append(coin)
            if isinstance(tx, CreateCoin):
                continue
            for coin in tx.spent:
                if coin.user_id == self.id:
                    print "spent coin\n"
                    coins.remove(coin)
        return coins

    def __str__(self):
        separator = '-' * 30 + '\n'
        result = 'User\n' + separator + \
            'Id: ' + self.id + '\n' + separator
        return result
