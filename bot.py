import asyncio
import logging
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import BOT_TOKEN
from main import monitor

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")
    await monitor(message)

async def main():
    await dp.start_polling(bot)

async def send_message_to_bot(message: types.Message, text):
    await message.answer(text=text)



if __name__ == "__main__":
    asyncio.run(main())