import requests

url = "https://www.kucoin.com/_api/payment-api/pmtapi/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&quoteType=FIAT&source=WEB&side=BUY&platform=KUCOIN&version=v2&c=b1d1f08e0e854220ae1fd92e7ccf5f22&lang=ru_RU"

response = requests.get(url)
data = response.json()

high_prices_advcash = []

for quote in data.get('data', {}).get('quotes', []):
    if quote['paymentMethod'] == 'ADVCASH':
        high_prices_advcash.append(float(quote['highPrice']))

print("High Prices for ADVCASH:", high_prices_advcash)
