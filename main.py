import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import asyncio
from handlers import router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

load_dotenv()

token = str(os.getenv("BOT_TOKEN"))
bot = Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        dp.include_router(router)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Сессия завершена")