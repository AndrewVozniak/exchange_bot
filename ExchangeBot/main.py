from email import message
import telebot
from telebot import *
from subprocess import Popen
import os
import dotenv
import handlers.database as db


# ! DATABASE CONNECTION
database = db.connect("localhost","root", "root", "exchange_bot")
mycursor = database.cursor()

db.execute(mycursor, "SELECT * FROM `config`")
config = mycursor.fetchone()








dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
token = config[5]
adminPassword = config[6]
bot = telebot.TeleBot(token)


script = Popen(['python','./view.py']) # python если на Windows | python3 если на Linux

def checkList(data, array):
    array = list(array)
    for x in array:
        if int(data) == int(x[1]):
            return 1
        else:
            pass

    

def saveChatID(message):
    global database

    # ? DATABASE SELECT ADMINS IDS
    db.execute(mycursor, "SELECT * FROM `admins`")
    id_list = list(mycursor.fetchall())

    if checkList(message.chat.id, id_list) != 1:      
        sql = f"INSERT INTO admins (telegram_id) VALUES ({message.chat.id})"
        mycursor.execute(sql)

        database.commit()
        return True

    else:
        pass

def restartScript():
    global script 
    
    script.kill()
    script = Popen(['python','./view.py']) # python если на Windows | python3 если на Linux
    print('restarted')


def saveENV(action, message, key):
    global database
    
    home_bt = types.InlineKeyboardButton(text="На главную страницу", callback_data="home")
    keyboard = types.InlineKeyboardMarkup().add(home_bt)

    # ? UPDATING DATA IN DB
    sql = f"UPDATE `config` SET `{key}`='{message.text.partition('-')[2]}' WHERE 1"
    mycursor.execute(sql)
    database.commit()

    # ? SUCCESSFUL MSG
    if(key == "ADMIN_PASSWORD"):
        global adminPassword
        bot.send_message(message.chat.id, f"""Данные {action} успешно изменены. 
Текущий пароль от панели администратора - {message.text.partition('-')[2]}. 
Постарайся не забыть его""", reply_markup=keyboard)
        adminPassword = message.text.partition('-')[2]
        return adminPassword

    else:
        restartScript()
        bot.send_message(message.chat.id, f"""Данные {action} успешно изменены. 
Текущие - {message.text.partition('-')[2]}. 
Бот успешно перезагружен!""", reply_markup=keyboard)

        
        
def adminScreen(message):
    card_bt = types.InlineKeyboardButton(text="Изменить карту", callback_data="card")
    btc_bt = types.InlineKeyboardButton(text="Изменить btc кошелёк", callback_data="btc")

    support_bt = types.InlineKeyboardButton(text="Изменить саппорта", callback_data="support")
    rules_bt = types.InlineKeyboardButton(text="Изменить правила", callback_data="rules")
    description_bt = types.InlineKeyboardButton(text="Изменить описание", callback_data="description")
    bot_name_bt = types.InlineKeyboardButton(text="Изменить название бота", callback_data="bot_name")

    token_bt = types.InlineKeyboardButton(text="Изменить токен", callback_data="token")
    password_bt = types.InlineKeyboardButton(text="Изменить пароль", callback_data="password")
    reload_bt = types.InlineKeyboardButton(text="Перезагрузить бота", callback_data="reload")
    info_bt = types.InlineKeyboardButton(text="Информация", callback_data="information")
    
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(info_bt)
    keyboard.add(card_bt, btc_bt, rules_bt, support_bt, description_bt, password_bt, bot_name_bt, reload_bt, token_bt)

    bot.send_message(message.chat.id, f"""*❤️ Добро пожаловать в админку! ❤️*
""", parse_mode="Markdown", reply_markup=keyboard)

