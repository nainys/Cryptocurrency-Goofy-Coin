class Payment():
    def __init__(self, balance, spent, transaction_id=-1):
        self.balance = balance
        self.spent = spent
        self.id = transaction_id

    def __str__(self):
        result = 'TransID: ' + str(self.id) + '\nType: Payment\n' + '\nSpent coins: \n'
        for coin in self.spent:
            result += str(coin) + '\n'
        result += '\nCreated coins: \n'
        for coin in self.balance:
            result += str(coin) + '\n'
        return result

class CreateCoin():
    def __init__(self, balance, transaction_id=-1):
        self.balance = balance
        self.id = transaction_id

    def __str__(self):
        string = 'TransID: ' + str(self.id) + '\nType: Coin base transaction\n' + \
            '\nCreated coins: \n'
        for coin in self.balance:
            string += str(coin) + '\n'
        return string
