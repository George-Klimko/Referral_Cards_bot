"""
Конфиг бота.

- BOT_TOKEN берётся из переменных окружения (см. .env.example)
- PHOTO_* — заглушки для photo_id / URL / file_id Telegram.
  Замените значения на реальные перед запуском в проде.
"""

from __future__ import annotations

import os
from aiogram.types import FSInputFile
from aiogram.types import InputMediaPhoto
from dotenv import load_dotenv


load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Environment variable {name!r} is required. "
            f"Create a .env file (see .env.example)."
        )
    return value


BOT_TOKEN: str = _require_env("BOT_TOKEN")

# Пауза между сообщениями (требование ТЗ)
SEND_DELAY_SECONDS: float = 0.2

# Заглушки картинок для каждого шага.
# Можно подставить file_id (строка), либо URL на картинку.
PHOTO_1: str = "image.png"
PHOTO_2: str = "image.png"
PHOTO_3: str = "image.png"
PHOTO_4: str = "image.png"
PHOTO_5: str = "image.png"
PHOTO_6: str = "image.png"

PHOTO_1: FSInputFile = FSInputFile("image.png")
PHOTO_2: FSInputFile = FSInputFile("image.png")
PHOTO_3: FSInputFile = FSInputFile("image.png")
PHOTO_4: FSInputFile = FSInputFile("image.png")
PHOTO_5: FSInputFile = FSInputFile("image.png")
PHOTO_6: FSInputFile = FSInputFile("image.png")