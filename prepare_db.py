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
    aantal = 50
    cont = 0
    index = 1
    while cont != aantal:
        code = index
        value = random.randrange(2, 10)
        code_dict = {"code" : code ,"value": value}

        if code_dict == strip(punten_col.find_one(code_dict)):
            continue

        else:
            punten_col.insert_one(code_dict)
            print("Coupon met code {} aangemaakt".format(punten_col.find_one(code_dict)))
            cont = cont + 1
            index += 1
create_coupon()
