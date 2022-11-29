import os
import requests
import handlers.database as db
from dotenv import load_dotenv

load_dotenv()

# ! DATABASE CONNECTION
database = db.connect("localhost","root", "root", "exchange_bot")

mycursor = database.cursor()
db.execute(mycursor, "SELECT * FROM `config`")
config = mycursor.fetchone()


PROJECT_NAME = "murbot"
BOT_TOKEN = config[0]
BTC =  config[1]
CARD_NUMBER = config[2]
RULES = config[3]
BOT_NAME = config[4]
SUPPORT = config[7]
DESCRIPTION =config[8]



#! CRYPTOS PRICE
BTC_PARSE_LINK = "http://rate.sx/1BTC"
BTC = requests.get(BTC_PARSE_LINK)
BTC_PRICE = float((BTC.json()))

XRP_PARSE_LINK = "http://rate.sx/1XRP"
XRP = requests.get(XRP_PARSE_LINK)
XRP_PRICE = float((XRP.json()))

TRX_PARSE_LINK = "http://rate.sx/1TRX"
TRX = requests.get(TRX_PARSE_LINK)
TRX_PRICE = float((TRX.json()))

APT_PARSE_LINK = "http://rate.sx/1APT"
APT = requests.get(APT_PARSE_LINK)
APT_PRICE = float((APT.json()))

ETH_PARSE_LINK = "http://rate.sx/1ETH"
ETH = requests.get(ETH_PARSE_LINK)
ETH_PRICE = float((ETH.json()))

MATIC_PARSE_LINK = "http://rate.sx/1MATIC"
MATIC = requests.get(MATIC_PARSE_LINK)
MATIC_PRICE = float((MATIC.json()))

DOGE_PARSE_LINK = "http://rate.sx/1DOGE"
DOGE = requests.get(DOGE_PARSE_LINK)
DOGE_PRICE = float((DOGE.json()))

LTC_PARSE_LINK = "http://rate.sx/1LTC"
LTC = requests.get(LTC_PARSE_LINK)
LTC_PRICE = float((LTC.json()))

TWT_PARSE_LINK = "http://rate.sx/1TWT"
TWT = requests.get(TWT_PARSE_LINK)
TWT_PRICE = float((TWT.json()))

BNB_PARSE_LINK = "http://rate.sx/1BNB"
BNB = requests.get(BNB_PARSE_LINK)
BNB_PRICE = float((BNB.json()))


CRYPTO_LIST = {'BTC': BTC_PRICE, 'XRP': XRP_PRICE, 'TRX': TRX_PRICE, 'APT': APT_PRICE, 'ETH': ETH_PRICE, 'MATIC': MATIC_PRICE, 'DOGE': DOGE_PRICE, 'LTC': LTC_PRICE, 'TWT': TWT_PRICE, 'BNB': BNB_PRICE}

for i in list(CRYPTO_LIST.values()):
    print(i)