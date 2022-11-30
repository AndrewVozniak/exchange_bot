import os
import requests
import handlers.database as db
from dotenv import load_dotenv

load_dotenv()

# ! DATABASE CONNECTION
database = db.connect("localhost","root", "root", "exchange_bot")

mycursor = database.cursor(buffered=True)
db.execute(mycursor, "SELECT * FROM `config`")
config = mycursor.fetchone()


PROJECT_NAME = "murbot"
BOT_TOKEN = config[0]
BTC =  config[1]
CARD_NUMBER = config[2]
RULES = config[3]
BOT_NAME = config[4]
SUPPORT = config[7]

latestID = 0

#! CRYPTOS PRICE
CRYPTO_LIST = {}


def getCryptos():
    global CRYPTO_LIST
    CRYPTO_LIST = {}
    
    cryptoCursor = database.cursor()
    db.execute(cryptoCursor, "SELECT * FROM `coins`")
    cryptos = cryptoCursor.fetchall()


    for i in cryptos:
        print(i[1])
        CRYPTO_LIST[i[1]] = requests.get(i[3]).json()

        
    return CRYPTO_LIST

getCryptos()