from email import message
import telebot
from telebot import *
from subprocess import Popen
import handlers.config as cfg
import requests
from threading import Thread
import dotenv
import handlers.database as db


# ! DATABASE CONNECTION
database = db.connect("localhost","root", "root", "exchange_bot")
mycursor = database.cursor(buffered=True)

db.execute(mycursor, "SELECT * FROM `config`")
config = mycursor.fetchone()



cancelKeyboard = telebot.types.ReplyKeyboardMarkup(True, False)
cancelKeyboard.row('Отмена')




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




def saveENV(message, key):
    global database
    
    home_bt = types.InlineKeyboardButton(text="На главную страницу", callback_data="home")
    keyboard = types.InlineKeyboardMarkup().add(home_bt)

    # ? UPDATING DATA IN DB
    sql = f"UPDATE `config` SET `{key}`='{message.text}' WHERE 1"
    mycursor.execute(sql)
    database.commit()

    # ? SUCCESSFUL MSG
    if(key == "ADMIN_PASSWORD"):
        global adminPassword
        bot.send_message(message.chat.id, f"""Данные успешно изменены. 
Текущий пароль от панели администратора - {message.text}. 
Постарайся не забыть его""", reply_markup=keyboard)
        adminPassword = message.text
        return adminPassword

    else:
        restartScript()
        bot.send_message(message.chat.id, f"""Данные успешно изменены. 
Текущие - {message.text}. 
Бот успешно перезагружен!""", reply_markup=keyboard)



#! CHECKING NEW REQUEST TO EXCHANGE

def sendExchangerInfo():
    exc = db.connect("localhost","root", "root", "exchange_bot")

    operationsCursor = exc.cursor(buffered=True)
    adminsCursor = exc.cursor(buffered=True)

    while True:
        try:
            time.sleep(3)
            
            operationsCursor.execute(f"SELECT * FROM `operations` ORDER BY `operations`.`id` DESC")
            operation = operationsCursor.fetchone()

            adminsCursor.execute(f"SELECT * FROM `admins` WHERE 1")
            admins = adminsCursor.fetchall()


            if operation[0] != cfg.latestID: # ? если последний ид не соответсвует текущемо
                for x in admins:
                    bot.send_message(x[1], f"""✅ Привет поступила новая заявка:
`Номер:` {operation[0]}
`Тип:` {operation[1]};
`Монета:` {operation[2]};
`Средство вывода:` {operation[3]};
`Сумма:` {operation[4]} USD;
`User ID:` {operation[5]};
`User Name:` @{operation[6]};
    """, parse_mode="Markdown")

                cfg.latestID = operation[0]
            operationsCursor.close()
            adminsCursor.close()
            exc.close()

            exc = db.connect("localhost","root", "root", "exchange_bot")
            operationsCursor = exc.cursor(buffered=True)
            adminsCursor = exc.cursor(buffered=True)
        except: 
            pass
        

        
t = Thread(target=sendExchangerInfo)
t.start()

        
        








def adminScreen(message):
    card_bt = types.InlineKeyboardButton(text="Изменить карту", callback_data="card")
    btc_bt = types.InlineKeyboardButton(text="Изменить btc кошелёк", callback_data="btc")

    support_bt = types.InlineKeyboardButton(text="Изменить саппорта", callback_data="support")
    rules_bt = types.InlineKeyboardButton(text="Изменить правила", callback_data="rules")
    bot_name_bt = types.InlineKeyboardButton(text="Изменить название бота", callback_data="bot_name")

    token_bt = types.InlineKeyboardButton(text="Изменить токен", callback_data="token")
    password_bt = types.InlineKeyboardButton(text="Изменить пароль", callback_data="password")
    operations_bt = types.InlineKeyboardButton(text="Просмотреть все транзакции", callback_data="operations")
    coin_bt = types.InlineKeyboardButton(text="Настройка криптовалют", callback_data="coin")
    reload_bt = types.InlineKeyboardButton(text="Перезагрузить бота", callback_data="reload")
    info_bt = types.InlineKeyboardButton(text="Информация", callback_data="information")
    
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(info_bt)
    keyboard.add(card_bt, btc_bt, rules_bt, support_bt, password_bt, coin_bt, operations_bt, bot_name_bt, reload_bt, token_bt)

    bot.send_message(message.chat.id, f"""*❤️ Добро пожаловать в админку! ❤️*
""", parse_mode="Markdown", reply_markup=keyboard)














