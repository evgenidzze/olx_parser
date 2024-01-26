from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator


job_stores = {
    "default": RedisJobStore(
        jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running",
        host="localhost", port=6380
    )
}
scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores))
storage = MemoryStorage()
bot = Bot('6851807344:AAHSJnkQXajm5a5eM5enWMRg7aozPmj_hu8')
dp = Dispatcher(bot=bot, storage=storage)
scheduler.start()