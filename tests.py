import coin
from Goofy import Goofy
from coin import GoofyCoin, CoinId
import Ledger
from transaction import CreateCoin,Payment
from User import User


print "0. No action - EXIT"
print "1. Goofy Create coins"
print "2. Make payment"
num = input("Enter action to perform\n")
goofy = Goofy()

while(num!=0):


    if num == 1:

        amt = input("Enter number of coins to generate\n")
        coins = [GoofyCoin(value=amt,user_id = goofy.user.id)]
        goofy.create_coins(coins)
        print(goofy.Ledger)

    elif num == 2:
        sender = input("Enter Sender\n")
        receiver = input("Enter Receiver\n")
        sender = User(name = sender)
        receiver = User(name = receiver)
        amt = input("Enter coins to pay\n")

        payment = sender.create_payment(sender.id,amt,goofy.Ledger,receiver.id,goofy)
        signature = sender.sign(goofy.generate_hash(payment))
        payment_result = goofy.process_payment(
            payment, [(sender.public_key, signature)]
        )
        if payment_result is None :
            print "Payment not verified"
        print(goofy.Ledger)

    elif num==0:
        sys.exit()

    else:
        print "Invalid action\n"

    num = input("Enter action to perform\n")
