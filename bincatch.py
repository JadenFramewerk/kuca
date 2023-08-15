from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def get_binance_price_tether():
    url = 'https://www.binance.com/ru/price/tether'


    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)
        html_text = driver.page_source
        return html_text
    except Exception as e:
        print(f"Failed to get data. Error: {str(e)}")
        return None
    finally:
        driver.quit()

def find_rub_price(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    target_div = soup.find('div', {'data-bn-type': 'text', 'class': 'css-zo19gu'})

    if target_div:
        return target_div.text.strip()
    else:
        return None

def main():
    while True:
        html_text = get_binance_price_tether()
        if html_text:
            rub_price = find_rub_price(html_text)
            if rub_price:
                print("Found the RUB price:", rub_price)
            else:
                print("Failed to find the RUB price.")
        else:
            print("Failed to get data from Binance.")

        with open('rub_price_binance.txt', 'w', encoding ="utf-8") as file_bin:
            file_bin.writelines(rub_price)

        time.sleep(60)  # Ждем 60 секунд перед следующей итерацией

if __name__ == "__main__":
    main()
