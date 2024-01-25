from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

manage_panel_kb = InlineKeyboardMarkup(row_width=2)
mail_settings_btn = InlineKeyboardButton(text='Змінити посилання', callback_data='mail_settings')

manage_panel_kb.add(mail_settings_btn)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
mail_settings_btn_menu = KeyboardButton(text='Змінити посилання', callback_data='mail_settings')
menu.add(mail_settings_btn_menu)