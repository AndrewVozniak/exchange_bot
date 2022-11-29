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



#! BTC
BTC_PARSE_LINK = "https://blockchain.info/ticker"

r = requests.get(BTC_PARSE_LINK)
BTC_BUY_PRICE = float((r.json()['RUB']['buy']))
BTC_SELL_PRICE = float((r.json()['RUB']['sell']))