# CHATBOT
@bot.message_handler(content_types=["text"])
def checkUser(message):

    # ? DATABASE SELECT ADMINS IDS
    db.execute(mycursor, "SELECT * FROM `admins`")
    id_list = list(mycursor.fetchall())

    # Проверяем наличие id пользователя в admins.txt. Если он есть даем стартовое сообщение, иначе пользо   ватель должен ввести пароль 
    if checkList(message.chat.id, id_list) == 1:
        saveData(message)
    elif message.text == adminPassword:
        saveChatID(message)
        adminScreen(message)
    else:
        bot.send_message(message.chat.id, f"""Извини, я стандартный бот, я ничего не умею делать :(""")


def saveData(message):
    # ? DATABASE SELECT ADMINS IDS
    db.execute(mycursor, "SELECT * FROM `admins`")
    id_list = list(mycursor.fetchall())
    
    
    # Проверяем наличие id пользователя в admins.txt. Если он есть даем доступ к командам, иначе пользователь должен ввести пароль 
    if checkList(message.chat.id, id_list) == 1:
        if message.text.startswith('!card-'):
            saveENV('карты', message, "CARD_NUMBER")
        
        elif message.text.startswith('!btc-'):
            saveENV('btc кошелька', message, "BTC")

        elif message.text.startswith('!name-'):
            saveENV('имени', message, "BOT_NAME") 

        elif message.text.startswith('!support-'):
            saveENV('сапорта', message, "SUPPORT") 

        elif message.text.startswith('!rules-'):
            saveENV('бонуса', message, "RULES") 
        
        elif message.text.startswith('!description-'):
            saveENV('описания', message, "DESCRIPTION") 

        elif message.text.startswith('!token-'):
            saveENV('токена', message, "BOT_TOKEN")

        elif message.text.startswith('!password-'):
            saveENV('пароля', message, "ADMIN_PASSWORD")

        elif message.text.startswith('!bot_name-'):
            saveENV('имени бота', message, "BOT_NAME")

        else:
            adminScreen(message)

    else:
        bot.send_message(message.chat.id, f"""Извини, я стандартный бот, я ничего не умею делать :(""")


@bot.callback_query_handler(func=lambda call: True)
def purchaseScreen(call):
    if call.message:
        if call.data == "home":
            adminScreen(call.message)

        if call.data == "card":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !card-( Значение )")

        if call.data == "btc":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !btc-( Значение )")

        if call.data == "name":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !name-( Значение )")

        if call.data == "support":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !support-( Значение )")

        if call.data == "rules":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !rules-( Значение )")

        if call.data == "description":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !description-( Значение )")

        if call.data == "token":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !token-( Значение )")

        if call.data == "bot_name":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !bot_name-( Значение )")

        if call.data == "password":
            bot.send_message(call.message.chat.id, f"Для изменения напиши !password-( Значение )")

        if call.data == "reload":
            restartScript()
            bot.send_message(call.message.chat.id, f"Бот перезагружен.") 


        if call.data == "information":
            bot.send_message(call.message.chat.id, f"""*Текущая информация:*

*Платежные системы*
Номер карты - {os.environ['CARD_NUMBER']}
Номер BTC кошелька - {os.environ['BTC']}

Мин.сумма (рубли) - {os.environ['MIN_SUM_RUB']}
Макс.сумма (рубли) - {os.environ['MAX_SUM_RUB']}

Мин.сумма (BTC) - {os.environ['MIN_SUM_BTC']}
Макс.сумма (BTC) - {os.environ['MAX_SUM_BTC']}
""", parse_mode="Markdown") 

            bot.send_message(call.message.chat.id, f"""Текущая информация:

Сапорт - {os.environ['SUPPORT']}

--------------------------------

Бонус:
{os.environ['BONUS']}

--------------------------------

Описание: 
{os.environ['DESCRIPTION']}
""") 


            bot.send_message(call.message.chat.id, f"""Текущая информация:

Системные
Имя бота - {os.environ['BOT_NAME']}

Токен бота - {os.environ['BOT_TOKEN']}  

Токен админки - {os.environ['ADMIN_TOKEN']}

Пароль от админки - {os.environ['ADMIN_PASSWORD']}
""") 

if __name__ == '__main__':
    bot.infinity_polling()