import handlers.config as cfg

def buyBTC_inBTC(price): #? количество в биткоинах ( )
    return '{:f}'.format(price * cfg.BUY_PRICE )


def buyBTC_inRUB(price): #? количество в рублях ( )
    return '{:f}'.format(price / cfg.BUY_PRICE )


def sellBTC_inBTC(price): #? количество в биткоинах ( )
    return '{:f}'.format(price * cfg.SELL_PRICE )


def sellBTC_inRUB(price): #? количество в рублях ( )
    return '{:f}'.format(price / cfg.SELL_PRICE )