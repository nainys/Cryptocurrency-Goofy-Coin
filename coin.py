class GoofyCoin():
    def __init__(self, value, user_id, coin_id=None):
        self.value = value
        self.user_id = user_id
        self.id = coin_id

    def __str__(self):
        if self.id != None:
            num = self.id.coin_num
        else:
            num = '-'
        return 'Num: ' + str(num) + '\nValue: ' + str(self.value) + \
            '\nUser id: ' + self.user_id

class CoinId():
    def __init__(self, coin_num, transaction_id=None):
        self.coin_num = coin_num
        self.transaction_id = transaction_id