def changeCrypto(message, row, key):
    global database
    
    home_bt = types.InlineKeyboardButton(text="На главную страницу", callback_data="home")
    keyboard = types.InlineKeyboardMarkup().add(home_bt)

    # ? UPDATING DATA IN DB
    sql = f"UPDATE `coins` SET `{row}`='{message.text}' WHERE name = '{key}'"
    mycursor.execute(sql)
    database.commit()

    bot.send_message(message.chat.id, f"""Данные успешно изменены. 
Текущие данные {row} | {key} - {message.text}. """, reply_markup=keyboard)
    restartScript()
    cfg.getCryptos()


def addCryptoStady_Name(message):
    global cancelKeyboard
    if message.text != "Отмена":
        name = message.text
        bot.send_message(message.chat.id, f"Введите парс.ссылку для {name}", reply_markup=cancelKeyboard)
        bot.register_next_step_handler(message, addCryptoStady_Link, name)


    elif message.text == "Отмена":
        bot.send_message(message.chat.id, f"""🚫 Действие отменено""")
        adminScreen(message)
        return False


def addCryptoStady_Link(message, name):
    global database

    if(requests.get(message.text).json) and message.text != "Отмена":
        link = message.text
        sql = f"INSERT INTO coins (name, parse_link) VALUES ('{name}', '{link}')"
        mycursor.execute(sql)

        database.commit()
        restartScript()
        cfg.getCryptos()

        bot.send_message(message.chat.id, f"""{name} Добавлена. 
Коммисию можно изменить в настройках криптовалют.
""")
        adminScreen(message)


    elif message.text == "Отмена":
        bot.send_message(message.chat.id, f"""🚫 Действие отменено""")
        adminScreen(message)
        return False























# ! CHATBOT
@bot.message_handler(content_types=["text"])
def checkUser(message):

    # ? DATABASE SELECT ADMINS IDS
    db.execute(mycursor, "SELECT * FROM `admins`")
    id_list = list(mycursor.fetchall())

    # ? Проверяем наличие id пользователя в admins. Если он есть даем стартовое сообщение, иначе пользователь должен ввести пароль 
    if checkList(message.chat.id, id_list) == 1:
        adminScreen(message)
    elif message.text == adminPassword:
        saveChatID(message)
        adminScreen(message)
    else:
        bot.send_message(message.chat.id, f"""Извини, я стандартный бот, я ничего не умею делать :(""")


def saveData(message, key):
    # ? DATABASE SELECT ADMINS IDS
    db.execute(mycursor, "SELECT * FROM `admins`")
    id_list = list(mycursor.fetchall())
    
    
    # Проверяем наличие id пользователя в admins.txt. Если он есть даем доступ к командам, иначе пользователь должен ввести пароль 
    if checkList(message.chat.id, id_list) == 1 and message.text != "Отмена":
        saveENV(message, key)

    elif message.text == "Отмена":
        bot.send_message(message.chat.id, f"""🚫 Действие отменено""")
        adminScreen(message)
        return False
        
    else:
        bot.send_message(message.chat.id, f"""Извини, я стандартный бот, я ничего не умею делать :(""")


