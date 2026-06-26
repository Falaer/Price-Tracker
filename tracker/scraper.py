import requests
from bs4 import BeautifulSoup
import re


def getRozetkaPrice(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            price_element = soup.find(class_=re.compile(r'product-price.*big'))

            if price_element:
                cleanPrice = re.sub(r'[^\d]', '', price_element.text)
                return int(cleanPrice)  # Повертаємо знайдену ціну
            else:
                print("Не вдалося знайти тег з ціною на сторінці.")
                return None
        else:
            print(f"Помилка доступу до сайту. Код: {response.status_code}")
            return None
    except Exception as e:
        print(f"Сталася помилка під час парсингу: {e}")
        return None