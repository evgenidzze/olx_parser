import logging
from aiogram.utils import executor
from create_bot import dp
from main_handlers import register_handlers_main
logging.basicConfig(level=logging.INFO)

register_handlers_main(dp)

executor.start_polling(dp, skip_updates=True)
