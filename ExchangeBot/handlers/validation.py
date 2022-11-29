def validateCard(card):
    try:
        card = str(card).replace(' ', '')

        if int(card.isnumeric()):
            if len(card) == 13 or len(card) == 16 or len(card) == 19:
                return True
            else: 
                return False
    except:
        return False

def validateBTC(BTC):
    try:
        BTC = str(BTC).replace(' ', '')

        flag_let = False
        flag_num = False
        flag_low = False

        for i in BTC:
            if i.isalpha():
                flag_let = True

            if i.isdigit():
                flag_num = True

            if i.islower():
                flag_low = True

        if flag_let and flag_num and flag_low:
            if BTC.startswith("1") or BTC.startswith("3") or BTC.startswith("bc1q") or BTC.startswith("bc1p") and len(BTC) <= 10:
                return True
            else: 
                return False
        else: 
            return False
    except:
        return False

def checkSum(min, max, current):
    try: 
        min = float(min)
        max = float(max)
        current = float(current)

        if float(current) >= min and float(current) <= max:
            return True
        else:
            return False
    except:
        return False

print(validateCard("4441114411444444"))