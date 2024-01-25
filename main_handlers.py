import datetime
import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from bs4 import BeautifulSoup

from create_bot import scheduler, bot
from keyboards import manage_panel_kb, mail_settings_btn_menu, menu
from utils import link_in_json, add_link_json


async def start(message: types.Message, state: FSMContext):
    job = scheduler.get_job(str(message.from_user.id))
    if not job:
        url = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?currency=UAH&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D=15000'
        scheduler.add_job(start_mail_handler, trigger='interval', seconds=10, id=str(message.from_user.id),
                          kwargs={'url': url, 'chat_id': message.from_user.id})
    await message.answer(text='Ви підписались на розсилку квартир до 15000грн, очікуйте нові оголошення...\n\n'
                              'Щоб змінити критерії, змініть посилання з новими фільтрами.',
                         reply_markup=menu)


async def start_mail_handler(url, chat_id):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    ad_objects = soup.find_all('div', class_='css-1sw7q4x')
    for flat in ad_objects:
        flat_link_tag = flat.find('a', class_='css-rc5s2u')
        flat_date_tag = flat.find('p', class_='css-veheph er34gjf0')

        if flat_link_tag and flat_date_tag and 'Сьогодні' in flat_date_tag.text:
            date = flat_date_tag.text
            publish_time = datetime.datetime.strptime(date.split('о')[-1].strip(), '%H:%M')
            publish_time = publish_time + datetime.timedelta(hours=2)
            publish_time = publish_time.time().strftime('%H:%M')

            flat_link = "https://www.olx.ua" + flat_link_tag.get('href')
            if not await link_in_json(flat_link, user_id=str(chat_id)):
                await add_link_json(flat_link, user_id=str(chat_id))

                flat_name_tag = flat.find('h6', class_='css-16v5mdi er34gjf0')
                flat_name = None
                if flat_name_tag:
                    flat_name = flat_name_tag.text
                await bot.send_message(chat_id=chat_id, text=f"Сьогодні о {publish_time}\n\n"
                                                             f"{flat_name}\n\n"
                                                             f"{flat_link}")


class FSMParser(StatesGroup):
    new_url = State()


async def change_url(message: types.CallbackQuery, state: FSMContext):
    await FSMParser.new_url.set()
    scheduler.remove_job(str(message.from_user.id))
    await bot.send_message(chat_id=message.from_user.id, text='Надішліть посилання з новими фільтрами:')


async def load_new_url(message: types.Message, state: FSMContext):
    new_url = message.text
    job = scheduler.get_job(str(message.from_user.id))
    if job:
        job.remove()
    scheduler.add_job(start_mail_handler, trigger='interval', seconds=10, id=str(message.from_user.id),
                      kwargs={'url': new_url, 'chat_id': message.from_user.id})
    await message.answer(text='✅ Посилання змінено', reply_markup=menu)


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_callback_query_handler(change_url, Text('mail_settings'), state='*')
    dp.register_message_handler(change_url, Text('mail_settings'), state='*')
    dp.register_message_handler(load_new_url, state=FSMParser.new_url)
