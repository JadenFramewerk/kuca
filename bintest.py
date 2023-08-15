import requests
import json
import time

data_sell = {
    "proMerchantAds": False,
    "page": 1,
    "rows": 20,
    "payTypes": [],
    "countries": [],
    "publisherType": None,
    "asset": "USDT",
    "fiat": "RUB",
    "tradeType": "BUY"
}

data_buy = {
    "proMerchantAds": False,
    "page": 1,
    "rows": 20,
    "payTypes": [],
    "countries": [],
    "publisherType": None,
    "asset": "USDT",
    "fiat": "RUB",
    "tradeType": "SELL"
}

# Emoji Unicode representations for Telegram Binance
emoji_sell = u'\U0001F4C5'
emoji_buy = u'\U0001F4B0'

while True:
    result_sell = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", json=data_sell)
    result_sell = json.loads(result_sell.text)
    price_sell = float(result_sell['data'][0]['adv']['price'])
    time.sleep(20)

    result_buy = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", json=data_buy)
    result_buy = json.loads(result_buy.text)
    price_buy = float(result_buy['data'][0]['adv']['price'])

    with open('p2p_data.txt', 'w', encoding="utf-8") as file_p2p:
        file_p2p.write(emoji_sell + ' SELL FROM P2P BINANCE: ' + str(price_sell) + '\n')
        file_p2p.write(emoji_buy + ' BUY  FROM P2P BINANCE: ' + str(price_buy) + '\n')

    time.sleep(20)
