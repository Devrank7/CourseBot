import os

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

from db.psql.connect import init_db
from routers import start_router, course_router, back_router, admin_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()

routers = [
    start_router.router,
    course_router.router,
    back_router.router,
    admin_router.router
]


@dispatcher.startup()
async def start():
    await init_db()
    print("Bot started")


async def main():
    dispatcher.include_routers(*routers)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
