import asyncio
import datetime
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier

toaster = ToastNotifier()

option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
option.add_argument('-headless')
browser = webdriver.Firefox(options=option)
browser.get("https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?currency=UAH&search"
            "%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D=13000")


async def monitor(message):
    latest_time = datetime.datetime.strptime("00:00", "%H:%M")
    while True:
        try:
            all_items = browser.find_elements(By.CLASS_NAME, 'css-1sw7q4x')
            for item in all_items:
                date_place = item.find_element(By.CSS_SELECTOR, "[data-testid='location-date']").text.split('-')
                place = date_place[0]
                date = date_place[1]

                if 'Сьогодні' in date:
                    item_time = datetime.datetime.strptime(date.split(' ')[-1], "%H:%M")
                    if item_time >= latest_time:
                        latest_time = item_time
                        name = item.find_element(By.CLASS_NAME, 'css-16v5mdi').text
                        url = item.find_element(By.CLASS_NAME, 'css-rc5s2u').get_attribute('href')

                        with open('data.json', 'r+', encoding='utf-8') as file:
                            file_data = json.load(file)
                            if not url in file_data['items']:
                                file_data['items'][url] = date
                                file.seek(0)
                                json.dump(file_data, file, indent=4, ensure_ascii=False)
                                await message.answer(text=f"{name}\n"
                                                          f"Час публікації: {item_time.time()}"
                                                          f"{url}\n")

        except Exception as error:
            print(error)
        await asyncio.sleep(10)
        browser.refresh()