@bot.callback_query_handler(func=lambda call: True)
def purchaseScreen(call):
    global cancelKeyboard
    global config
    global mycursor

    if call.message:
        if call.data == "home":
            adminScreen(call.message)

        if call.data == "token":
            bot.send_message(call.message.chat.id, "Введи новый токен", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, saveData, "BOT_TOKEN")

        if call.data == "btc":
            bot.send_message(call.message.chat.id, "Введи новый адрес кошелька", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, saveData, "BTC")

        if call.data == "card":
            bot.send_message(call.message.chat.id, "Введи новое значение карты", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, saveData, "CARD_NUMBER")

        if call.data == "rules":
            bot.send_message(call.message.chat.id, "Введи новые правила", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, saveData, "RULES")

        if call.data == "password":
            bot.send_message(call.message.chat.id, "Введи новый админ пароль", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, saveData, "ADMIN_PASSWORD")

        if call.data == "support":
            bot.send_message(call.message.chat.id, "Введи новый текст сапорта", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, saveData, "CARD_NUMBER")

        if call.data == "operations":
            mycursor.execute(f"SELECT * FROM operations WHERE 1")

            operations = mycursor.fetchall()

            bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text=f"""🔄 История обменов""")
            for x in operations:
                bot.send_message(call.message.chat.id, reply_markup=cancelKeyboard, text=f"""`Номер:` {x[0]};
`Тип:` {x[1]};
`Монета:` {x[2]};
`Средство вывода:` {x[3]};
`Сумма:` {x[4]} USD;
`User ID:` {x[5]};
`User Name:` {x[6]};
""", parse_mode="Markdown")


        if call.data == "bot_name":
            bot.send_message(call.message.chat.id, "Введи новое имя бота", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, saveData, "BOT_NAME")


        if call.data == "reload":
            restartScript()
            bot.send_message(call.message.chat.id, f"Бот перезагружен.") 


        if call.data == "information":
            bot.send_message(call.message.chat.id, f"""*Текущая информация:*

*Платежные системы*
Номер карты - {config[2]}
Номер BTC кошелька - {config[1]}
""", parse_mode="Markdown") 

            bot.send_message(call.message.chat.id, f"""Текущая информация:

Сапорт - {config[7]}

--------------------------------

Правила:
{config[4]}
""") 


            bot.send_message(call.message.chat.id, f"""Текущая информация:

Системные
Имя бота - {config[4]}

Токен бота - {config[0]}  

Токен админки - {config[5]}

Пароль от админки - {config[6]}
""") 
















        #! CHANGE COIN
        #? LIST OF ALL COINS
        if call.data == 'coin':
            cryptoCursor = database.cursor()
            db.execute(cryptoCursor, "SELECT * FROM `coins`")
            cryptos = cryptoCursor.fetchall()

            keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
            cryptos_bt = [types.InlineKeyboardButton(i[1], callback_data=f"coin-{i[1]}") for i in cryptos]
            add_bt = types.InlineKeyboardButton("Добавить криптовалюту", callback_data=f"addCoin")
            keyboard.add(*cryptos_bt, add_bt)

            bot.send_message(call.message.chat.id, "Выберите валюту", reply_markup=keyboard)  
            cryptoCursor.close()      

        if call.data == 'addCoin':
            print(call.data.partition('-')[2])
            bot.send_message(call.message.chat.id, f"Введите название криптовалюты", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, addCryptoStady_Name)







        #? SET UP COIN
        if call.data.startswith('coin-'):
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
            commision_bt = types.InlineKeyboardButton("Изменить комиссию", callback_data=f"commission-{call.data.partition('-')[2]}")
            link_bt = types.InlineKeyboardButton("Изменить парс.ссылку", callback_data=f"parse_link-{call.data.partition('-')[2]}")
            delete_bt = types.InlineKeyboardButton("Удалить валюту", callback_data=f"delete-{call.data.partition('-')[2]}")
            keyboard.add(commision_bt, link_bt, delete_bt)

            bot.send_message(call.message.chat.id, f"Выберите действие", reply_markup=keyboard)

            
        if call.data.startswith('commission-'):
            print(call.data.partition('-')[2])
            bot.send_message(call.message.chat.id, f"Введи новвую комисию на {call.data.partition('-')[2]}", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, changeCrypto, 'commission', call.data.partition('-')[2])

        if call.data.startswith('parse_link-'):
            print(call.data.partition('-')[2])
            bot.send_message(call.message.chat.id, f"Введи новую ссылку на {call.data.partition('-')[2]}", reply_markup=cancelKeyboard)
            bot.register_next_step_handler(call.message, changeCrypto, 'parse_link', call.data.partition('-')[2])

        if call.data.startswith('delete-'):
            print(f"DELETE FROM `coins` WHERE `coins`.`name` = '{call.data.partition('-')[2]}'")
            mycursor.execute(f"DELETE FROM `coins` WHERE `coins`.`name` = '{call.data.partition('-')[2]}'")

            database.commit()

            bot.send_message(call.message.chat.id, f"{call.data.partition('-')[2]} успешно удален!")
            restartScript()




if __name__ == '__main__':
    bot.infinity_polling()