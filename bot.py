"""
Инструкция по запуску бота:

1. Создайте и активируйте виртуальное окружение (по желанию), например:
   python -m venv .venv
   source .venv/bin/activate      # Linux / macOS
   .venv\\Scripts\\activate       # Windows

2. Установите зависимости:
   pip install -r requirements.txt

3. Создайте файл .env на основе .env.example и укажите токен:
   BOT_TOKEN=1234567890:YOUR_TELEGRAM_BOT_TOKEN_HERE

4. Запустите бота:
   python bot.py
"""

from __future__ import annotations
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import router


async def main() -> None:
    """
    Точка входа для запуска Telegram-бота.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

