import requests
import xml.etree.ElementTree as etree
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import pymongo, random, pprint

from pymongo import MongoClient
db = 0

def db_connection(ip, port):
	global db
	client = MongoClient(ip, port)
	db = client.koffie

#gebruiker aanmaken in database
#variabelen voor gebruiker
#voornaam = raw_input("voornaam: ")
#achternaam = raw_input("achternaam: ")
#geboortedatum = raw_input("geboortedatum: ")
#woonplaats = raw_input("woonplaats: ")
#klantnummer = str(random.randint(0,500))

def db_makeUser(fullname, firstname, lastname, emailaddress, customernumber, provider):
	#aanmaken gebruiker
	global db
	collection = db.users
	collection.insert_one({"User":{"provider":provider, "customernumber":customernumber,"fullname": fullname,"firstname":firstname,"lastname":lastname,"emailaddress":emailaddress, "punten": 0,}})
	return

def db_UserExist(customernumber, provider):
	global db
	collection = db.users
	if collection.find_one({"User.provider": provider,"User.customernumber": str(customernumber)}) == None:
		return 1
	return 0

def db_GetPunten(customernumber, provider):
	global db
	collection = db.users
	result = collection.find_one({"User.provider": provider,"User.customernumber": str(customernumber)})
	result = strip(result)
	return result['User']['punten']

def db_ClaimPunten(customernumber, provider, paknummer):
	global db
	print(paknummer)
	coupons = db.coupons
	db_coupon = coupons.find_one({"code" : paknummer})
	if db_coupon == None:
		return 1, "punten konden niet worden toegevoegd, de code is al gebruikt of bestaat niet"

	db_coupon =  strip(db_coupon)
	collection = db.users
	result = collection.find_one({"User.provider": provider,"User.customernumber": str(customernumber)})
	result = strip(result)
	new_value = int(result['User']['punten']) + int(db_coupon['value'])
	collection.update_one({"User.provider": provider,"User.customernumber": str(customernumber)}, { "$set": { "User.punten": str(new_value) } })

	coupons.delete_one({"code" : paknummer})
	return 0, db_coupon['value']

def strip(input):
    try:
        del input["_id"]
        return input
    except:
        pass

if __name__ == "__main__":
	db_connection('192.168.100.50', 9001)
	db_UserExist(108685268574053470126, "google")
	db_GetPunten(108685268574053470126, "google")
	db_ClaimPunten(108685268574053470126, "google", 75161609209)

	