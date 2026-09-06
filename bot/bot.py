import asyncio
import logging
import sys
import json

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers.start import router as start_router
from bot.handlers.find_ticket import router as find_ticket_router

with open("config.json", "r") as f:
    BOT_TOKEN = json.load(f)["BOT_TOKEN"]

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(start_router)
    dp.include_router(find_ticket_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
