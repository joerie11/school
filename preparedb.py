import random
from pymongo import MongoClient
client = MongoClient("127.0.0.1", 27017)
def strip(input):
    try:
        del input["_id"]
        return input
    except:
        pass

def create_coupon():
    db = client.koffie
    punten_col = db.coupons
    aantal = 25
    cont = 0
    while cont != aantal:
        code = random.randrange(10000000000, 90000000000)
        value = random.randrange(2, 10)
        code_dict = {"code" : code ,"value": value}

        if code_dict == strip(punten_col.find_one(code_dict)):
            continue

        else:
            punten_col.insert_one(code_dict)
            print("Coupon met code {} aangemaakt".format(punten_col.find_one(code_dict)))
            cont = cont + 1
create_coupon()