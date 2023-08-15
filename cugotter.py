import time
import json
import os
import pickle
import statistics
import math
import requests

def make_request(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for any HTTP errors
    json_data = response.json()
    return json_data

def save_data_to_cache(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def save_data_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

def format_order_info(order):
    formatted_info = f"Payment Method: {order['paymentMethod']}\n"
    formatted_info += f"Payment Type: {order['paymentType']}\n"
    formatted_info += f"Price: {order['price']} {order['fiatCurrency']}\n"
    formatted_info += f"High Price: {order['highPrice']} {order['fiatCurrency']}\n"
    return formatted_info

def save_median_to_file(median_crypto, median_fiat, file_path, quote_type_crypto_response, quote_type_fiat_response):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("All Orders (SELL):\n")
        for quote in quote_type_crypto_response.get('data', {}).get('quotes', []):
            if quote['paymentMethod'] == 'Advcash':  # Фильтр по 'payment_method': 'Advcash'
                formatted_order_info = format_order_info(quote)
                file.write(formatted_order_info)
                file.write("\n")
        file.write("\n")
        file.write("All Orders (BUY):\n")
        for quote in quote_type_fiat_response.get('data', {}).get('quotes', []):
            if quote['paymentMethod'] == 'Advcash':  # Фильтр по 'payment_method': 'Advcash'
                formatted_order_info = format_order_info(quote)
                file.write(formatted_order_info)
                file.write("\n")

def main():
    quote_type_crypto_url = "https://www.kucoin.com/_api/payment-api/pmtapi/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&quoteType=CRYPTO&source=WEB&side=SELL&platform=KUCOIN&version=v2&c=9dfb4245fe7948639ed29ef92fd6a399&lang=ru_RU"
    quote_type_fiat_url = "https://www.kucoin.com/_api/payment-api/pmtapi/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&quoteType=FIAT&source=WEB&side=BUY&platform=KUCOIN&version=v2&c=9dfb4245fe7948639ed29ef92fd6a399&lang=ru_RU"

    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    quote_type_crypto_cache_file = os.path.join(cache_dir, 'quote_type_crypto_cache.pickle')
    quote_type_fiat_cache_file = os.path.join(cache_dir, 'quote_type_fiat_cache.pickle')

    while True:
        try:
            quote_type_crypto_response = make_request(quote_type_crypto_url)
            save_data_to_cache(quote_type_crypto_response, quote_type_crypto_cache_file)
            high_prices_crypto = [float(quote['highPrice']) for quote in quote_type_crypto_response.get('data', {}).get('quotes', [])]

            quote_type_fiat_response = make_request(quote_type_fiat_url)
            save_data_to_cache(quote_type_fiat_response, quote_type_fiat_cache_file)
            high_prices_fiat = [float(quote['highPrice']) for quote in quote_type_fiat_response.get('data', {}).get('quotes', [])]

            # Calculate the median for crypto and fiat high prices
            median_crypto = statistics.median(high_prices_crypto)

            # Check if high_prices_fiat is empty
            if high_prices_fiat:
                median_fiat = statistics.median(high_prices_fiat)
            else:
                # Set a default value if the list is empty
                median_fiat = 0.0  # You can set any default value here

            # Save all orders and median rounded values to a text file
            save_median_to_file(median_crypto, median_fiat, 'output.txt', quote_type_crypto_response, quote_type_fiat_response)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(14)  # Wait 14 seconds before retrying

        time.sleep(40)  # Wait 40 seconds before the next request

if __name__ == "__main__":
    main()
